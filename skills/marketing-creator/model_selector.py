#!/usr/bin/env python3
"""
Model Selector - Intelligent model selection for cost optimization

Automatically selects the optimal BytePlus ModelArk model based on:
- Platform requirements
- Quality needs
- Speed/budget constraints
- Content type
"""

__version__ = "1.3.0"

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class ContentType(Enum):
    PRODUCT_PHOTO = "product_photo"
    LIFESTYLE = "lifestyle"
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    ABSTRACT = "abstract"
    TEXT_HEAVY = "text_heavy"
    VIDEO_PRODUCT = "video_product"
    VIDEO_LIFESTYLE = "video_lifestyle"
    VIDEO_ABSTRACT = "video_abstract"


class QualityLevel(Enum):
    DRAFT = "draft"           # Quick iterations, low cost
    STANDARD = "standard"     # Good enough for most uses
    HIGH = "high"             # Professional quality
    PREMIUM = "premium"       # Maximum quality, highest cost


@dataclass
class ModelOption:
    """Represents a model option with cost and capability info."""
    model_id: str
    name: str
    cost_tier: int  # 1-4, higher = more expensive
    quality_score: int  # 1-10
    speed_score: int  # 1-10 (higher = faster)
    best_for: List[str]
    estimated_cost_usd: float
    supports_i2i: bool = False  # Whether model supports image-to-image


# Image Model Catalog (from BytePlus API)
IMAGE_MODELS = {
    "seedream-4.0": ModelOption(
        model_id="seedream-4-0-250828",
        name="Seedream 4.0",
        cost_tier=1,
        quality_score=8,
        speed_score=8,
        best_for=["standard_content", "social_media", "web_graphics", "image_to_image"],
        estimated_cost_usd=0.030,  # $0.03 per image
        supports_i2i=True,  # Supports image-to-image generation
    ),
    "seedream-4.5": ModelOption(
        model_id="seedream-4-5-251128",
        name="Seedream 4.5",
        cost_tier=2,
        quality_score=9,
        speed_score=7,
        best_for=["marketing_materials", "presentations", "product_shots", "image_to_image"],
        estimated_cost_usd=0.040,  # $0.04 per image
        supports_i2i=True,  # Supports image-to-image generation
    ),
    "seedream-5.0": ModelOption(
        model_id="seedream-5-0-260128",
        name="Seedream 5.0",
        cost_tier=3,
        quality_score=10,
        speed_score=6,
        best_for=["premium_content", "high_end_product"],
        estimated_cost_usd=0.035,  # $0.035 per image
        supports_i2i=False,  # Does NOT support image-to-image
    ),
}

# Video Model Catalog (from BytePlus API)
VIDEO_MODELS = {
    "seedance-1.0-lite-t2v": ModelOption(
        model_id="seedance-1-0-lite-t2v-250428",
        name="Seedance 1.0 Lite T2V",
        cost_tier=1,
        quality_score=6,
        speed_score=9,
        best_for=["social_stories", "quick_content", "drafts", "iterations"],
        estimated_cost_usd=0.001,  # $0.0010/K tokens
    ),
    "seedance-1.0-pro": ModelOption(
        model_id="seedance-1-0-pro-250528",
        name="Seedance 1.0 Pro",
        cost_tier=2,
        quality_score=8,
        speed_score=7,
        best_for=["professional_content", "ads", "presentations"],
        estimated_cost_usd=0.0024,  # $0.0024/K tokens
    ),
    "seedance-1.0-pro-fast": ModelOption(
        model_id="seedance-1-0-pro-fast-251015",
        name="Seedance 1.0 Pro Fast",
        cost_tier=2,
        quality_score=8,
        speed_score=9,
        best_for=["fast_production", "social_content", "quick_turnaround"],
        estimated_cost_usd=0.0017,  # $0.0017/K tokens
    ),
    "seedance-1.5-pro": ModelOption(
        model_id="seedance-1-5-pro-251215",
        name="Seedance 1.5 Pro",
        cost_tier=3,
        quality_score=10,
        speed_score=6,
        best_for=["premium_content", "high_end_ads", "cinematic"],
        estimated_cost_usd=0.0030,  # $0.0030/K tokens
    ),
}

# Resolution cost multipliers for video
VIDEO_RESOLUTION_MULTIPLIERS = {
    "480p": 0.5,
    "720p": 1.0,
    "1080p": 2.5,
    "2k": 3.5,
}

# Duration cost multipliers (base is 5s)
def get_duration_multiplier(duration: int) -> float:
    """Calculate cost multiplier based on duration."""
    return max(0.8, duration / 5.0)


class ModelSelector:
    """Intelligent model selector for cost-optimized generation."""
    
    def __init__(self, budget_mode: str = "balanced"):
        """
        Initialize selector.
        
        Args:
            budget_mode: "economy", "balanced", or "premium"
        """
        self.budget_mode = budget_mode
    
    def select_image_model(
        self,
        content_type: ContentType = ContentType.LIFESTYLE,
        quality: QualityLevel = QualityLevel.STANDARD,
        platform: str = "instagram",
        urgency: str = "normal",  # "asap", "normal", "flexible"
        has_text: bool = False,
    ) -> Dict[str, Any]:
        """
        Select optimal image model based on requirements.
        
        Returns dict with:
        - model_key: str (short name)
        - model_id: str (full API ID)
        - reasoning: str (why this model)
        - estimated_cost: float
        - alternatives: list of options
        """
        candidates = list(IMAGE_MODELS.values())
        
        # Filter by quality requirement
        if quality == QualityLevel.DRAFT:
            candidates = [m for m in candidates if m.cost_tier <= 2]
        elif quality == QualityLevel.STANDARD:
            candidates = [m for m in candidates if 2 <= m.cost_tier <= 3]
        elif quality == QualityLevel.HIGH:
            candidates = [m for m in candidates if m.cost_tier >= 3]
        elif quality == QualityLevel.PREMIUM:
            candidates = [m for m in candidates if m.cost_tier == 4]
        
        # For text-heavy content, prefer higher quality models
        if has_text and quality.value in ["standard", "high", "premium"]:
            candidates = [m for m in candidates if m.quality_score >= 7]
        
        # For urgent requests, prioritize speed
        if urgency == "asap":
            candidates.sort(key=lambda m: (-m.speed_score, m.cost_tier))
        else:
            # Balance quality and cost
            candidates.sort(key=lambda m: (m.quality_score / m.cost_tier), reverse=True)
        
        if not candidates:
            # Fallback to seedream-3.0
            selected = IMAGE_MODELS["seedream-3.0"]
            model_key = "seedream-3.0"
        else:
            selected = candidates[0]
            # Find the key for this model
            model_key = next(
                k for k, v in IMAGE_MODELS.items() 
                if v.model_id == selected.model_id
            )
        
        # Build reasoning
        reasoning_parts = [f"Selected {selected.name}"]
        
        if urgency == "asap":
            reasoning_parts.append(f"fastest option ({selected.speed_score}/10 speed)")
        
        if quality == QualityLevel.DRAFT:
            reasoning_parts.append("for quick iteration (draft quality)")
        elif quality == QualityLevel.PREMIUM:
            reasoning_parts.append("for maximum quality output")
        elif selected.cost_tier <= 2:
            reasoning_parts.append("for cost efficiency")
        
        if platform in ["tiktok", "instagram_stories"]:
            reasoning_parts.append("optimized for mobile viewing")
        
        # Get alternatives
        alternatives = [
            {
                "model": k,
                "cost": v.estimated_cost_usd,
                "quality": v.quality_score,
                "speed": v.speed_score,
            }
            for k, v in IMAGE_MODELS.items()
            if v.model_id != selected.model_id
        ]
        
        return {
            "model_key": model_key,
            "model_id": selected.model_id,
            "name": selected.name,
            "reasoning": ", ".join(reasoning_parts),
            "estimated_cost_usd": selected.estimated_cost_usd,
            "quality_score": selected.quality_score,
            "speed_score": selected.speed_score,
            "cost_tier": selected.cost_tier,
            "alternatives": alternatives,
        }
    
    def select_i2i_model(
        self,
        quality: QualityLevel = QualityLevel.STANDARD,
        platform: str = "instagram",
        urgency: str = "normal",
        num_reference_images: int = 1,
    ) -> Dict[str, Any]:
        """
        Select optimal image-to-image model based on requirements.
        
        Only considers models that support image-to-image (seedream-4.0, seedream-4.5).
        
        Args:
            quality: Desired quality level
            platform: Target platform
            urgency: Speed priority
            num_reference_images: Number of reference images (2+ suggests fusion capability needed)
            
        Returns:
            Dict with model selection details
        """
        # Filter to only I2I-capable models
        candidates = [m for m in IMAGE_MODELS.values() if m.supports_i2i]
        
        if not candidates:
            return {
                "success": False,
                "error": "No image-to-image capable models available",
                "supported_models": ["seedream-4.0", "seedream-4.5"],
            }
        
        # Filter by quality requirement
        if quality == QualityLevel.DRAFT:
            candidates = [m for m in candidates if m.cost_tier <= 1]
        elif quality == QualityLevel.STANDARD:
            candidates = [m for m in candidates if m.cost_tier <= 2]
        elif quality == QualityLevel.HIGH:
            candidates = [m for m in candidates if m.cost_tier >= 2]
        elif quality == QualityLevel.PREMIUM:
            candidates = [m for m in candidates if m.cost_tier >= 2]
        
        # For multi-image fusion (3+ images), prefer 4.5 for better quality
        if num_reference_images >= 3:
            candidates = [m for m in candidates if m.quality_score >= 9]
        
        # For urgent requests, prioritize speed
        if urgency == "asap":
            candidates.sort(key=lambda m: (-m.speed_score, m.cost_tier))
        else:
            # Balance quality and cost
            candidates.sort(key=lambda m: (m.quality_score / m.cost_tier), reverse=True)
        
        if not candidates:
            # Fallback to seedream-4.0 (always supports i2i)
            selected = IMAGE_MODELS["seedream-4.0"]
            model_key = "seedream-4.0"
        else:
            selected = candidates[0]
            # Find the key for this model
            model_key = next(
                k for k, v in IMAGE_MODELS.items() 
                if v.model_id == selected.model_id
            )
        
        # Build reasoning
        reasoning_parts = [f"Selected {selected.name} for image-to-image"]
        
        if num_reference_images > 1:
            reasoning_parts.append(f"fusion of {num_reference_images} images")
        
        if urgency == "asap":
            reasoning_parts.append(f"fastest i2i option ({selected.speed_score}/10 speed)")
        
        if quality == QualityLevel.PREMIUM:
            reasoning_parts.append("for maximum quality output")
        elif selected.cost_tier == 1:
            reasoning_parts.append("for cost efficiency")
        
        # Get alternatives (only I2I-capable)
        alternatives = [
            {
                "model": k,
                "cost": v.estimated_cost_usd,
                "quality": v.quality_score,
                "speed": v.speed_score,
            }
            for k, v in IMAGE_MODELS.items()
            if v.model_id != selected.model_id and v.supports_i2i
        ]
        
        return {
            "model_key": model_key,
            "model_id": selected.model_id,
            "name": selected.name,
            "reasoning": ", ".join(reasoning_parts),
            "estimated_cost_usd": selected.estimated_cost_usd,
            "quality_score": selected.quality_score,
            "speed_score": selected.speed_score,
            "cost_tier": selected.cost_tier,
            "supports_i2i": True,
            "alternatives": alternatives,
        }
    
    def select_video_model(
        self,
        content_type: ContentType = ContentType.VIDEO_LIFESTYLE,
        quality: QualityLevel = QualityLevel.STANDARD,
        platform: str = "tiktok",
        resolution: Optional[str] = None,
        duration: int = 5,
        urgency: str = "normal",
    ) -> Dict[str, Any]:
        """
        Select optimal video model and settings.
        
        Returns dict with model selection and optimal resolution.
        """
        # Auto-select resolution based on platform if not specified
        if not resolution:
            resolution = self._suggest_resolution(platform, quality)
        
        candidates = list(VIDEO_MODELS.values())
        
        # Filter by quality
        if quality == QualityLevel.DRAFT:
            candidates = [m for m in candidates if m.cost_tier <= 1]
        elif quality == QualityLevel.PREMIUM:
            candidates = [m for m in candidates if m.cost_tier >= 3]
        
        # Sort by criteria
        if urgency == "asap":
            candidates.sort(key=lambda m: (-m.speed_score, m.cost_tier))
        else:
            # For social content, balance is key
            candidates.sort(key=lambda m: (m.quality_score / m.cost_tier), reverse=True)
        
        if not candidates:
            selected = VIDEO_MODELS["seedance-1.0-lite"]
            model_key = "seedance-1.0-lite"
        else:
            selected = candidates[0]
            model_key = next(
                k for k, v in VIDEO_MODELS.items()
                if v.model_id == selected.model_id
            )
        
        # Calculate estimated cost
        res_multiplier = VIDEO_RESOLUTION_MULTIPLIERS.get(resolution, 1.0)
        dur_multiplier = get_duration_multiplier(duration)
        estimated_cost = selected.estimated_cost_usd * res_multiplier * dur_multiplier
        
        # Build reasoning
        reasoning_parts = [f"Selected {selected.name}"]
        reasoning_parts.append(f"at {resolution}")
        
        if quality == QualityLevel.DRAFT:
            reasoning_parts.append("for quick iteration")
        elif selected.cost_tier == 1:
            reasoning_parts.append("for cost-effective social content")
        
        if urgency == "asap":
            reasoning_parts.append(f"(fastest generation: {selected.speed_score}/10)")
        
        # Platform-specific advice
        platform_notes = {
            "tiktok": "720p is optimal for mobile viewing",
            "instagram": "1080p recommended for Reels",
            "youtube": "1080p or 2K for professional look",
            "linkedin": "1080p for professional presentations",
        }
        
        note = platform_notes.get(platform, "")
        
        # Get alternatives with cost comparison
        alternatives = []
        for k, v in VIDEO_MODELS.items():
            if v.model_id != selected.model_id:
                alt_cost = v.estimated_cost_usd * res_multiplier * dur_multiplier
                alternatives.append({
                    "model": k,
                    "resolution": resolution,
                    "estimated_cost": round(alt_cost, 3),
                    "quality": v.quality_score,
                    "speed": v.speed_score,
                })
        
        return {
            "model_key": model_key,
            "model_id": selected.model_id,
            "name": selected.name,
            "resolution": resolution,
            "duration": duration,
            "reasoning": ", ".join(reasoning_parts),
            "estimated_cost_usd": round(estimated_cost, 3),
            "quality_score": selected.quality_score,
            "speed_score": selected.speed_score,
            "platform_note": note,
            "cost_breakdown": {
                "base_cost": selected.estimated_cost_usd,
                "resolution_multiplier": res_multiplier,
                "duration_multiplier": round(dur_multiplier, 2),
            },
            "alternatives": alternatives,
        }
    
    def _suggest_resolution(self, platform: str, quality: QualityLevel) -> str:
        """Suggest optimal resolution for platform and quality."""
        suggestions = {
            ("tiktok", QualityLevel.DRAFT): "480p",
            ("tiktok", QualityLevel.STANDARD): "720p",
            ("tiktok", QualityLevel.HIGH): "1080p",
            ("instagram", QualityLevel.DRAFT): "720p",
            ("instagram", QualityLevel.STANDARD): "1080p",
            ("instagram", QualityLevel.HIGH): "1080p",
            ("youtube", QualityLevel.STANDARD): "1080p",
            ("youtube", QualityLevel.HIGH): "1080p",
            ("youtube", QualityLevel.PREMIUM): "2k",
            ("linkedin", QualityLevel.STANDARD): "1080p",
            ("linkedin", QualityLevel.HIGH): "1080p",
        }
        
        key = (platform, quality)
        if key in suggestions:
            return suggestions[key]
        
        # Default based on quality
        quality_map = {
            QualityLevel.DRAFT: "720p",
            QualityLevel.STANDARD: "1080p",
            QualityLevel.HIGH: "1080p",
            QualityLevel.PREMIUM: "2k",
        }
        return quality_map.get(quality, "1080p")
    
    def compare_all_options(
        self,
        asset_type: str = "image",  # "image" or "video"
        duration: int = 5,
    ) -> List[Dict[str, Any]]:
        """Return comparison of all available options."""
        if asset_type == "image":
            return [
                {
                    "model": k,
                    "name": v.name,
                    "cost_usd": v.estimated_cost_usd,
                    "quality": v.quality_score,
                    "speed": v.speed_score,
                    "best_for": v.best_for,
                }
                for k, v in IMAGE_MODELS.items()
            ]
        else:  # video
            results = []
            for res in ["480p", "720p", "1080p", "2k"]:
                for k, v in VIDEO_MODELS.items():
                    res_mult = VIDEO_RESOLUTION_MULTIPLIERS[res]
                    dur_mult = get_duration_multiplier(duration)
                    results.append({
                        "model": k,
                        "name": v.name,
                        "resolution": res,
                        "duration": duration,
                        "cost_usd": round(v.estimated_cost_usd * res_mult * dur_mult, 3),
                        "quality": v.quality_score,
                        "speed": v.speed_score,
                    })
            return results


# Convenience functions for quick selection

def select_for_social_post(
    platform: str = "instagram",
    post_type: str = "feed",  # "feed", "story", "reel"
    quality: str = "standard",  # "draft", "standard", "high"
) -> Dict[str, Any]:
    """Quick selector optimized for social media posts."""
    selector = ModelSelector()
    
    quality_enum = QualityLevel(quality)
    
    if post_type == "reel":
        return selector.select_video_model(
            platform=platform,
            quality=quality_enum,
            duration=5,
        )
    else:
        return selector.select_image_model(
            platform=platform,
            quality=quality_enum,
        )


def select_for_ad_campaign(
    platform: str = "facebook",
    campaign_type: str = "prospecting",  # "prospecting", "retargeting", "brand"
    budget_tier: str = "medium",  # "low", "medium", "high"
) -> Dict[str, Any]:
    """Selector optimized for ad campaigns."""
    selector = ModelSelector()
    
    # Map budget tier to quality
    budget_quality_map = {
        "low": QualityLevel.STANDARD,
        "medium": QualityLevel.HIGH,
        "high": QualityLevel.PREMIUM,
    }
    quality = budget_quality_map.get(budget_tier, QualityLevel.HIGH)
    
    # Prospectors need volume → faster/cheaper
    # Retargeting needs conversion → higher quality
    if campaign_type == "prospecting":
        return selector.select_image_model(
            quality=QualityLevel.STANDARD,
            platform=platform,
            urgency="normal",
        )
    else:
        return selector.select_image_model(
            quality=quality,
            platform=platform,
            urgency="normal",
        )


def get_cost_estimate(
    asset_type: str = "image",
    quantity: int = 1,
    video_resolution: str = "1080p",
    video_duration: int = 5,
) -> Dict[str, Any]:
    """Get cost estimate for batch generation."""
    selector = ModelSelector()
    
    if asset_type == "image":
        # Use standard recommendation
        selection = selector.select_image_model(quality=QualityLevel.STANDARD)
        unit_cost = selection["estimated_cost_usd"]
        
        return {
            "asset_type": "image",
            "quantity": quantity,
            "recommended_model": selection["model_key"],
            "unit_cost_usd": unit_cost,
            "total_cost_usd": round(unit_cost * quantity, 2),
            "alternatives": {
                "economy": round(IMAGE_MODELS["seedream-2.0-ultra"].estimated_cost_usd * quantity, 2),
                "premium": round(IMAGE_MODELS["seedream-5.0"].estimated_cost_usd * quantity, 2),
            },
        }
    else:
        # Video estimate
        selection = selector.select_video_model(
            resolution=video_resolution,
            duration=video_duration,
        )
        unit_cost = selection["estimated_cost_usd"]
        
        return {
            "asset_type": "video",
            "quantity": quantity,
            "resolution": video_resolution,
            "duration": video_duration,
            "recommended_model": selection["model_key"],
            "unit_cost_usd": unit_cost,
            "total_cost_usd": round(unit_cost * quantity, 2),
            "alternatives": {
                "480p": round(
                    VIDEO_MODELS["seedance-1.0-lite"].estimated_cost_usd * 
                    VIDEO_RESOLUTION_MULTIPLIERS["480p"] * 
                    get_duration_multiplier(video_duration) * quantity, 2
                ),
                "2k": round(
                    VIDEO_MODELS["seedance-1.0-pro"].estimated_cost_usd * 
                    VIDEO_RESOLUTION_MULTIPLIERS["2k"] * 
                    get_duration_multiplier(video_duration) * quantity, 2
                ),
            },
        }


if __name__ == "__main__":
    # Demo the selector
    print("🎯 Model Selector - Cost Optimization Demo")
    print("=" * 60)
    
    selector = ModelSelector()
    
    # Demo 1: Instagram post
    print("\n📱 Instagram Feed Post (Standard Quality):")
    result = selector.select_image_model(
        platform="instagram",
        quality=QualityLevel.STANDARD,
    )
    print(f"   Model: {result['name']}")
    print(f"   Cost: ${result['estimated_cost_usd']:.2f}")
    print(f"   Reasoning: {result['reasoning']}")
    
    # Demo 2: TikTok video
    print("\n🎵 TikTok Video (Standard Quality):")
    result = selector.select_video_model(
        platform="tiktok",
        quality=QualityLevel.STANDARD,
        duration=5,
    )
    print(f"   Model: {result['name']}")
    print(f"   Resolution: {result['resolution']}")
    print(f"   Cost: ${result['estimated_cost_usd']:.2f}")
    print(f"   Reasoning: {result['reasoning']}")
    
    # Demo 3: Quick draft
    print("\n⚡ Quick Draft (Low Cost):")
    result = selector.select_image_model(
        quality=QualityLevel.DRAFT,
        urgency="asap",
    )
    print(f"   Model: {result['name']}")
    print(f"   Cost: ${result['estimated_cost_usd']:.2f}")
    print(f"   Speed: {result['speed_score']}/10")
    
    # Demo 4: Batch cost estimate
    print("\n💰 Batch Cost Estimate (10 images):")
    estimate = get_cost_estimate(asset_type="image", quantity=10)
    print(f"   Recommended: {estimate['recommended_model']}")
    print(f"   Total: ${estimate['total_cost_usd']:.2f}")
    print(f"   Economy option: ${estimate['alternatives']['economy']:.2f}")
    print(f"   Premium option: ${estimate['alternatives']['premium']:.2f}")

#!/usr/bin/env python3
"""
BytePlus ModelArk API Client Wrapper (SDK Only)
Handles image and video generation using BytePlus SDK only.
"""

__version__ = "1.6.0"

import os
import json
import time
import base64
from typing import Optional, Dict, Any, List
from pathlib import Path

# SDK is required - no REST API fallback
from byteplussdkarkruntime import Ark


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json if it exists."""
    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def encode_image_to_base64(image_path: str) -> str:
    """Encode a local image file to base64 data URL."""
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    # Determine MIME type from extension
    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    mime_type = mime_types.get(ext, 'image/jpeg')
    
    b64_data = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{b64_data}"


class BytePlusClient:
    """Client for BytePlus ModelArk API - Image and Video Generation (SDK Only)"""
    
    # Base URLs
    BASE_URL_V3 = "https://ark.ap-southeast.bytepluses.com/api/v3"
    
    # Available models (from BytePlus API /models endpoint)
    IMAGE_MODELS = {
        "seedream-5.0": "seedream-5-0-260128",
        "seedream-4.5": "seedream-4-5-251128",
        "seedream-4.0": "seedream-4-0-250828",
        "seedream-3.0": "seedream-3-0-t2i-250415",
    }
    
    VIDEO_MODELS = {
        "seedance-1.5-pro": "seedance-1-5-pro-251215",
        "seedance-1.0-pro": "seedance-1-0-pro-250528",
        "seedance-1.0-pro-fast": "seedance-1-0-pro-fast-251015",
        "seedance-1.0-lite-t2v": "seedance-1-0-lite-t2v-250428",
        "seedance-1.0-lite-i2v": "seedance-1-0-lite-i2v-250428",
    }
    
    VIDEO_RESOLUTIONS = ["480p", "720p", "1080p", "2k"]
    VIDEO_ASPECT_RATIOS = ["16:9", "9:16", "1:1", "4:3"]
    VIDEO_DURATIONS = list(range(4, 16))  # 4-15 seconds
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize BytePlus client (SDK required).
        
        Args:
            api_key: BytePlus API key. If not provided, reads from config.json or ARK_API_KEY env var.
        
        Raises:
            ImportError: If byteplussdkarkruntime is not installed
            ValueError: If API key is not provided
        """
        # Get API key from: 1) parameter, 2) config.json, 3) env var
        self.api_key = api_key
        if not self.api_key:
            config = load_config()
            self.api_key = config.get("api_key")
        if not self.api_key:
            self.api_key = os.environ.get("ARK_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "API key required. Set in config.json, or use ARK_API_KEY environment variable.\n"
                "Get your key at: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey"
            )
        
        # Initialize SDK client
        try:
            self._client = Ark(
                base_url=self.BASE_URL_V3,
                api_key=self.api_key,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Ark client: {e}")
    
    def generate_image(
        self,
        prompt: str,
        model: str = "seedream-5.0",
        size: str = "2K",
        quality: str = "standard",
        response_format: str = "url",
        watermark: bool = False,
        n: int = 1,
    ) -> Dict[str, Any]:
        """
        Generate images using Seedream models (SDK only).
        
        Args:
            prompt: Text description of the desired image
            model: Model identifier (seedream-5.0, seedream-4.0, seedream-3.0)
            size: Image size (e.g., "1024x1024", "2K", "1080p")
            quality: "standard" or "hd"
            response_format: "url" or "b64_json"
            watermark: Whether to add watermark
            n: Number of images to generate (1-4)
            
        Returns:
            Dict containing generation results with 'url' or 'base64' key
        """
        model_id = self.IMAGE_MODELS.get(model, model)
        
        try:
            # Aligned with SDK sample code
            response = self._client.images.generate(
                model=model_id,
                prompt=prompt,
                size=size,
                sequential_image_generation="disabled",
                response_format=response_format,
                stream=False,
                watermark=False,
            )
            
            results = []
            for item in response.data:
                result = {"prompt": prompt, "model": model}
                if response_format == "url":
                    result["url"] = item.url
                else:
                    result["base64"] = item.b64_json
                results.append(result)
            
            return {
                "success": True,
                "count": len(results),
                "images": results,
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt,
                "model": model,
            }
    
    def generate_image_i2i(
        self,
        prompt: str,
        reference_images: List[str],
        model: str = "seedream-4.0",
        size: str = "2K",
        mode: str = "single",
        n: int = 1,
    ) -> Dict[str, Any]:
        """
        Generate images using Image-to-Image (SDK only).
        
        Uses Seedream 4.0 or 4.5 which support I2I generation.
        Reference images can be URLs or local file paths.
        
        Args:
            prompt: Text description of desired output
            reference_images: List of image URLs or local file paths (1-10 images)
            model: Model to use (seedream-4.0 or seedream-4.5)
            size: Output image size
            mode: Generation mode (single, fusion, style_transfer, edit, subject_preservation, image_set)
            n: Number of images to generate
            
        Returns:
            Dict containing generation results
        """
        # Validate model
        if model not in ["seedream-4.0", "seedream-4.5"]:
            return {
                "success": False,
                "error": f"Model '{model}' does not support image-to-image. Use 'seedream-4.0' or 'seedream-4.5'",
                "supported_models": ["seedream-4.0", "seedream-4.5"],
            }
        
        if not reference_images:
            return {
                "success": False,
                "error": "At least one reference image is required for image-to-image generation",
            }
        
        if len(reference_images) > 10:
            return {
                "success": False,
                "error": f"Too many reference images. Maximum is 10, got {len(reference_images)}",
            }
        
        model_id = self.IMAGE_MODELS.get(model, model)
        
        try:
            # Process reference images - convert local files to base64 URLs
            processed_images = []
            for img_path in reference_images:
                if img_path.startswith(('http://', 'https://', 'data:')):
                    # Already a URL or data URL
                    processed_images.append(img_path)
                elif os.path.exists(img_path):
                    # Local file - convert to base64
                    processed_images.append(encode_image_to_base64(img_path))
                else:
                    return {
                        "success": False,
                        "error": f"Reference image not found: {img_path}",
                    }
            
            # Determine sequential mode based on generation mode
            sequential_mode = "auto" if mode == "image_set" else "disabled"
            
            # Build extended prompt with mode instruction
            extended_prompt = prompt
            if mode == "style_transfer":
                extended_prompt = f"Apply the style from the reference image to: {prompt}"
            elif mode == "edit":
                extended_prompt = f"Edit the reference image: {prompt}"
            elif mode == "fusion":
                extended_prompt = f"Combine the reference images: {prompt}"
            
            # Call API with image parameter for I2I (aligned with SDK sample)
            # For single image, use 'image' parameter directly
            # For multiple images (fusion), use 'image_urls' in extra_body
            if len(processed_images) == 1:
                response = self._client.images.generate(
                    model=model_id,
                    prompt=extended_prompt,
                    image=processed_images[0],
                    sequential_image_generation=sequential_mode,
                    response_format="url",
                    size=size,
                    stream=False,
                    watermark=False,
                )
            else:
                # Multiple images - use extra_body for image_urls
                response = self._client.images.generate(
                    model=model_id,
                    prompt=extended_prompt,
                    size=size,
                    sequential_image_generation=sequential_mode,
                    response_format="url",
                    stream=False,
                    watermark=False,
                    extra_body={
                        "image_urls": processed_images,
                    }
                )
            
            results = []
            for item in response.data:
                results.append({
                    "prompt": prompt,
                    "model": model,
                    "url": item.url,
                })
            
            return {
                "success": True,
                "count": len(results),
                "images": results,
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Image-to-image generation failed: {str(e)}",
                "prompt": prompt,
                "model": model,
            }
    
    def generate_video(
        self,
        prompt: str,
        model: str = "seedance-1.5-pro",
        duration: int = 5,
        resolution: Optional[str] = None,
        ratio: Optional[str] = None,
        generate_audio: bool = True,
        watermark: bool = False,
        camera_fixed: Optional[bool] = None,
        seed: Optional[int] = None,
        reference_images: Optional[List[str]] = None,
        poll_interval: int = 1,
        max_polls: int = 300,
    ) -> Dict[str, Any]:
        """
        Generate videos using Seedance models via SDK (async job pattern).
        Aligned with BytePlus official API documentation.
        
        Args:
            prompt: Text description of the desired video
            model: Model identifier (seedance-1.5-pro, seedance-1.0-pro, etc.)
            duration: Video duration in seconds (5-10 for most models)
            resolution: Output resolution (480p, 720p, 1080p, 2k)
            ratio: Aspect ratio (adaptive, 16:9, 9:16, 1:1, 4:3)
            generate_audio: Whether to generate audio for the video
            watermark: Whether to include watermark
            camera_fixed: Whether to fix camera position
            seed: Random seed for reproducibility
            reference_images: Optional list of image file paths or URLs for image-to-video
            poll_interval: Seconds between status checks (default: 1 for faster updates)
            max_polls: Maximum number of status checks (default: 300 for 5 min timeout)
            
        Returns:
            Dict containing generation results with 'video_url', 'status', etc.
        """
        model_id = self.VIDEO_MODELS.get(model, model)
        
        # Validate duration
        if duration not in self.VIDEO_DURATIONS:
            return {
                "success": False,
                "error": f"Invalid duration: {duration}. Must be one of {self.VIDEO_DURATIONS}"
            }
        
        # Validate resolution if provided
        if resolution and resolution not in self.VIDEO_RESOLUTIONS:
            return {
                "success": False,
                "error": f"Invalid resolution: {resolution}. Must be one of {self.VIDEO_RESOLUTIONS}"
            }
        
        # Validate ratio if provided
        valid_ratios = ["adaptive", "16:9", "9:16", "1:1", "4:3"]
        if ratio and ratio not in valid_ratios:
            return {
                "success": False,
                "error": f"Invalid ratio: {ratio}. Must be one of {valid_ratios}"
            }
        
        try:
            # Build content array for the request (just the prompt text)
            content = [{"type": "text", "text": prompt}]
            
            # Add reference images if provided (convert local files to base64)
            if reference_images:
                for img_path in reference_images:
                    if img_path.startswith(('http://', 'https://', 'data:')):
                        # URL provided directly
                        content.append({
                            "type": "image_url",
                            "image_url": {"url": img_path}
                        })
                    elif os.path.exists(img_path):
                        # Local file - convert to base64 data URL
                        data_url = encode_image_to_base64(img_path)
                        content.append({
                            "type": "image_url",
                            "image_url": {"url": data_url}
                        })
                    else:
                        return {
                            "success": False,
                            "error": f"Reference image not found: {img_path}"
                        }
            
            # Build API parameters (aligned with official documentation)
            api_params = {
                "model": model_id,
                "content": content,
                "duration": duration,
                "generate_audio": generate_audio,
                "watermark": watermark,
            }
            
            # Add optional parameters if provided
            if resolution:
                api_params["resolution"] = resolution
            if ratio:
                api_params["ratio"] = ratio
            if camera_fixed is not None:
                api_params["camera_fixed"] = camera_fixed
            if seed is not None:
                api_params["seed"] = seed
            
            # Create task
            print(f"  Submitting video generation task...")
            print(f"  Model: {model_id}")
            print(f"  Duration: {duration}s")
            if resolution:
                print(f"  Resolution: {resolution}")
            if ratio:
                print(f"  Ratio: {ratio}")
            
            task = self._client.content_generation.tasks.create(**api_params)
            
            task_id = task.id
            print(f"  Task ID: {task_id}")
            
            # Poll for completion
            for poll_count in range(max_polls):
                time.sleep(poll_interval)
                
                status_result = self._client.content_generation.tasks.get(task_id=task_id)
                status = status_result.status
                
                if status == "succeeded":
                    video_url = status_result.content.get("video_url") if status_result.content else None
                    return {
                        "success": True,
                        "job_id": task_id,
                        "status": status,
                        "video_url": video_url,
                        "duration": getattr(status_result, "duration", duration),
                        "resolution": getattr(status_result, "resolution", resolution),
                        "framespersecond": getattr(status_result, "framespersecond", 24),
                        "usage": {
                            "completion_tokens": getattr(status_result.usage, "completion_tokens", 0) if status_result.usage else 0,
                            "total_tokens": getattr(status_result.usage, "total_tokens", 0) if status_result.usage else 0,
                        },
                        "prompt": prompt,
                        "model": model,
                    }
                
                elif status == "failed":
                    return {
                        "success": False,
                        "error": "Video generation failed",
                        "prompt": prompt,
                        "model": model,
                    }
                
                # Still processing
                if poll_count % 6 == 0:  # Print every ~30 seconds
                    print(f"  Video generation in progress... ({(poll_count + 1) * poll_interval}s)")
            
            # Timeout
            return {
                "success": False,
                "job_id": task_id,
                "status": "timeout",
                "error": f"Generation timed out after {max_polls * poll_interval} seconds",
                "prompt": prompt,
                "model": model,
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Video generation failed: {str(e)}",
                "prompt": prompt,
                "model": model_id,
            }

    def get_video_status(self, job_id: str) -> Dict[str, Any]:
        """Check status of a video generation job."""
        try:
            result = self._client.content_generation.tasks.get(task_id=job_id)
            return {
                "success": True,
                "status": result.status,
                "content": result.to_dict() if hasattr(result, 'to_dict') else str(result),
            }
        except Exception as e:
            return {"error": str(e)}
    
    def edit_image(
        self,
        prompt: str,
        image_path: str,
        model: str = "seedream-4.0",
        size: str = "2K",
    ) -> Dict[str, Any]:
        """Edit an image - add, remove, or modify elements."""
        return self.generate_image_i2i(
            prompt=prompt,
            reference_images=[image_path],
            model=model,
            size=size,
            mode="edit",
            n=1,
        )
    
    def style_transfer(
        self,
        content_prompt: str,
        style_image: str,
        model: str = "seedream-4.0",
        size: str = "2K",
    ) -> Dict[str, Any]:
        """Transfer style from reference image to new content."""
        return self.generate_image_i2i(
            prompt=content_prompt,
            reference_images=[style_image],
            model=model,
            size=size,
            mode="style_transfer",
            n=1,
        )
    
    def generate_variations(
        self,
        reference_image: str,
        prompt: str = "Generate variations of this image with different angles and lighting",
        model: str = "seedream-4.0",
        n: int = 4,
        size: str = "2K",
    ) -> Dict[str, Any]:
        """Generate variations of a reference image while preserving the subject."""
        if n > 14:
            return {
                "success": False,
                "error": "Maximum 14 variations allowed",
            }
        
        return self.generate_image_i2i(
            prompt=prompt,
            reference_images=[reference_image],
            model=model,
            size=size,
            mode="image_set" if n > 1 else "single",
            n=n,
        )
    
    def fuse_images(
        self,
        images: List[str],
        prompt: str,
        model: str = "seedream-4.0",
        size: str = "2K",
    ) -> Dict[str, Any]:
        """Fuse multiple images into a single cohesive image."""
        if len(images) < 2:
            return {
                "success": False,
                "error": "At least 2 images required for fusion",
            }
        
        return self.generate_image_i2i(
            prompt=prompt,
            reference_images=images,
            model=model,
            size=size,
            mode="fusion",
            n=1,
        )


# Convenience functions for direct use
def generate_marketing_image(
    prompt: str,
    platform: str = "instagram",
    style: str = "cinematic",
    model: str = "auto",
    quality: str = "standard",
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a marketing image optimized for a specific platform.
    """
    try:
        from model_selector import ModelSelector, QualityLevel
        HAS_SELECTOR = True
    except ImportError:
        HAS_SELECTOR = False
    
    # Platform-specific optimizations
    platform_prompts = {
        "instagram": "Instagram-optimized square format, social media aesthetic, engaging visual",
        "tiktok": "Vertical 9:16 format, mobile-first, bold and eye-catching, short-form content style",
        "linkedin": "Professional corporate aesthetic, clean and polished, business-appropriate",
        "twitter": "Wide format optimized for feeds, attention-grabbing thumbnail style",
        "youtube": "16:9 thumbnail style, high contrast, click-optimized, vibrant colors",
    }
    
    style_prompts = {
        "cinematic": "cinematic lighting, film grain, professional color grading, movie poster aesthetic",
        "product": "product photography, clean background, soft shadows, commercial advertising style",
        "lifestyle": "authentic lifestyle shot, natural lighting, relatable scene, real-world setting",
        "minimal": "minimalist composition, clean lines, negative space, modern aesthetic",
    }
    
    # Build enhanced prompt
    enhanced_prompt = prompt
    if style in style_prompts:
        enhanced_prompt += f", {style_prompts[style]}"
    if platform in platform_prompts:
        enhanced_prompt += f", {platform_prompts[platform]}"
    
    # Platform-specific sizes
    size_map = {
        "instagram": "1024x1024",
        "tiktok": "1080x1920",
        "linkedin": "1200x627",
        "twitter": "1200x675",
        "youtube": "1280x720",
    }
    
    size = kwargs.pop("size", size_map.get(platform, "1024x1024"))
    
    # Auto-select model if needed
    if model == "auto":
        if HAS_SELECTOR:
            selector = ModelSelector()
            quality_enum = QualityLevel(quality)
            selection = selector.select_image_model(
                quality=quality_enum,
                platform=platform,
            )
            model = selection["model_key"]
        else:
            model = "seedream-5.0"
    
    client = BytePlusClient()
    return client.generate_image(
        prompt=enhanced_prompt,
        model=model,
        size=size,
        **kwargs
    )


def generate_marketing_image_i2i(
    prompt: str,
    reference_images: List[str],
    mode: str = "single",
    platform: str = "instagram",
    style: str = "cinematic",
    model: str = "auto",
    quality: str = "standard",
    **kwargs
) -> Dict[str, Any]:
    """
    Generate marketing image using image-to-image (reference-based generation).
    """
    # Platform-specific sizes
    size_map = {
        "instagram": "1024x1024",
        "tiktok": "1080x1920",
        "linkedin": "1200x627",
        "twitter": "1200x675",
        "youtube": "1280x720",
    }
    
    # Style enhancements
    style_prompts = {
        "cinematic": "cinematic lighting, film grain, professional color grading",
        "product": "product photography, clean background, soft shadows",
        "lifestyle": "authentic lifestyle shot, natural lighting",
        "minimal": "minimalist composition, clean lines, negative space",
    }
    
    enhanced_prompt = prompt
    if style in style_prompts:
        enhanced_prompt += f", {style_prompts[style]}"
    
    size = kwargs.pop("size", size_map.get(platform, "1024x1024"))
    
    # Auto-select model if needed
    if model == "auto":
        try:
            from model_selector import ModelSelector, QualityLevel
            selector = ModelSelector()
            quality_enum = QualityLevel(quality)
            
            if len(reference_images) > 3:
                model = "seedream-4.5"  # Better for complex fusion
            else:
                model = "seedream-4.0"
        except ImportError:
            model = "seedream-4.0"
    
    client = BytePlusClient()
    return client.generate_image_i2i(
        prompt=enhanced_prompt,
        reference_images=reference_images,
        model=model,
        mode=mode,
        size=size,
        **kwargs
    )


def generate_marketing_video(
    prompt: str,
    platform: str = "tiktok",
    duration: int = 5,
    model: str = "seedance-1.5-pro",
    resolution: Optional[str] = None,
    generate_audio: bool = True,
    reference_images: Optional[List[str]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a marketing video optimized for a specific platform.
    
    Args:
        prompt: Text description of the desired video
        platform: Target platform (tiktok, instagram, youtube, linkedin)
        duration: Video duration in seconds (5-10)
        model: Model identifier (seedance-1.5-pro, seedance-1.0-pro)
        resolution: Output resolution (480p, 720p, 1080p, 2k)
        generate_audio: Whether to generate audio for the video
        reference_images: Optional list of image URLs for image-to-video
        **kwargs: Additional parameters (watermark, seed, camera_fixed, etc.)
    """
    # Platform-specific enhancements (added to prompt)
    platform_prompts = {
        "tiktok": "fast-paced, engaging hook in first second, vertical format, mobile-optimized",
        "instagram": "polished aesthetic, smooth transitions, vertical format, Reels-optimized",
        "youtube": "professional quality, clear narrative, horizontal format, cinematic pacing",
        "linkedin": "corporate professional, clean graphics, horizontal format, business-appropriate",
    }
    
    # Platform-specific aspect ratios
    platform_ratios = {
        "tiktok": "9:16",
        "instagram": "9:16",
        "youtube": "16:9",
        "linkedin": "16:9",
    }
    
    enhanced_prompt = prompt
    if platform in platform_prompts:
        enhanced_prompt += f", {platform_prompts[platform]}"
    
    # Get ratio from kwargs or use platform default
    ratio = kwargs.pop("ratio", None) or platform_ratios.get(platform, "16:9")
    
    client = BytePlusClient()
    return client.generate_video(
        prompt=enhanced_prompt,
        duration=duration,
        model=model,
        resolution=resolution,
        ratio=ratio,
        generate_audio=generate_audio,
        reference_images=reference_images,
        **kwargs
    )


if __name__ == "__main__":
    # Test the client (SDK required)
    print("BytePlus Marketing Creator Client (SDK Only)")
    print("=" * 50)
    
    # Check API key
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("\nError: ARK_API_KEY not set!")
        print("Get your API key at: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey")
        exit(1)
    
    print(f"\nAPI Key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        client = BytePlusClient()
        print("✅ Client initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        exit(1)
    
    print("\nAvailable Image Models:")
    for name, model_id in BytePlusClient.IMAGE_MODELS.items():
        print(f"  - {name}: {model_id}")
    
    print("\nAvailable Video Models:")
    for name, model_id in BytePlusClient.VIDEO_MODELS.items():
        print(f"  - {name}: {model_id}")

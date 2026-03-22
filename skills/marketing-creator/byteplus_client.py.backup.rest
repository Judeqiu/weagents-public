#!/usr/bin/env python3
"""
BytePlus ModelArk API Client Wrapper
Handles image and video generation with proper error handling and retry logic.
"""

__version__ = "1.5.0"

import os
import json
import time
import base64
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path

try:
    from byteplussdkarkruntime import Ark
    SDK_AVAILABLE = True
except ImportError:
    Ark = None
    SDK_AVAILABLE = False
    print("Warning: byteplussdkarkruntime not installed. Video generation requires SDK.")


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


class BytePlusClient:
    """Client for BytePlus ModelArk API - Image and Video Generation"""
    
    # Base URLs
    BASE_URL_V3 = "https://ark.ap-southeast.bytepluses.com/api/v3"
    SEEDANCE_BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"
    
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
        Initialize BytePlus client.
        
        Args:
            api_key: BytePlus API key. If not provided, reads from config.json or ARK_API_KEY env var.
        """
        # Try to get API key from: 1) parameter, 2) config.json, 3) env var
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
        
        # Initialize image generation client (if SDK available)
        self._image_client = None
        if Ark:
            try:
                self._image_client = Ark(
                    base_url=self.BASE_URL_V3,
                    api_key=self.api_key,
                )
            except Exception as e:
                print(f"Warning: Failed to initialize Ark client: {e}")
    
    def generate_image(
        self,
        prompt: str,
        model: str = "seedream-5.0",
        size: str = "2K",
        quality: str = "standard",
        response_format: str = "url",
        watermark: bool = False,
        n: int = 1,
        timeout: int = 120,
        image_urls: Optional[List[str]] = None,
        sequential_image_generation: str = "disabled",
    ) -> Dict[str, Any]:
        """
        Generate images using Seedream models.
        
        Args:
            prompt: Text description of the desired image
            model: Model identifier (seedream-5.0, seedream-4.0, seedream-3.0, seedream-2.0)
            size: Image size (e.g., "1024x1024", "2K", "1080p")
            quality: "standard" or "hd"
            response_format: "url" or "b64_json"
            watermark: Whether to add watermark
            n: Number of images to generate (1-4)
            timeout: Request timeout in seconds
            image_urls: List of reference image URLs for image-to-image generation (Seedream 4.0/4.5)
            sequential_image_generation: "disabled" (single image) or "auto" (image set generation)
            
        Returns:
            Dict containing generation results with 'url' or 'base64' key
        """
        model_id = self.IMAGE_MODELS.get(model, model)
        
        if not self._image_client:
            # Fallback to REST API if SDK not available
            return self._generate_image_rest(
                prompt, model_id, size, quality, response_format, watermark, n, timeout,
                image_urls, sequential_image_generation
            )
        
        try:
            response = self._image_client.images.generate(
                model=model_id,
                prompt=prompt,
                size=size,
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
    
    def _generate_image_rest(
        self,
        prompt: str,
        model_id: str,
        size: str,
        quality: str,
        response_format: str,
        watermark: bool,
        n: int,
        timeout: int,
        image_urls: Optional[List[str]] = None,
        sequential_image_generation: str = "disabled",
    ) -> Dict[str, Any]:
        """Fallback image generation using REST API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": model_id,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "response_format": response_format,
            "watermark": watermark,
            "n": n,
        }
        
        # Add image-to-image parameters if reference images provided
        if image_urls:
            payload["image_urls"] = image_urls
            payload["sequential_image_generation"] = sequential_image_generation
        
        try:
            response = requests.post(
                f"{self.BASE_URL_V3}/images/generations",
                headers=headers,
                json=payload,
                timeout=timeout,
            )
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("data", []):
                result = {"prompt": prompt, "model": model_id}
                if response_format == "url":
                    result["url"] = item.get("url")
                else:
                    result["base64"] = item.get("b64_json")
                results.append(result)
            
            return {
                "success": True,
                "count": len(results),
                "images": results,
            }
            
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            if "404" in error_msg or "Not Found" in error_msg:
                error_msg = (
                    f"Model '{model_id}' not found or not activated. "
                    f"Please activate the model in BytePlus console: "
                    f"https://console.byteplus.com/ark/ → Model activation → Media"
                )
            return {
                "success": False,
                "error": error_msg,
                "prompt": prompt,
                "model": model_id,
                "hint": "Models must be activated separately from API key. See: https://console.byteplus.com/ark/ → Model activation",
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API request failed: {str(e)}",
                "prompt": prompt,
                "model": model_id,
            }

    # Image-to-Image Generation Methods
    
    def generate_image_to_image(
        self,
        prompt: str,
        reference_images: List[str],
        model: str = "auto",
        size: str = "2K",
        mode: str = "single",
        n: int = 1,
        quality: str = "standard",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate images using reference images (Image-to-Image).
        
        Supports multiple generation modes:
        - single: Generate 1 image from 1 reference image
        - fusion: Fuse 2-10 reference images into 1 output
        - style_transfer: Apply style from reference to new content
        - edit: Modify elements in the reference image
        - subject_preservation: Keep subject consistent across variations
        - image_set: Generate a set of related images (up to 14 images)
        
        Args:
            prompt: Text description of desired output
            reference_images: List of image URLs or file paths (1-10 images)
            model: Model to use ("auto" to auto-select, or "seedream-4.0"/"seedream-4.5")
            size: Output image size
            mode: Generation mode - "single", "fusion", "style_transfer", "edit", 
                  "subject_preservation", or "image_set"
            n: Number of images to generate (for image_set mode, max 14)
            quality: Quality level for auto-selection (draft, standard, high, premium)
            **kwargs: Additional parameters passed to generate_image()
            
        Returns:
            Dict containing generation results
        """
        # Auto-select model if needed
        if model == "auto":
            try:
                from model_selector import ModelSelector, QualityLevel
                selector = ModelSelector()
                quality_enum = QualityLevel(quality)
                
                selection = selector.select_i2i_model(
                    quality=quality_enum,
                    num_reference_images=len(reference_images),
                )
                model = selection["model_key"]
            except ImportError:
                # Fallback without selector
                model = "seedream-4.0"
        
        # Validate model support for image-to-image
        if model not in ["seedream-4.0", "seedream-4.5"]:
            return {
                "success": False,
                "error": f"Model '{model}' does not support image-to-image. Use 'seedream-4.0' or 'seedream-4.5'",
                "supported_models": ["seedream-4.0", "seedream-4.5"],
            }
        
        # Validate reference images count
        if not reference_images:
            return {
                "success": False,
                "error": "At least one reference image is required for image-to-image generation",
            }
        
        max_images = 10
        if len(reference_images) > max_images:
            return {
                "success": False,
                "error": f"Too many reference images. Maximum is {max_images}, got {len(reference_images)}",
            }
        
        # Determine sequential_image_generation setting based on mode
        sequential_mode = "auto" if mode == "image_set" else "disabled"
        
        # Adjust n for image_set mode
        if mode == "image_set":
            total_items = len(reference_images) + n
            if total_items > 15:
                return {
                    "success": False,
                    "error": f"Total items (reference images + output images) cannot exceed 15. Got {total_items}",
                }
        
        return self.generate_image(
            prompt=prompt,
            model=model,
            size=size,
            n=n,
            image_urls=reference_images,
            sequential_image_generation=sequential_mode,
            **kwargs
        )
    
    def edit_image(
        self,
        prompt: str,
        image_path: str,
        model: str = "seedream-4.0",
        size: str = "2K",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Edit an image - add, remove, or modify elements.
        
        Args:
            prompt: Edit instruction (e.g., "Remove the background", "Change the color to red")
            image_path: Path or URL to the image to edit
            model: Model to use
            size: Output size
            **kwargs: Additional parameters
            
        Returns:
            Dict containing edited image
        """
        return self.generate_image_to_image(
            prompt=prompt,
            reference_images=[image_path],
            model=model,
            size=size,
            mode="edit",
            n=1,
            **kwargs
        )
    
    def style_transfer(
        self,
        content_prompt: str,
        style_image: str,
        model: str = "seedream-4.0",
        size: str = "2K",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transfer style from reference image to new content.
        
        Args:
            content_prompt: Description of content to generate
            style_image: URL or path to style reference image
            model: Model to use
            size: Output size
            **kwargs: Additional parameters
            
        Returns:
            Dict containing styled image
        """
        prompt = f"Refer to this image, keep the content unchanged, and apply its style to: {content_prompt}"
        return self.generate_image_to_image(
            prompt=prompt,
            reference_images=[style_image],
            model=model,
            size=size,
            mode="style_transfer",
            n=1,
            **kwargs
        )
    
    def generate_variations(
        self,
        reference_image: str,
        prompt: str = "Generate variations of this image with different angles and lighting",
        model: str = "seedream-4.0",
        n: int = 4,
        size: str = "2K",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate variations of a reference image while preserving the subject.
        
        Args:
            reference_image: URL or path to reference image
            prompt: Description of variations to create
            model: Model to use
            n: Number of variations (1-14)
            size: Output size
            **kwargs: Additional parameters
            
        Returns:
            Dict containing generated variations
        """
        if n > 14:
            return {
                "success": False,
                "error": "Maximum 14 variations allowed",
            }
        
        return self.generate_image_to_image(
            prompt=prompt,
            reference_images=[reference_image],
            model=model,
            size=size,
            mode="image_set" if n > 1 else "single",
            n=n,
            **kwargs
        )
    
    def fuse_images(
        self,
        images: List[str],
        prompt: str,
        model: str = "seedream-4.0",
        size: str = "2K",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Fuse multiple images into a single cohesive image.
        
        Args:
            images: List of 2-10 image URLs/paths to fuse
            prompt: Description of how to combine the images
            model: Model to use
            size: Output size
            **kwargs: Additional parameters
            
        Returns:
            Dict containing fused image
        """
        if len(images) < 2:
            return {
                "success": False,
                "error": "At least 2 images required for fusion",
            }
        
        return self.generate_image_to_image(
            prompt=prompt,
            reference_images=images,
            model=model,
            size=size,
            mode="fusion",
            n=1,
            **kwargs
        )
    
    def generate_video(
        self,
        prompt: str,
        model: str = "seedance-1.0-pro",
        resolution: str = "1080p",
        duration: int = 5,
        aspect_ratio: str = "16:9",
        audio: bool = True,
        reference_images: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
        style: Optional[str] = None,
        seed: Optional[int] = None,
        poll_interval: int = 5,
        max_polls: int = 60,
    ) -> Dict[str, Any]:
        """
        Generate videos using Seedance models via SDK (async job pattern).
        
        Args:
            prompt: Text description of the desired video
            model: Model identifier (seedance-1.0-pro, seedance-1.0-lite)
            resolution: Output resolution (480p, 720p, 1080p, 2k)
            duration: Video duration in seconds (4-15)
            aspect_ratio: Frame aspect ratio (16:9, 9:16, 1:1, 4:3)
            audio: Enable native audio generation
            reference_images: Optional list of image file paths for image-to-video
            negative_prompt: Elements to exclude from generation
            style: Visual style preset (cinematic, anime, realistic, 3d_render)
            seed: Reproducibility seed
            poll_interval: Seconds between status checks
            max_polls: Maximum number of status checks
            
        Returns:
            Dict containing generation results with 'video_url', 'status', etc.
        """
        if not SDK_AVAILABLE:
            return {
                "success": False,
                "error": "Video generation requires byteplus-python-sdk-v2. Install with: pip install byteplus-python-sdk-v2 pydantic",
                "prompt": prompt,
                "model": model,
            }
        
        model_id = self.VIDEO_MODELS.get(model, model)
        
        # Validate parameters
        if resolution not in self.VIDEO_RESOLUTIONS:
            return {
                "success": False,
                "error": f"Invalid resolution: {resolution}. Must be one of {self.VIDEO_RESOLUTIONS}"
            }
        
        if aspect_ratio not in self.VIDEO_ASPECT_RATIOS:
            return {
                "success": False,
                "error": f"Invalid aspect_ratio: {aspect_ratio}. Must be one of {self.VIDEO_ASPECT_RATIOS}"
            }
        
        if duration not in self.VIDEO_DURATIONS:
            return {
                "success": False,
                "error": f"Invalid duration: {duration}. Must be between 4-15 seconds"
            }
        
        try:
            # Use SDK for video generation
            client = Ark(
                base_url=self.BASE_URL_V3,
                api_key=self.api_key,
            )
            
            # Build content
            content = [{"type": "text", "text": prompt}]
            
            # Add reference images if provided
            if reference_images:
                for img_path in reference_images:
                    if not os.path.exists(img_path):
                        return {
                            "success": False,
                            "error": f"Reference image not found: {img_path}"
                        }
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"file://{img_path}"}
                    })
            
            # Create task
            print(f"  Submitting video generation task...")
            task = client.content_generation.tasks.create(
                model=model_id,
                content=content,
            )
            
            task_id = task.id
            print(f"  Task ID: {task_id}")
            
            # Poll for completion
            for poll_count in range(max_polls):
                time.sleep(poll_interval)
                
                status_result = client.content_generation.tasks.get(task_id=task_id)
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
        if not SDK_AVAILABLE:
            return {"error": "SDK not available"}
        
        try:
            client = Ark(
                base_url=self.BASE_URL_V3,
                api_key=self.api_key,
            )
            result = client.content_generation.tasks.get(task_id=job_id)
            return {
                "success": True,
                "status": result.status,
                "content": result.to_dict() if hasattr(result, 'to_dict') else str(result),
            }
        except Exception as e:
            return {"error": str(e)}


# Convenience functions for direct use
def generate_marketing_image(
    prompt: str,
    platform: str = "instagram",  # instagram, tiktok, linkedin, twitter, youtube
    style: str = "cinematic",     # cinematic, product, lifestyle, minimal
    model: str = "auto",          # "auto" to auto-select, or specific model name
    quality: str = "standard",    # draft, standard, high, premium
    image_urls: Optional[List[str]] = None,  # If provided, uses image-to-image
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a marketing image optimized for a specific platform.
    
    Automatically selects the right model based on:
    - If image_urls provided: uses seedream-4.0/4.5 (image-to-image capable)
    - If text-to-image: uses seedream-5.0 or quality-appropriate model
    
    Args:
        prompt: Base description of the image
        platform: Target platform for size/aspect optimization
        style: Visual style preset
        model: Model to use ("auto" for auto-selection)
        quality: Quality level for auto-selection
        image_urls: Optional reference images for image-to-image generation
        **kwargs: Additional arguments passed to generate_image()
    """
    # Import here to avoid circular dependency issues
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
    
    client = BytePlusClient()
    
    # Auto-select model if needed
    if model == "auto":
        if HAS_SELECTOR:
            selector = ModelSelector()
            quality_enum = QualityLevel(quality)
            
            if image_urls:
                # Use image-to-image model selection
                selection = selector.select_i2i_model(
                    quality=quality_enum,
                    platform=platform,
                    num_reference_images=len(image_urls),
                )
                model = selection["model_key"]
            else:
                # Use standard image model selection
                selection = selector.select_image_model(
                    quality=quality_enum,
                    platform=platform,
                )
                model = selection["model_key"]
        else:
            # Fallback without selector
            model = "seedream-4.0" if image_urls else "seedream-5.0"
    
    # Generate with appropriate method
    if image_urls:
        return client.generate_image_to_image(
            prompt=enhanced_prompt,
            reference_images=image_urls,
            model=model,
            size=size,
            **kwargs
        )
    else:
        return client.generate_image(
            prompt=enhanced_prompt,
            model=model,
            size=size,
            **kwargs
        )


def generate_marketing_video(
    prompt: str,
    platform: str = "tiktok",      # tiktok, instagram, youtube, linkedin
    duration: int = 5,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a marketing video optimized for a specific platform.
    
    Args:
        prompt: Base description of the video
        platform: Target platform for aspect ratio optimization
        duration: Video length in seconds
        **kwargs: Additional arguments passed to generate_video()
    """
    # Platform-specific aspect ratios
    aspect_map = {
        "tiktok": "9:16",
        "instagram": "9:16",
        "youtube": "16:9",
        "linkedin": "16:9",
    }
    
    # Platform-specific enhancements
    platform_prompts = {
        "tiktok": "fast-paced, engaging hook in first second, vertical format, mobile-optimized",
        "instagram": "polished aesthetic, smooth transitions, vertical format, Reels-optimized",
        "youtube": "professional quality, clear narrative, horizontal format, cinematic pacing",
        "linkedin": "corporate professional, clean graphics, horizontal format, business-appropriate",
    }
    
    enhanced_prompt = prompt
    if platform in platform_prompts:
        enhanced_prompt += f", {platform_prompts[platform]}"
    
    aspect_ratio = kwargs.pop("aspect_ratio", aspect_map.get(platform, "16:9"))
    
    client = BytePlusClient()
    return client.generate_video(
        prompt=enhanced_prompt,
        aspect_ratio=aspect_ratio,
        duration=duration,
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
    
    Automatically selects seedream-4.0 or seedream-4.5 based on quality and requirements.
    
    Args:
        prompt: Text description of desired output
        reference_images: List of reference image URLs/paths (1-10 images)
        mode: Generation mode (single, fusion, style_transfer, edit, subject_preservation, image_set)
        platform: Target platform for size optimization
        style: Visual style preset
        model: Model to use ("auto" for auto-selection)
        quality: Quality level for auto-selection (draft, standard, high, premium)
        **kwargs: Additional arguments
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
    
    client = BytePlusClient()
    return client.generate_image_to_image(
        prompt=enhanced_prompt,
        reference_images=reference_images,
        model=model,
        mode=mode,
        size=size,
        quality=quality,
        **kwargs
    )


if __name__ == "__main__":
    # Test the client
    print("BytePlus Marketing Creator Client")
    print("=" * 50)
    
    # Check API key
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("\nError: ARK_API_KEY not set!")
        print("Get your API key at: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey")
        exit(1)
    
    print(f"\nAPI Key: {api_key[:10]}...{api_key[-4:]}")
    print(f"\nSDK Available: {SDK_AVAILABLE}")
    print("\nAvailable Image Models:")
    for name, model_id in BytePlusClient.IMAGE_MODELS.items():
        print(f"  - {name}: {model_id}")
    
    print("\nAvailable Video Models:")
    for name, model_id in BytePlusClient.VIDEO_MODELS.items():
        print(f"  - {name}: {model_id}")
    
    print("\nClient initialized successfully!")

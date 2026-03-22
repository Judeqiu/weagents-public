#!/usr/bin/env python3
"""
Marketing Creator - API Integration Reference

This document describes the BytePlus ModelArk API integration
capabilities available in this skill.
"""

# =============================================================================
# BYTEPLUS MODELARK API OVERVIEW
# =============================================================================

"""
Base URLs:
- Image/Chat API v3: https://ark.ap-southeast.bytepluses.com/api/v3
- Video API (Seedance): https://api.byteplus.com/seedance/v1

Authentication:
- Header: Authorization: Bearer {ARK_API_KEY}
- API Key from: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey

Python SDK:
- Package: byteplussdkarkruntime
- Install: pip install byteplussdkarkruntime
"""

# =============================================================================
# IMAGE GENERATION (SEEDREAM MODELS)
# =============================================================================

"""
Available Models:
- seedream-5-0-260128 (Latest, highest quality)
- seedream-4-0-250828 (Balanced quality/speed)
- seedream-3-0-250315 (Fast generation)
- seedream-2-0-ultra-250318 (Ultra-fast)

API Endpoint (SDK):
    client.images.generate(
        model="seedream-5-0-260128",
        prompt="Your prompt here",
        size="2K",  # or "1024x1024", "1080p"
        quality="standard",  # or "hd"
        response_format="url",  # or "b64_json"
        watermark=False,
        n=1,  # 1-4 images
    )

API Endpoint (REST):
    POST https://ark.ap-southeast.bytepluses.com/api/v3/images/generations
    Headers:
        Authorization: Bearer {API_KEY}
        Content-Type: application/json
    Body:
        {
            "model": "seedream-5-0-260128",
            "prompt": "Your prompt",
            "size": "2K",
            "n": 1
        }

Parameters:
- model: Model ID string
- prompt: Text description (up to ~2000 chars)
- size: "2K", "1080p", "1024x1024", etc.
- quality: "standard" or "hd"
- response_format: "url" or "b64_json"
- watermark: true/false
- n: Number of images (1-4)
"""

# =============================================================================
# VIDEO GENERATION (SEEDANCE MODELS)
# =============================================================================

"""
Available Models:
- seedance-1-0-pro-250528 (Professional quality, up to 1080p)
- seedance-1-0-lite-i2v-250219 (Lighter model, image-to-video)

API Endpoint (Async Pattern):
    
Step 1 - Submit Job:
    POST https://api.byteplus.com/seedance/v1/videos
    Headers:
        Authorization: Bearer {API_KEY}
        Content-Type: application/json
    Body:
        {
            "model": "seedance-1-0-pro-250528",
            "prompt": "Cinematic drone shot over city at sunset",
            "resolution": "1080p",  # 480p, 720p, 1080p, 2k
            "duration": 5,  # 4-15 seconds
            "aspect_ratio": "16:9",  # 16:9, 9:16, 1:1, 4:3
            "audio": true,
            "negative_prompt": "blurry, low quality",
            "style": "cinematic",  # cinematic, anime, realistic, 3d_render
            "seed": 12345  # optional, for reproducibility
        }
    Response: {"id": "job_abc123", "status": "pending"}

Step 2 - Poll for Status:
    GET https://api.byteplus.com/seedance/v1/videos/{job_id}
    Headers:
        Authorization: Bearer {API_KEY}
    Response (completed):
        {
            "id": "job_abc123",
            "status": "completed",
            "output": {
                "video_url": "https://.../video.mp4",
                "duration": 5,
                "resolution": "1080p"
            }
        }
    Response (failed):
        {
            "id": "job_abc123",
            "status": "failed",
            "error": "Error message"
        }

Parameters:
- model: Model ID string
- prompt: Text description
- resolution: "480p", "720p", "1080p", "2k"
- duration: 4-15 seconds
- aspect_ratio: "16:9", "9:16", "1:1", "4:3"
- audio: true/false (enable native audio generation)
- references: Array of reference images/videos/audio (up to 12 items)
- negative_prompt: Elements to exclude
- style: Visual style preset
- seed: Integer for reproducibility

Image-to-Video:
    Include references array with base64-encoded images:
    "references": [
        {
            "type": "image",
            "data": "base64_encoded_image_data",
            "role": "subject"  # or "environment", "motion"
        }
    ]
"""

# =============================================================================
# PRICING (ESTIMATED - March 2026)
# =============================================================================

"""
Image Generation (Seedream):
- ~$0.02-0.05 per 2K image
- Pricing based on resolution and model

Video Generation (Seedance):
- 720p, 5s: ~$0.05-0.10
- 1080p, 5s: ~$0.25-0.50
- 2K, 5s: ~$0.50-0.75

Token-based pricing also available for some models.
See: https://docs.byteplus.com/en/docs/ModelArk/1544106
"""

# =============================================================================
# RATE LIMITS
# =============================================================================

"""
Seedance 1.0 Pro:
- Concurrency: 10 concurrent requests per account
- RPM: 600 requests per minute for job creation

Check documentation for latest limits.
"""

# =============================================================================
# EXAMPLE PROMPTS
# =============================================================================

EXAMPLE_IMAGE_PROMPTS = {
    "product": """
        Premium wireless headphones product shot, floating in mid-air,
        soft studio lighting, gradient background from navy to purple,
        reflection on glossy surface, commercial advertising photography,
        8K detail, professional product photography
    """,
    
    "lifestyle": """
        Young professional working in modern coffee shop,
        natural window lighting, laptop and coffee on table,
        candid moment, shallow depth of field, warm tones,
        lifestyle photography, authentic, relatable
    """,
    
    "tech": """
        Futuristic AI visualization, neural network nodes glowing,
        deep blue and electric purple color scheme,
        holographic interface elements, cinematic lighting,
        tech company aesthetic, cutting edge, innovation
    """,
    
    "food": """
        Gourmet burger close-up, steam rising, perfect grill marks,
        fresh ingredients visible, professional food photography,
        warm lighting, appetizing, commercial quality,
        shallow depth of field, vibrant colors
    """,
}

EXAMPLE_VIDEO_PROMPTS = {
    "product_showcase": """
        Smooth camera movement around premium smartwatch,
        rotating on elegant display stand, dramatic lighting,
        product features highlighted, luxury aesthetic,
        cinematic color grading, 4K quality feel
    """,
    
    "lifestyle_montage": """
        Fast-paced montage of friends enjoying outdoor activities,
        quick cuts between hiking, laughing, sunset views,
        energetic music visualization, vibrant colors,
        adventure lifestyle brand aesthetic
    """,
    
    "brand_story": """
        Cinematic opening shot of artisan craftsman at work,
        close-ups of hands creating product, natural workshop lighting,
        slow motion details, authentic storytelling,
        heritage brand aesthetic, emotional connection
    """,
}

# =============================================================================
# PLATFORM-SPECIFIC OPTIMIZATIONS
# =============================================================================

PLATFORM_SPECS = {
    "instagram": {
        "image_sizes": ["1080x1080", "1080x1350", "1080x1920"],
        "video_aspect": "9:16",  # Reels
        "video_duration": "15-90s",
        "style": "Polished, aesthetic, aspirational",
    },
    "tiktok": {
        "image_sizes": ["1080x1920"],
        "video_aspect": "9:16",
        "video_duration": "15-60s",
        "style": "Authentic, fast-paced, hook-focused",
    },
    "youtube": {
        "image_sizes": ["1280x720", "1920x1080"],
        "video_aspect": "16:9",
        "video_duration": "varies",
        "style": "Professional, engaging, clear narrative",
    },
    "linkedin": {
        "image_sizes": ["1200x627", "1080x1080"],
        "video_aspect": "16:9",
        "video_duration": "up to 30min",
        "style": "Professional, informative, trustworthy",
    },
    "twitter": {
        "image_sizes": ["1200x675", "1080x1080"],
        "video_aspect": "16:9",
        "video_duration": "up to 2min20s",
        "style": "Concise, attention-grabbing, shareable",
    },
}

if __name__ == "__main__":
    print("BytePlus ModelArk API Integration Reference")
    print("=" * 50)
    print("\nThis file documents the API capabilities.")
    print("Import from byteplus_client.py to use the integration.")

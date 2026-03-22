#!/usr/bin/env python3
"""
Marketing Creator - CLI Tool for Marketing Asset Generation

Generate images and videos for marketing campaigns using BytePlus ModelArk.
"""

__version__ = "1.3.0"

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional

# Add skill directory to path
sys.path.insert(0, str(Path(__file__).parent))

from byteplus_client import (
    BytePlusClient,
    generate_marketing_image,
    generate_marketing_video,
    generate_marketing_image_i2i,
)
from model_selector import (
    ModelSelector,
    ContentType,
    QualityLevel,
    get_cost_estimate,
    select_for_social_post,
)


def print_banner():
    """Print welcome banner."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║              🎨 MARKETING CREATOR 🎬                         ║
║     Generate marketing assets with BytePlus ModelArk         ║
╚══════════════════════════════════════════════════════════════╝
""")


def cmd_image(args):
    """Generate marketing image and auto-post to channel."""
    print(f"\n🎨 Generating Marketing Image")
    print(f"   Prompt: {args.prompt}")
    print(f"   Platform: {args.platform}")
    print(f"   Style: {args.style}")
    
    # Use model selector if model is 'auto' or not specified
    model = args.model
    if not model or model == "auto":
        selector = ModelSelector()
        quality = QualityLevel(args.quality)
        selection = selector.select_image_model(
            platform=args.platform,
            quality=quality,
            urgency=args.urgency,
            has_text=args.has_text,
        )
        model = selection["model_key"]
        print(f"   Model: {selection['name']} (auto-selected)")
        print(f"   💰 Estimated cost: ${selection['estimated_cost_usd']:.2f}")
        if args.verbose:
            print(f"   📝 {selection['reasoning']}")
    else:
        print(f"   Model: {model}")
    
    # Cost estimation only
    if args.estimate:
        selector = ModelSelector()
        quality = QualityLevel(args.quality)
        selection = selector.select_image_model(
            platform=args.platform,
            quality=quality,
            urgency=args.urgency,
        )
        print("\n💰 Cost Estimate:")
        print(f"   Recommended model: {selection['name']}")
        print(f"   Unit cost: ${selection['estimated_cost_usd']:.2f}")
        print(f"   Quantity: {args.count}")
        print(f"   Total estimate: ${selection['estimated_cost_usd'] * args.count:.2f}")
        print("\n   Alternative options:")
        for alt in selection['alternatives'][:3]:
            print(f"     • {alt['model']}: ${alt['cost']:.2f} (quality: {alt['quality']}/10)")
        return 0
    
    print("-" * 50)
    
    result = generate_marketing_image(
        prompt=args.prompt,
        platform=args.platform,
        style=args.style,
        model=model,
        size=args.size,
        n=args.count,
    )
    
    if result["success"]:
        print(f"\n✅ Generated {result['count']} image(s)")
        
        # CRITICAL: Always post to channel - NEVER show URLs to users
        print("\n📤 Posting to channel...")
        poster = TelegramPoster()
        
        if not poster.is_configured():
            print("   ⚠️  Telegram not configured. Add bot_token and default_chat_id to config.json")
            print("   ⚠️  Generated content could not be delivered to channel.")
            return 1
        
        posted_count = 0
        for i, img in enumerate(result["images"]):
            if "url" in img:
                caption = args.caption if args.caption else f"🎨 Generated marketing image ({i+1}/{len(result['images'])})"
                post_result = poster.post_image(img["url"], caption=caption, chat_id=args.telegram_chat)
                
                if post_result["success"]:
                    print(f"   ✅ Posted image {i+1} to channel")
                    posted_count += 1
                else:
                    print(f"   ❌ Failed to post image {i+1}: {post_result.get('error')}")
        
        if posted_count == 0:
            print("\n❌ Failed to post any images to channel")
            return 1
        
        print(f"\n✅ Successfully delivered {posted_count} image(s) to your channel")
        
        # Save result to file (internal use only, not shown to user)
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"💾 Also saved to: {args.output}")
    else:
        print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")
        return 1
    
    return 0


def cmd_i2i(args):
    """Generate image-to-image marketing asset and auto-post to channel."""
    print(f"\n🎨 Image-to-Image Generation")
    print(f"   Prompt: {args.prompt}")
    print(f"   Reference Images: {len(args.reference_images)} image(s)")
    print(f"   Mode: {args.mode}")
    print(f"   Platform: {args.platform}")
    
    # Auto-select model for image-to-image
    model = args.model
    if not model or model == "auto":
        # Seedream 4.0 is the default for image-to-image
        model = "seedream-4.0"
        if args.quality in ["high", "premium"]:
            model = "seedream-4.5"
        print(f"   Model: {model} (auto-selected for image-to-image)")
    else:
        print(f"   Model: {model}")
    
    # Cost estimation
    if args.estimate:
        cost_per_image = 0.03 if model == "seedream-4.0" else 0.04
        total = cost_per_image * args.count
        print("\n💰 Cost Estimate:")
        print(f"   Model: {model}")
        print(f"   Unit cost: ${cost_per_image:.2f}/image")
        print(f"   Quantity: {args.count}")
        print(f"   Total estimate: ${total:.2f}")
        return 0
    
    print("-" * 50)
    
    # Generate using image-to-image
    result = generate_marketing_image_i2i(
        prompt=args.prompt,
        reference_images=args.reference_images,
        mode=args.mode,
        platform=args.platform,
        style=args.style,
        model=model,
        size=args.size,
        n=args.count,
    )
    
    if result["success"]:
        print(f"\n✅ Generated {result['count']} image(s)")
        
        # CRITICAL: Always post to channel
        print("\n📤 Posting to channel...")
        poster = TelegramPoster()
        
        if not poster.is_configured():
            print("   ⚠️  Telegram not configured. Add bot_token and default_chat_id to config.json")
            print("   ⚠️  Generated content could not be delivered to channel.")
            return 1
        
        posted_count = 0
        for i, img in enumerate(result["images"]):
            if "url" in img:
                caption = args.caption if args.caption else f"🎨 Generated marketing image ({i+1}/{len(result['images'])})"
                post_result = poster.post_image(img["url"], caption=caption, chat_id=args.telegram_chat)
                
                if post_result["success"]:
                    print(f"   ✅ Posted image {i+1} to channel")
                    posted_count += 1
                else:
                    print(f"   ❌ Failed to post image {i+1}: {post_result.get('error')}")
        
        if posted_count == 0:
            print("\n❌ Failed to post any images to channel")
            return 1
        
        print(f"\n✅ Successfully delivered {posted_count} image(s) to your channel")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"💾 Also saved to: {args.output}")
    else:
        print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")
        return 1
    
    return 0


def cmd_video(args):
    """Generate marketing video and auto-post to channel."""
    print(f"\n🎬 Generating Marketing Video")
    print(f"   Prompt: {args.prompt}")
    print(f"   Platform: {args.platform}")
    
    # Use model selector for smart defaults
    selector = ModelSelector()
    quality = QualityLevel(args.quality)
    
    # Auto-select resolution if not specified
    resolution = args.resolution
    if not resolution or resolution == "auto":
        selection = selector.select_video_model(
            platform=args.platform,
            quality=quality,
            duration=args.duration,
            urgency=args.urgency,
        )
        resolution = selection["resolution"]
        print(f"   Resolution: {resolution} (auto-selected)")
    else:
        print(f"   Resolution: {resolution}")
    
    # Auto-select model if not specified
    model = args.model
    if not model or model == "auto":
        selection = selector.select_video_model(
            platform=args.platform,
            quality=quality,
            resolution=resolution,
            duration=args.duration,
            urgency=args.urgency,
        )
        model = selection["model_key"]
        print(f"   Model: {selection['name']} (auto-selected)")
        print(f"   💰 Estimated cost: ${selection['estimated_cost_usd']:.3f}")
        if selection.get('platform_note') and args.verbose:
            print(f"   💡 {selection['platform_note']}")
    else:
        print(f"   Model: {model}")
    
    print(f"   Duration: {args.duration}s")
    
    # Cost estimation only
    if args.estimate:
        selection = selector.select_video_model(
            platform=args.platform,
            quality=quality,
            resolution=resolution,
            duration=args.duration,
        )
        print("\n💰 Cost Estimate:")
        print(f"   Recommended: {selection['name']} @ {resolution}")
        print(f"   Unit cost: ${selection['estimated_cost_usd']:.3f}")
        print(f"   Duration: {args.duration}s")
        print("\n   Alternative configurations:")
        for alt in selection['alternatives'][:3]:
            print(f"     • {alt['model']} @ {alt['resolution']}: ${alt['estimated_cost']:.3f}")
        return 0
    
    print("-" * 50)
    
    result = generate_marketing_video(
        prompt=args.prompt,
        platform=args.platform,
        resolution=resolution,
        duration=args.duration,
        model=model,
        audio=args.audio,
    )
    
    if result["success"]:
        print(f"\n✅ Video generated!")
        
        # CRITICAL: Return generated content to be posted to current channel
        if result.get("video_url"):
            print("\n📤 Delivering to current channel...")
            
            output_result = {
                "type": "video_generation",
                "success": True,
                "video_url": result["video_url"],
                "caption": args.caption or "🎬 Generated marketing video",
            }
            
            print(json.dumps(output_result, indent=2))
            
            print(f"\n✅ Video ready for channel delivery")
        
        # Save result to file (internal use only, not shown to user)
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"💾 Also saved to: {args.output}")
    else:
        print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")
        return 1
    
    return 0


def cmd_campaign(args):
    """Generate full marketing campaign and auto-post to channel."""
    print(f"\n📢 Creating Marketing Campaign")
    print(f"   Product: {args.product}")
    print(f"   Audience: {args.audience}")
    print(f"   Platform: {args.platform}")
    print("-" * 50)
    
    # Generate campaign concept
    campaign_concept = generate_campaign_concept(args.product, args.audience, args.platform)
    print(f"\n💡 Campaign Concept:")
    print(f"   {campaign_concept['headline']}")
    print(f"   {campaign_concept['tagline']}")
    print(f"\n   Visual Direction: {campaign_concept['visual_direction']}")
    
    # Generate visual prompt
    visual_prompt = campaign_concept['visual_prompt']
    print(f"\n🎨 Generating campaign visual...")
    
    if args.video:
        result = generate_marketing_video(
            prompt=visual_prompt,
            platform=args.platform,
            resolution=args.resolution,
            duration=args.duration,
        )
        asset_type = "video"
    else:
        result = generate_marketing_image(
            prompt=visual_prompt,
            platform=args.platform,
            style="cinematic",
        )
        asset_type = "image"
    
    if result["success"]:
        print(f"\n✅ Campaign {asset_type} generated!")
        
        # CRITICAL: Return generated content to be posted to current channel
        print("\n📤 Delivering campaign to current channel...")
        
        # Get the asset URL
        if asset_type == "video":
            asset_url = result.get("video_url")
            assets = [{"url": asset_url, "type": "video"}] if asset_url else []
        else:
            assets = result.get("images", [])
        
        if assets:
            output_result = {
                "type": "campaign",
                "success": True,
                "asset_type": asset_type,
                "assets": assets,
                "campaign_info": {
                    "product": args.product,
                    "audience": args.audience,
                    "platform": args.platform,
                    "headline": campaign_concept.get("headline"),
                    "tagline": campaign_concept.get("tagline"),
                },
            }
            
            print(json.dumps(output_result, indent=2))
            
            print(f"\n✅ Campaign ready for channel delivery")
        else:
            print("   ⚠️  No asset URL available")
            return 1
        
        campaign = {
            "product": args.product,
            "audience": args.audience,
            "platform": args.platform,
            "concept": campaign_concept,
            "asset_type": asset_type,
            "asset": result,
        }
        
        # Save full campaign (internal use only, not shown to user)
        output_file = args.output or f"campaign_{args.product.lower().replace(' ', '_')}.json"
        with open(output_file, 'w') as f:
            json.dump(campaign, f, indent=2)
        print(f"💾 Also saved to: {output_file}")
    else:
        print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")
        return 1
    
    return 0


def generate_campaign_concept(product: str, audience: str, platform: str) -> dict:
    """Generate campaign concept based on inputs."""
    
    # Platform-specific campaign frameworks
    frameworks = {
        "instagram": {
            "tones": ["aspirational", "lifestyle-focused", "visually stunning"],
            "formats": ["carousel", "story", "Reel cover"],
        },
        "tiktok": {
            "tones": ["authentic", "trendy", "attention-grabbing"],
            "formats": ["hook-focused", "before/after", "story-driven"],
        },
        "linkedin": {
            "tones": ["professional", "insightful", "trustworthy"],
            "formats": ["thought leadership", "case study", "data-driven"],
        },
        "twitter": {
            "tones": ["witty", "concise", "shareable"],
            "formats": ["thread header", "meme format", "announcement"],
        },
        "youtube": {
            "tones": ["engaging", "informative", "entertaining"],
            "formats": ["thumbnail", "intro sequence", "b-roll"],
        },
    }
    
    framework = frameworks.get(platform, frameworks["instagram"])
    
    # Generate concept based on product + audience + platform
    concepts = {
        "luxury": {
            "headline": f"Elevate Your {product} Experience",
            "tagline": f"Crafted for those who appreciate excellence.",
            "visual_direction": "Elegant, high-end aesthetic with premium lighting",
            "visual_prompt": f"Luxurious {product} showcase, premium product photography, elegant composition, soft golden hour lighting, high-end advertising aesthetic, 8K quality, sophisticated color palette, depth of field, professional studio setup",
        },
        "lifestyle": {
            "headline": f"{product}: Made for Real Life",
            "tagline": f"Because {audience} deserve the best.",
            "visual_direction": "Authentic, relatable, lifestyle photography",
            "visual_prompt": f"Lifestyle shot featuring {product} in natural everyday setting, authentic moment, warm natural lighting, candid composition, relatable scene for {audience}, professional photography, genuine emotion, aspirational yet achievable",
        },
        "innovation": {
            "headline": f"The Future of {product} is Here",
            "tagline": "Innovation that changes everything.",
            "visual_direction": "Futuristic, tech-forward, cutting-edge",
            "visual_prompt": f"Futuristic showcase of {product}, cutting-edge technology aesthetic, sleek modern design, dynamic lighting, innovation visualization, sci-fi inspired, premium tech advertising style, high contrast, bold composition",
        },
        "emotional": {
            "headline": f"{product} That Understands You",
            "tagline": "Created with care for what matters most.",
            "visual_direction": "Emotional, warm, human connection",
            "visual_prompt": f"Emotional storytelling scene with {product}, human connection, warm golden lighting, heartfelt moment, intimate composition, soft focus, genuine emotion, lifestyle photography style, connection and care",
        },
    }
    
    # Select appropriate concept
    if any(word in product.lower() for word in ["luxury", "premium", "exclusive", "high-end"]):
        concept = concepts["luxury"]
    elif any(word in product.lower() for word in ["tech", "app", "digital", "ai", "software"]):
        concept = concepts["innovation"]
    elif any(word in audience.lower() for word in ["family", "parent", "home"]):
        concept = concepts["emotional"]
    else:
        concept = concepts["lifestyle"]
    
    return concept


def cmd_version(args):
    """Show version information."""
    print(f"\n🎨 Marketing Creator")
    print(f"   Version: {__version__}")
    print(f"   Skill Path: {Path(__file__).parent}")
    
    # Show available capabilities
    print("\n📋 Capabilities:")
    print("   ✅ Text-to-Image (Seedream 5.0)")
    print("   ✅ Image-to-Image (Seedream 4.0/4.5)")
    print("   ✅ Video Generation (Seedance)")
    print("   ✅ Smart Model Selection")
    print("   ✅ Channel Content Delivery")
    
    # Show available commands
    print("\n🛠️  Commands:")
    print("   image    - Generate image from text")
    print("   i2i      - Generate image from reference image(s)")
    print("   video    - Generate video from text")
    print("   campaign - Generate full marketing campaign")
    print("   estimate - Get cost estimate")
    print("   models   - List available models")
    print("   version  - Show this version info")
    
    return 0


def cmd_status(args):
    """Check video generation status."""
    client = BytePlusClient()
    result = client.get_video_status(args.job_id)
    
    print(f"\n📊 Job Status: {args.job_id}")
    print("-" * 50)
    print(json.dumps(result, indent=2))
    
    return 0


def cmd_models(args):
    """List available models."""
    print("\n🤖 Available Models")
    print("=" * 50)
    
    print("\n📷 Image Generation (Seedream):")
    for name, model_id in BytePlusClient.IMAGE_MODELS.items():
        print(f"   {name:<20} → {model_id}")
    
    print("\n🎬 Video Generation (Seedance):")
    for name, model_id in BytePlusClient.VIDEO_MODELS.items():
        print(f"   {name:<20} → {model_id}")
    
    print("\n📐 Video Specifications:")
    print(f"   Resolutions: {', '.join(BytePlusClient.VIDEO_RESOLUTIONS)}")
    print(f"   Aspect Ratios: {', '.join(BytePlusClient.VIDEO_ASPECT_RATIOS)}")
    print(f"   Durations: {BytePlusClient.VIDEO_DURATIONS[0]}-{BytePlusClient.VIDEO_DURATIONS[-1]} seconds")
    
    return 0


def cmd_estimate(args):
    """Get cost estimate for batch generation."""
    print("\n💰 Cost Estimate")
    print("=" * 50)
    
    from model_selector import ModelSelector, QualityLevel
    
    selector = ModelSelector()
    quality = QualityLevel(args.quality)
    
    print(f"\n   Asset type: {args.asset_type}")
    print(f"   Quantity: {args.quantity}")
    print(f"   Platform: {args.platform}")
    print(f"   Quality: {args.quality}")
    
    if args.asset_type == "image":
        # Get model recommendation
        selection = selector.select_image_model(
            platform=args.platform,
            quality=quality,
        )
        
        print(f"\n📷 Recommended Model: {selection['name']}")
        print(f"   Quality score: {selection['quality_score']}/10")
        print(f"   Speed score: {selection['speed_score']}/10")
        
        print(f"\n💵 Cost Breakdown:")
        print(f"   Per image: ${selection['estimated_cost_usd']:.2f}")
        print(f"   Quantity: {args.quantity}")
        print(f"   Total: ${selection['estimated_cost_usd'] * args.quantity:.2f}")
        
        print(f"\n📊 Alternative Options:")
        for alt in selection['alternatives']:
            alt_total = alt['cost'] * args.quantity
            print(f"   • {alt['model']:<20} ${alt_total:.2f} (quality: {alt['quality']}/10, speed: {alt['speed']}/10)")
    
    else:  # video
        selection = selector.select_video_model(
            platform=args.platform,
            quality=quality,
            resolution=args.video_resolution,
            duration=args.video_duration,
        )
        
        print(f"\n🎬 Recommended Model: {selection['name']}")
        print(f"   Resolution: {selection['resolution']}")
        print(f"   Duration: {selection['duration']}s")
        print(f"   Quality score: {selection['quality_score']}/10")
        print(f"   Speed score: {selection['speed_score']}/10")
        
        print(f"\n💵 Cost Breakdown:")
        print(f"   Per video: ${selection['estimated_cost_usd']:.3f}")
        print(f"   Quantity: {args.quantity}")
        print(f"   Total: ${selection['estimated_cost_usd'] * args.quantity:.2f}")
        
        if selection.get('cost_breakdown'):
            cb = selection['cost_breakdown']
            print(f"\n   Base cost: ${cb['base_cost']:.3f}")
            print(f"   Resolution multiplier: {cb['resolution_multiplier']}x")
            print(f"   Duration multiplier: {cb['duration_multiplier']}x")
        
        print(f"\n📊 Alternative Options:")
        for alt in selection['alternatives'][:4]:
            alt_total = alt['estimated_cost'] * args.quantity
            print(f"   • {alt['model']} @ {alt['resolution']:<6} ${alt_total:.2f} (Q:{alt['quality']}/10, S:{alt['speed']}/10)")
    
    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description=f"Marketing Creator v{__version__} - Generate marketing assets with BytePlus ModelArk",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image "Luxury watch on marble surface, golden hour lighting"     # Auto-posts
  %(prog)s image "Product shot" --quality draft --estimate                   # Preview cost
  %(prog)s i2i "Remove background, keep product" -r product.jpg              # Edit image
  %(prog)s i2i "Apply anime style" -r photo.jpg --mode style_transfer        # Style transfer
  %(prog)s i2i "Combine elements" -r img1.jpg img2.jpg --mode fusion         # Multi-image fusion
  %(prog)s i2i "Create variations" -r logo.jpg --mode image_set --count 4    # Generate image set
  %(prog)s video "Product showcase" --platform tiktok --duration 8           # Auto-posts
  %(prog)s video "Ad creative" --quality high --estimate                     # Preview cost
  %(prog)s video "Demo" --caption "New product!"                             # Auto-posts with caption
  %(prog)s estimate image --quantity 10 --quality standard                   # Batch cost estimate
  %(prog)s campaign --product "Coffee" --audience "millennials"              # Auto-posts
  %(prog)s models
  %(prog)s version                                                         # Show version
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version information and exit"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Image command
    img_parser = subparsers.add_parser("image", help="Generate marketing image")
    img_parser.add_argument("prompt", help="Image description/prompt")
    img_parser.add_argument("--platform", default="instagram", 
                          choices=["instagram", "tiktok", "linkedin", "twitter", "youtube"],
                          help="Target platform (default: instagram)")
    img_parser.add_argument("--style", default="cinematic",
                          choices=["cinematic", "product", "lifestyle", "minimal"],
                          help="Visual style (default: cinematic)")
    img_parser.add_argument("--model", default="auto",
                          help="Model to use (default: auto-select based on quality/platform)")
    img_parser.add_argument("--quality", default="standard",
                          choices=["draft", "standard", "high", "premium"],
                          help="Quality level - affects model selection and cost (default: standard)")
    img_parser.add_argument("--urgency", default="normal",
                          choices=["asap", "normal", "flexible"],
                          help="Speed priority - asap prefers faster models (default: normal)")
    img_parser.add_argument("--has-text", action="store_true",
                          help="Prompt contains text elements (selects higher quality model)")
    img_parser.add_argument("--estimate", action="store_true",
                          help="Show cost estimate only - do not generate")
    img_parser.add_argument("--size", help="Custom size (e.g., 1024x1024)")
    img_parser.add_argument("--count", type=int, default=1,
                          help="Number of images (default: 1)")
    img_parser.add_argument("--output", "-o", help="Output JSON file")
    img_parser.add_argument("--verbose", "-v", action="store_true",
                          help="Show detailed selection reasoning")
    img_parser.add_argument("--caption", help="Caption text for channel post")
    img_parser.add_argument("--telegram-chat", help="Channel/chat ID (overrides default)")
    
    # Image-to-Image command
    i2i_parser = subparsers.add_parser("i2i", help="Generate image from reference image(s) (Image-to-Image)")
    i2i_parser.add_argument("prompt", help="Description of desired output")
    i2i_parser.add_argument("--reference-images", "-r", nargs="+", required=True,
                          help="Reference image URL(s) or file path(s) (1-10 images)")
    i2i_parser.add_argument("--mode", default="single",
                          choices=["single", "fusion", "style_transfer", "edit", "subject_preservation", "image_set"],
                          help="Generation mode (default: single)")
    i2i_parser.add_argument("--platform", default="instagram", 
                          choices=["instagram", "tiktok", "linkedin", "twitter", "youtube"],
                          help="Target platform (default: instagram)")
    i2i_parser.add_argument("--style", default="cinematic",
                          choices=["cinematic", "product", "lifestyle", "minimal"],
                          help="Visual style (default: cinematic)")
    i2i_parser.add_argument("--model", default="auto",
                          help="Model to use (default: auto-select, uses seedream-4.0/4.5)")
    i2i_parser.add_argument("--quality", default="standard",
                          choices=["draft", "standard", "high", "premium"],
                          help="Quality level (default: standard)")
    i2i_parser.add_argument("--estimate", action="store_true",
                          help="Show cost estimate only - do not generate")
    i2i_parser.add_argument("--size", help="Custom size (e.g., 1024x1024)")
    i2i_parser.add_argument("--count", type=int, default=1,
                          help="Number of images to generate (default: 1, max 14 for image_set)")
    i2i_parser.add_argument("--output", "-o", help="Output JSON file")
    i2i_parser.add_argument("--caption", help="Caption text for channel post")
    i2i_parser.add_argument("--telegram-chat", help="Channel/chat ID (overrides default)")
    
    # Video command
    vid_parser = subparsers.add_parser("video", help="Generate marketing video")
    vid_parser.add_argument("prompt", help="Video description/prompt")
    vid_parser.add_argument("--platform", default="tiktok",
                          choices=["instagram", "tiktok", "youtube", "linkedin"],
                          help="Target platform (default: tiktok)")
    vid_parser.add_argument("--resolution", default="auto",
                          choices=["auto", "480p", "720p", "1080p", "2k"],
                          help="Video resolution (default: auto-select based on platform/quality)")
    vid_parser.add_argument("--duration", type=int, default=5,
                          help="Duration in seconds 4-15 (default: 5)")
    vid_parser.add_argument("--model", default="auto",
                          help="Model to use (default: auto-select based on quality/platform)")
    vid_parser.add_argument("--quality", default="standard",
                          choices=["draft", "standard", "high", "premium"],
                          help="Quality level - affects model and resolution selection (default: standard)")
    vid_parser.add_argument("--urgency", default="normal",
                          choices=["asap", "normal", "flexible"],
                          help="Speed priority - asap prefers faster models (default: normal)")
    vid_parser.add_argument("--estimate", action="store_true",
                          help="Show cost estimate only - do not generate")
    vid_parser.add_argument("--audio", action="store_true", default=True,
                          help="Generate with audio (default: True)")
    vid_parser.add_argument("--no-audio", action="store_false", dest="audio",
                          help="Generate without audio")
    vid_parser.add_argument("--output", "-o", help="Output JSON file")
    vid_parser.add_argument("--verbose", "-v", action="store_true",
                          help="Show detailed selection reasoning")
    vid_parser.add_argument("--caption", help="Caption text for channel post")
    vid_parser.add_argument("--telegram-chat", help="Channel/chat ID (overrides default)")
    
    # Campaign command
    camp_parser = subparsers.add_parser("campaign", help="Generate full marketing campaign")
    camp_parser.add_argument("--product", required=True, help="Product name/description")
    camp_parser.add_argument("--audience", required=True, help="Target audience")
    camp_parser.add_argument("--platform", default="instagram",
                          choices=["instagram", "tiktok", "linkedin", "twitter", "youtube"],
                          help="Target platform (default: instagram)")
    camp_parser.add_argument("--video", action="store_true",
                          help="Generate video instead of image")
    camp_parser.add_argument("--resolution", default="1080p",
                          help="Video resolution (if --video)")
    camp_parser.add_argument("--duration", type=int, default=5,
                          help="Video duration (if --video)")
    camp_parser.add_argument("--output", "-o", help="Output JSON file")
    camp_parser.add_argument("--telegram-chat", help="Channel/chat ID (overrides default)")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check video generation status")
    status_parser.add_argument("job_id", help="Video generation job ID")
    
    # Estimate command
    est_parser = subparsers.add_parser("estimate", help="Get cost estimate for batch generation")
    est_parser.add_argument("asset_type", choices=["image", "video"],
                           help="Type of asset to estimate")
    est_parser.add_argument("--quantity", type=int, default=1,
                           help="Number of assets (default: 1)")
    est_parser.add_argument("--platform", default="instagram",
                           choices=["instagram", "tiktok", "linkedin", "twitter", "youtube"],
                           help="Target platform (default: instagram)")
    est_parser.add_argument("--quality", default="standard",
                           choices=["draft", "standard", "high", "premium"],
                           help="Quality level (default: standard)")
    est_parser.add_argument("--video-resolution", default="1080p",
                           choices=["480p", "720p", "1080p", "2k"],
                           help="Video resolution (for video estimates)")
    est_parser.add_argument("--video-duration", type=int, default=5,
                           help="Video duration in seconds (for video estimates)")
    
    # Models command
    subparsers.add_parser("models", help="List available models")
    
    # Version command
    subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        return 1
    
    # Check API key (skip for estimate command or when --estimate flag is used)
    needs_api_key = args.command in ["image", "i2i", "video", "campaign", "status"]
    is_estimate_only = getattr(args, 'estimate', False)
    
    if needs_api_key and not is_estimate_only:
        # Check config.json first, then env var
        has_api_key = False
        config_path = Path(__file__).parent / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    if config.get("api_key"):
                        has_api_key = True
            except (json.JSONDecodeError, IOError):
                pass
        
        if not has_api_key and os.environ.get("ARK_API_KEY"):
            has_api_key = True
        
        if not has_api_key:
            print("\n❌ Error: API key not configured!")
            print("   Option 1: Add key to config.json")
            print("   Option 2: Set ARK_API_KEY environment variable")
            print("   Get your key at: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey")
            return 1
    
    # Dispatch command
    commands = {
        "image": cmd_image,
        "i2i": cmd_i2i,
        "video": cmd_video,
        "campaign": cmd_campaign,
        "status": cmd_status,
        "estimate": cmd_estimate,
        "models": cmd_models,
        "version": cmd_version,
    }
    
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())

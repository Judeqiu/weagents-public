#!/usr/bin/env python3
"""
Marketing Creator - CLI Tool for Marketing Asset Generation

Generate images and videos for marketing campaigns using BytePlus ModelArk.
"""

__version__ = "1.7.0"

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
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        
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
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        # CRITICAL: Return generated content to be posted to current channel
        # The calling system (Kimi/Claw) will handle posting to the current channel
        print("\n📤 Delivering to current channel...")
        
        # Output the results in a format that can be captured by the channel system
        output_result = {
            "type": "image_generation",
            "success": True,
            "count": result["count"],
            "images": result["images"],
            "caption": args.caption or f"🎨 Generated marketing image",
        }
        
        # Print JSON output for channel integration
        print(json.dumps(output_result, indent=2))
        
        print(f"\n✅ {result['count']} image(s) ready for channel delivery")
        
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
    
    # Auto-select model if not specified
    model = args.model
    if not model or model == "auto":
        selection = selector.select_video_model(
            platform=args.platform,
            quality=quality,
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
    if args.resolution:
        print(f"   Resolution: {args.resolution}")
    print(f"   Audio: {'enabled' if args.audio else 'disabled'}")
    
    # Cost estimation only
    if args.estimate:
        selection = selector.select_video_model(
            platform=args.platform,
            quality=quality,
            duration=args.duration,
        )
        print("\n💰 Cost Estimate:")
        print(f"   Recommended: {selection['name']}")
        print(f"   Unit cost: ${selection['estimated_cost_usd']:.3f}")
        print(f"   Duration: {args.duration}s")
        return 0
    
    print("-" * 50)
    
    result = generate_marketing_video(
        prompt=args.prompt,
        platform=args.platform,
        duration=args.duration,
        model=model,
        resolution=args.resolution,
        generate_audio=args.audio,
        watermark=args.watermark,
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



def cmd_story(args):
    """Generate a cohesive marketing story with multiple assets and create HTML landing page."""
    print(f"\n📖 Creating Marketing Story")
    print(f"   Product: {args.product}")
    print(f"   Theme: {args.theme}")
    print(f"   Pages/Sections: {args.pages}")
    print(f"   Include Video: {args.include_video}")
    
    # Handle reference images
    reference_images = args.reference_image if args.reference_image else []
    if reference_images:
        print(f"   Reference Images: {len(reference_images)}")
        for i, img in enumerate(reference_images, 1):
            print(f"      [{i}] {img}")
    print("=" * 60)
    
    # Generate story structure based on product and theme
    story_structure = generate_story_structure(args.product, args.theme, args.pages)
    
    print(f"\n✨ Story Arc: {story_structure['title']}")
    print(f"   Hook: {story_structure['hook']}")
    
    generated_assets = []
    total_cost = 0.0
    
    # Generate assets for each section
    for i, section in enumerate(story_structure['sections'], 1):
        print(f"\n📄 Section {i}/{len(story_structure['sections'])}: {section['name']}")
        print(f"   Purpose: {section['purpose']}")
        
        # Determine if we should use original image or generate
        use_original = args.use_original and reference_images and section['name'] == 'Solution'
        
        if use_original:
            # Use the first reference image directly for Solution section
            print(f"   Using original product photo...")
            section['image'] = {'url': reference_images[0], 'prompt': section['visual_prompt']}
            section['image_cost'] = 0
            section['is_original'] = True
            print(f"   ✅ Original image used")
        elif reference_images:
            # Use image-to-image generation with reference
            print(f"   Generating visual with product reference (image-to-image)...")
            
            # Adjust prompt based on section purpose
            i2i_prompt = f"{section['visual_prompt']}, featuring the product from the reference image"
            if section['name'] == 'Hero':
                i2i_prompt = f"Dramatic hero shot, product showcase, {section['visual_prompt']}, professional advertising photography"
            elif section['name'] == 'Benefits':
                i2i_prompt = f"Lifestyle scene showing benefits, person using product, {section['visual_prompt']}"
            elif section['name'] == 'Social Proof':
                i2i_prompt = f"Happy customers with product, authentic testimonial scene, {section['visual_prompt']}"
            
            img_result = generate_marketing_image_i2i(
                prompt=i2i_prompt,
                reference_images=reference_images,
                mode="single",
                platform=args.platform,
                style=args.style,
                quality=args.quality,
            )
            
            if img_result["success"]:
                section['image'] = img_result['images'][0] if img_result['images'] else None
                section['image_cost'] = 0.04  # I2I cost
                total_cost += 0.04
                print(f"   ✅ Image generated from reference")
            else:
                print(f"   ❌ Image generation failed: {img_result.get('error', 'Unknown')}")
                section['image'] = None
        else:
            # Standard text-to-image generation
            print(f"   Generating visual...")
            img_result = generate_marketing_image(
                prompt=section['visual_prompt'],
                platform=args.platform,
                style=args.style,
                quality=args.quality,
            )
            
            if img_result["success"]:
                section['image'] = img_result['images'][0] if img_result['images'] else None
                section['image_cost'] = 0.035  # Approximate cost
                total_cost += 0.035
                print(f"   ✅ Image generated")
            else:
                print(f"   ❌ Image failed: {img_result.get('error', 'Unknown')}")
                section['image'] = None
        
        # Generate video if requested and this is a key section (hero or CTA)
        if args.include_video and section.get('include_video') and not args.estimate:
            print(f"   🎬 Generating video...")
            vid_result = generate_marketing_video(
                prompt=section['video_prompt'] or section['visual_prompt'],
                platform=args.platform,
                duration=5,
                quality=args.quality,
            )
            if vid_result["success"]:
                section['video'] = vid_result.get('video_url')
                section['video_cost'] = 0.002  # Approximate cost
                total_cost += 0.002
                print(f"   ✅ Video generated")
            else:
                print(f"   ❌ Video failed: {vid_result.get('error', 'Unknown')}")
                section['video'] = None
        
        generated_assets.append(section)
    
    if args.estimate:
        print(f"\n💰 Estimated Total Cost: ${total_cost:.2f}")
        return 0
    
    # Generate HTML landing page
    print(f"\n🌐 Generating HTML landing page...")
    html_content = generate_story_html(story_structure, generated_assets, args.theme)
    
    # Save HTML to output directory
    output_dir = Path(args.output) if args.output else Path.cwd() / "marketing_story"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    html_path = output_dir / "index.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   ✅ HTML saved to: {html_path}")
    
    # Save story manifest for netlify-deploy skill
    manifest = {
        "type": "marketing_story",
        "title": story_structure['title'],
        "product": args.product,
        "theme": args.theme,
        "reference_images": reference_images,
        "use_original": args.use_original,
        "sections": len(generated_assets),
        "total_cost": total_cost,
        "output_dir": str(output_dir.absolute()),
        "html_file": str(html_path.absolute()),
        "assets": [
            {
                "section": s['name'],
                "headline": s['headline'],
                "body": s['body_text'],
                "image_url": s.get('image', {}).get('url') if s.get('image') else None,
                "video_url": s.get('video'),
                "is_original": s.get('is_original', False),
            }
            for s in generated_assets
        ]
    }
    
    manifest_path = output_dir / "story_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print(f"   ✅ Manifest saved to: {manifest_path}")
    
    # Output for channel integration
    output_result = {
        "type": "marketing_story",
        "success": True,
        "title": story_structure['title'],
        "output_dir": str(output_dir.absolute()),
        "html_file": str(html_path.absolute()),
        "manifest": str(manifest_path.absolute()),
        "sections": len(generated_assets),
        "total_cost": total_cost,
        "ready_for_netlify": True,  # Indicates output is ready for netlify-deploy skill
    }
    
    print("\n" + "=" * 60)
    print(json.dumps(output_result, indent=2))
    print("=" * 60)
    print(f"\n✅ Marketing story complete!")
    print(f"   📁 Output: {output_dir}")
    print(f"   🌐 HTML: {html_path}")
    print(f"   📋 Manifest: {manifest_path}")
    print(f"\n🚀 Ready for netlify-deploy skill")
    
    return 0


def generate_story_structure(product: str, theme: str, num_pages: int) -> dict:
    """Generate a cohesive story structure based on product and theme."""
    
    # Theme-based story frameworks
    themes = {
        "sustainable-adventure": {
            "title": f"The {product} Journey: From Nature to You",
            "hook": "Discover how sustainable choices create extraordinary experiences",
            "color_scheme": {"primary": "#2d5a3d", "secondary": "#f4f1ea", "accent": "#e07b39"},
            "font": "Montserrat",
        },
        "luxury-lifestyle": {
            "title": f"Experience {product}: Where Excellence Meets Elegance",
            "hook": "Elevate every moment with uncompromising quality",
            "color_scheme": {"primary": "#1a1a1a", "secondary": "#f5f5f5", "accent": "#c9a227"},
            "font": "Playfair Display",
        },
        "tech-innovation": {
            "title": f"{product}: The Future is Here",
            "hook": "Revolutionary technology that transforms your daily life",
            "color_scheme": {"primary": "#0a192f", "secondary": "#112240", "accent": "#64ffda"},
            "font": "Inter",
        },
        "wellness-health": {
            "title": f"{product}: Your Journey to Wellness",
            "hook": "Nurture your body, mind, and spirit with natural solutions",
            "color_scheme": {"primary": "#4a7c59", "secondary": "#f7f5f0", "accent": "#d4a574"},
            "font": "Lora",
        },
        "family-home": {
            "title": f"{product}: Made for Moments That Matter",
            "hook": "Creating memories and comfort for the ones you love",
            "color_scheme": {"primary": "#5a4a3a", "secondary": "#faf8f5", "accent": "#e85d4c"},
            "font": "Nunito",
        },
    }
    
    # Default theme if not found
    theme_data = themes.get(theme, themes["sustainable-adventure"])
    
    # Standard story sections based on copywriting frameworks (AIDA, PAS, etc.)
    all_sections = [
        {
            "name": "Hero",
            "purpose": "Grab attention with emotional hook",
            "headline": theme_data["title"],
            "subheadline": theme_data["hook"],
            "body_text": f"Introducing {product} - the perfect companion for your {theme.replace('-', ' ')} journey. Experience the difference that quality and thoughtfulness make.",
            "cta": "Discover More",
            "visual_prompt": f"Stunning hero image for {product}, {theme} aesthetic, wide cinematic composition, professional marketing photography, emotional storytelling, high-end advertising style, dramatic lighting",
            "video_prompt": f"Cinematic hero video for {product}, slow-motion reveal, {theme} atmosphere, professional color grading",
            "include_video": True,
        },
        {
            "name": "Problem",
            "purpose": "Agitate the pain point",
            "headline": "Does This Sound Familiar?",
            "subheadline": "The struggle is real",
            "body_text": f"We've all been there. Searching for a {product} that actually delivers on its promises. Dealing with inferior alternatives that leave you frustrated and disappointed.",
            "cta": "See The Solution",
            "visual_prompt": f"Relatable problem scenario for {product}, emotional candid photography, {theme} style, everyday situation, authentic moment, soft natural lighting",
            "include_video": False,
        },
        {
            "name": "Solution",
            "purpose": "Present the product as answer",
            "headline": f"Meet {product}: Your Perfect Solution",
            "subheadline": "Designed with you in mind",
            "body_text": f"After years of research and development, we've created {product} - a revolutionary approach that combines quality, sustainability, and exceptional performance.",
            "cta": "Learn More",
            "visual_prompt": f"Product showcase for {product}, clean studio photography, {theme} aesthetic, elegant composition, premium quality visible, soft shadows, professional lighting",
            "include_video": True,
        },
        {
            "name": "Benefits",
            "purpose": "Show key advantages",
            "headline": "Why Thousands Are Making the Switch",
            "subheadline": "Real benefits, real results",
            "body_text": "✓ Premium quality that lasts\n✓ Sustainable and eco-friendly\n✓ Designed for modern lifestyles\n✓ Loved by customers worldwide",
            "cta": "Explore Benefits",
            "visual_prompt": f"Lifestyle benefits scene with {product}, happy person using product, {theme} environment, aspirational yet achievable, warm natural lighting, authentic moment",
            "include_video": False,
        },
        {
            "name": "Social Proof",
            "purpose": "Build trust with testimonials",
            "headline": "Join Thousands of Happy Customers",
            "subheadline": "Real stories from real people",
            "body_text": '"I never knew what I was missing until I tried this. It completely transformed my daily routine!" - Sarah M.\n\n"Best investment I\'ve made this year. The quality is unmatched." - Michael R.',
            "cta": "Read Reviews",
            "visual_prompt": f"Diverse group of happy customers with {product}, genuine smiles, {theme} setting, authentic testimonial photography, natural lighting, community feeling",
            "include_video": False,
        },
        {
            "name": "CTA",
            "purpose": "Drive action",
            "headline": f"Ready to Transform Your Experience?",
            "subheadline": "Limited time offer - don't miss out",
            "body_text": f"Start your {theme.replace('-', ' ')} journey today with {product}. Order now and experience the difference that quality makes.",
            "cta": "Get Yours Now",
            "visual_prompt": f"Powerful call-to-action image with {product}, inspiring scene, {theme} aesthetic, uplifting composition, golden hour lighting, motivational atmosphere",
            "video_prompt": f"Dynamic CTA video for {product}, energetic motion, {theme} vibes, urgency and excitement",
            "include_video": True,
        },
    ]
    
    # Select sections based on requested number of pages
    if num_pages <= 3:
        selected_sections = [all_sections[0], all_sections[2], all_sections[5]]  # Hero, Solution, CTA
    elif num_pages == 4:
        selected_sections = [all_sections[0], all_sections[2], all_sections[3], all_sections[5]]  # Add Benefits
    elif num_pages == 5:
        selected_sections = [all_sections[0], all_sections[1], all_sections[2], all_sections[3], all_sections[5]]  # Add Problem
    else:
        selected_sections = all_sections  # All sections
    
    return {
        "title": theme_data["title"],
        "hook": theme_data["hook"],
        "theme": theme,
        "color_scheme": theme_data["color_scheme"],
        "font": theme_data["font"],
        "sections": selected_sections,
    }


def generate_story_html(story_structure: dict, assets: list, theme: str) -> str:
    """Generate AI-designed HTML landing page for the marketing story."""
    
    colors = story_structure['color_scheme']
    font = story_structure['font']
    
    # Generate CSS for responsive design
    css = f"""
        @import url('https://fonts.googleapis.com/css2?family={font.replace(" ", "+")}:wght@400;600;700&display=swap');
        
        :root {{
            --primary: {colors['primary']};
            --secondary: {colors['secondary']};
            --accent: {colors['accent']};
            --font-main: '{font}', sans-serif;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: var(--font-main);
            background: var(--secondary);
            color: #333;
            line-height: 1.6;
        }}
        
        .section {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 4rem 2rem;
            position: relative;
        }}
        
        .section-content {{
            max-width: 1200px;
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }}
        
        .section:nth-child(even) .section-content {{
            direction: rtl;
        }}
        
        .section:nth-child(even) .section-content > * {{
            direction: ltr;
        }}
        
        .text-content {{
            padding: 2rem;
        }}
        
        .visual-content {{
            position: relative;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        }}
        
        .visual-content img {{
            width: 100%;
            height: auto;
            display: block;
            transition: transform 0.5s ease;
        }}
        
        .visual-content:hover img {{
            transform: scale(1.05);
        }}
        
        h1 {{
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 1rem;
            line-height: 1.2;
        }}
        
        h2 {{
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }}
        
        .subheadline {{
            font-size: 1.25rem;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 1.5rem;
        }}
        
        .body-text {{
            font-size: 1.125rem;
            color: #555;
            margin-bottom: 2rem;
            white-space: pre-line;
        }}
        
        .cta-button {{
            display: inline-block;
            padding: 1rem 2.5rem;
            background: var(--accent);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        
        .hero {{
            background: linear-gradient(135deg, var(--primary) 0%, {colors['primary']}dd 100%);
            color: white;
        }}
        
        .hero h1, .hero h2 {{
            color: white;
        }}
        
        .hero .subheadline {{
            color: var(--accent);
        }}
        
        .hero .body-text {{
            color: rgba(255,255,255,0.9);
        }}
        
        .video-container {{
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: 20px;
        }}
        
        .video-container video {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        @media (max-width: 768px) {{
            .section-content {{
                grid-template-columns: 1fr;
                gap: 2rem;
            }}
            
            .section {{
                padding: 2rem 1rem;
            }}
            
            .section:nth-child(even) .section-content {{
                direction: ltr;
            }}
        }}
        
        .scroll-indicator {{
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            animation: bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateX(-50%) translateY(0); }}
            40% {{ transform: translateX(-50%) translateY(-10px); }}
            60% {{ transform: translateX(-50%) translateY(-5px); }}
        }}
    """
    
    # Generate HTML sections
    sections_html = []
    for i, section in enumerate(assets):
        is_hero = i == 0
        section_class = "section hero" if is_hero else "section"
        
        # Determine visual content (image or video)
        visual_html = ""
        if section.get('video'):
            visual_html = f'''
                <div class="visual-content">
                    <div class="video-container">
                        <video autoplay loop muted playsinline>
                            <source src="{section['video']}" type="video/mp4">
                        </video>
                    </div>
                </div>
            '''
        elif section.get('image'):
            img_url = section['image'].get('url', '')
            visual_html = f'''
                <div class="visual-content">
                    <img src="{img_url}" alt="{section['headline']}">
                </div>
            '''
        
        section_html = f'''
            <section class="{section_class}">
                <div class="section-content">
                    <div class="text-content">
                        <h2>{section['headline']}</h2>
                        <p class="subheadline">{section['subheadline']}</p>
                        <p class="body-text">{section['body_text']}</p>
                        <a href="#" class="cta-button">{section['cta']}</a>
                    </div>
                    {visual_html}
                </div>
                {('<div class="scroll-indicator">↓</div>' if is_hero else '')}
            </section>
        '''
        sections_html.append(section_html)
    
    # Assemble full HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{story_structure['title']}</title>
    <style>{css}</style>
</head>
<body>
    {''.join(sections_html)}
</body>
</html>"""
    
    return html
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
    print("   ✅ Marketing Story Generator (with Netlify-ready HTML)")
    
    # Show available commands
    print("\n🛠️  Commands:")
    print("   image    - Generate image from text")
    print("   i2i      - Generate image from reference image(s)")
    print("   video    - Generate video from text")
    print("   campaign - Generate full marketing campaign")
    print("   story    - Generate multi-page marketing story with HTML")
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
            duration=args.video_duration,
        )
        
        print(f"\n🎬 Recommended Model: {selection['name']}")
        print(f"   Duration: {args.video_duration}s")
        print(f"   Quality score: {selection['quality_score']}/10")
        print(f"   Speed score: {selection['speed_score']}/10")
        
        print(f"\n💵 Cost Breakdown:")
        print(f"   Per video: ${selection['estimated_cost_usd']:.3f}")
        print(f"   Quantity: {args.quantity}")
        print(f"   Total: ${selection['estimated_cost_usd'] * args.quantity:.2f}")
        
        print(f"\n📊 Alternative Options:")
        for alt in selection['alternatives'][:4]:
            alt_total = alt['estimated_cost'] * args.quantity
            print(f"   • {alt['model']:<20} ${alt_total:.2f} (Q:{alt['quality']}/10, S:{alt['speed']}/10)")
    
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
    vid_parser.add_argument("--duration", type=int, default=5,
                          help="Duration in seconds 5-10 (default: 5)")
    vid_parser.add_argument("--resolution",
                          choices=["480p", "720p", "1080p", "2k"],
                          help="Output resolution (default: model decides)")
    vid_parser.add_argument("--model", default="auto",
                          help="Model to use - seedance-1.5-pro, seedance-1.0-pro (default: auto-select)")
    vid_parser.add_argument("--quality", default="standard",
                          choices=["draft", "standard", "high", "premium"],
                          help="Quality level - affects model selection (default: standard)")
    vid_parser.add_argument("--urgency", default="normal",
                          choices=["asap", "normal", "flexible"],
                          help="Speed priority - asap prefers faster models (default: normal)")
    vid_parser.add_argument("--estimate", action="store_true",
                          help="Show cost estimate only - do not generate")
    vid_parser.add_argument("--audio", action="store_true", default=True,
                          help="Generate audio for the video (default: True)")
    vid_parser.add_argument("--no-audio", action="store_false", dest="audio",
                          help="Disable audio generation")
    vid_parser.add_argument("--watermark", action="store_true", default=False,
                          help="Include watermark (default: False)")
    vid_parser.add_argument("--output", "-o", help="Output JSON file")
    vid_parser.add_argument("--verbose", "-v", action="store_true",
                          help="Show detailed selection reasoning")
    vid_parser.add_argument("--caption", help="Caption text for channel post")
    vid_parser.add_argument("--telegram-chat", help="Channel/chat ID (overrides default)")
    
    # Campaign command
    camp_parser = subparsers.add_parser("campaign", help="Generate full marketing campaign (fresh visuals, no reference images)")
    camp_parser.add_argument("--product", required=True, help="Product name/description")
    camp_parser.add_argument("--audience", required=True, help="Target audience")
    camp_parser.add_argument("--platform", default="instagram",
                          choices=["instagram", "tiktok", "linkedin", "twitter", "youtube"],
                          help="Target platform (default: instagram)")
    camp_parser.add_argument("--video", action="store_true",
                          help="Generate video instead of image")
    camp_parser.add_argument("--duration", type=int, default=5,
                          help="Video duration in seconds 4-10 (if --video)")
    camp_parser.add_argument("--output", "-o", help="Output JSON file")
    camp_parser.add_argument("--telegram-chat", help="Channel/chat ID (overrides default)")
    
    # Story command
    story_parser = subparsers.add_parser("story", help="Generate cohesive marketing story with landing page")
    story_parser.add_argument("--product", required=True, help="Product name/description")
    story_parser.add_argument("--theme", default="sustainable-adventure",
                          choices=["sustainable-adventure", "luxury-lifestyle", "tech-innovation", 
                                   "wellness-health", "family-home"],
                          help="Marketing theme/story archetype (default: sustainable-adventure)")
    story_parser.add_argument("--pages", type=int, default=4,
                          help="Number of story sections/pages: 3-6 (default: 4)")
    story_parser.add_argument("--include-video", action="store_true",
                          help="Include video generation for key sections")
    story_parser.add_argument("--platform", default="instagram",
                          choices=["instagram", "tiktok", "linkedin", "twitter", "youtube"],
                          help="Target platform for visuals (default: instagram)")
    story_parser.add_argument("--style", default="cinematic",
                          choices=["cinematic", "product", "lifestyle", "minimal"],
                          help="Visual style (default: cinematic)")
    story_parser.add_argument("--quality", default="standard",
                          choices=["draft", "standard", "high", "premium"],
                          help="Quality level (default: standard)")
    story_parser.add_argument("--estimate", action="store_true",
                          help="Show cost estimate only - do not generate")
    story_parser.add_argument("--output", "-o", help="Output directory (default: ./marketing_story)")
    story_parser.add_argument("--reference-image", "-r", action="append",
                          help="Reference product image(s) to build story around (URL or file path). Can be used multiple times for multiple images.")
    story_parser.add_argument("--use-original", action="store_true",
                          help="Use the original reference image directly in the story ( Solution section) without generating variations")
    
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
    needs_api_key = args.command in ["image", "i2i", "video", "campaign", "status", "story"]
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
        "story": cmd_story,
        "status": cmd_status,
        "estimate": cmd_estimate,
        "models": cmd_models,
        "version": cmd_version,
    }
    
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())

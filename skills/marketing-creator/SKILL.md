# Marketing Creator Skill

**Version:** 1.5.0  
**Last Updated:** 2026-03-22

### v1.5.0 (2026-03-22)
- **Product Photo Integration** - Build stories around your own product images
  - `--reference-image` flag to use your product photos as reference
  - `--use-original` flag to use original image directly in Solution section
  - Image-to-image generation creates consistent product variations across story sections

### v1.4.0 (2026-03-22)
- **Marketing Story Generator** - New `story` command creates cohesive multi-page marketing narratives
  - Generates 3-6 connected sections (Hero, Problem, Solution, Benefits, Social Proof, CTA)
  - AI-designed HTML landing page with responsive layout
  - 5 built-in themes: sustainable-adventure, luxury-lifestyle, tech-innovation, wellness-health, family-home
  - Optional video generation for key sections
  - Ready for Netlify deployment (outputs manifest.json + index.html)

### v1.3.0 (2026-03-22)
- **Removed telegram_poster.py** - No longer depends on Telegram-specific posting
- **Channel Content Delivery** - Now outputs JSON for the calling system to deliver to current channel
- **Configuration simplified** - Removed telegram section from config.json

Generate marketing assets (images AND videos) using BytePlus ModelArk API with intelligent cost optimization. **Supports BOTH text-to-image AND image-to-image generation** for static images.

## Changelog

### v1.2.0 (2026-03-22)
- **Watermark disabled by default** for all image generation
- Improved documentation for image-to-image capabilities

### v1.1.0 (2026-03-22)
- **Added Image-to-Image support** for static images using Seedream 4.0 and 4.5
- New `i2i` CLI command for image-to-image generation
- Auto-model selection: detects I2I needs and picks appropriate model
- Support for: editing, style transfer, multi-image fusion, variations, image sets

### v1.0.0 (Initial)
- Text-to-image generation using Seedream models
- Video generation using Seedance models
- Smart model selection based on quality/cost
- Channel content delivery

## Capabilities

- **Text-to-Image Generation**: Create marketing images from text descriptions using Seedream models
- **Image-to-Image Generation**: Transform, edit, or fuse **static images** using reference images
  - **Edit existing images**: Remove backgrounds, add/remove elements, modify colors
  - **Style transfer**: Apply artistic styles from one image to another
  - **Multi-image fusion**: Combine 2-10 images into one cohesive image
  - **Generate variations**: Create multiple versions of a product/logo while preserving the subject
  - **Image set generation**: Generate up to 14 related images for campaigns
  - **Uses Seedream 4.0 or 4.5** - these are STATIC image models with I2I support
- **Video Generation**: Create marketing videos using Seedance models (also supports image-to-video)
- **Campaign Workflow**: End-to-end campaign creation with concepts, copy, and visuals
- **Multi-platform**: Generate assets optimized for different platforms (Instagram, TikTok, LinkedIn, etc.)
- **Smart Model Selection**: Automatically picks optimal model for quality/cost balance
- **Cost Estimation**: Preview costs before generating
- **Marketing Story Generator**: Create cohesive multi-page marketing narratives with AI-designed landing pages, ready for Netlify deployment
- **Channel Content Delivery**: ALL generated images/videos are returned for posting to the current channel - no download links provided to users

### Image Generation Modes

| Mode | Input | Output | Command |
|------|-------|--------|---------|
| **Text-to-Image** | Text prompt | Static image | `./marketing.py image "prompt"` |
| **Image-to-Image** | Text prompt + Reference image(s) | Static image | `./marketing.py i2i "prompt" -r image.jpg` |
| **Image-to-Video** | Text prompt + Reference image(s) | Video | `./marketing.py video "prompt" --reference-images img.jpg` |

## ⚠️ CRITICAL RULE: Automatic Channel Posting

**ALL generated images, videos, or files MUST be posted directly to the current channel. It is ABSOLUTELY PROHIBITED to tell users to download files from any location. The files must appear in the conversation automatically.**

### Why This Rule Exists
- Users should receive content directly in their conversation
- No external downloads, links, or "click here to get your file" messages
- Generated assets appear as native messages in the channel

### How to Follow This Rule
1. When generating any image/video/file, ALWAYS use the channel posting mechanism
2. NEVER provide URLs or download links to users
3. NEVER ask users to "download from" or "get your file at" any location
4. The file must be delivered as a post in the current channel/chat

### Technical Implementation
- All generation commands automatically post to the configured channel
- The `telegram_poster.py` module handles posting to Telegram channels
- File URLs are used internally for posting, never shown to users
- If posting fails, retry or inform user of failure - never provide raw URLs as workaround

## Setup

### Quick Install

```bash
cd skills/marketing-creator
pip install -r requirements.txt
```

Or use the install script:
```bash
./install.sh
```

### Dependencies

The skill requires the following packages:

| Package | Required For | Install Command |
|---------|--------------|-----------------|
| `requests` | Image generation | `pip install requests` |
| `byteplus-python-sdk-v2` | Video generation | `pip install byteplus-python-sdk-v2` |
| `pydantic` | Video generation | `pip install pydantic` |

**Note:** Video generation requires the BytePlus SDK (`byteplus-python-sdk-v2` + `pydantic`). Image generation works with just `requests`.

### API Key Configuration

API key should be configured in `config.json`:
```json
{
  "api_key": "your-byteplus-api-key"
}
```

Get your API key from: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey

### Verify Installation

```bash
python3 test_setup.py
```

Alternatively, you can override via environment variable:
```bash
export ARK_API_KEY="your-byteplus-api-key"
```

Get your API key from: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey

### ⚠️ Important: Activate Models

Before using image/video generation, you must **activate the models** in the BytePlus console:

1. Go to https://console.byteplus.com/ark/
2. Click **"Model activation"** in the left sidebar
3. Select **"Media"** category
4. Activate **Seedream** (for images) and/or **Seedance** (for videos)

**Note:** Model activation is separate from API key creation. Without activation, you'll get "model not found" errors.

## Quick Start

> **NOTE:** This skill supports BOTH text-to-image AND image-to-image for **static images**.
> Use `image` command for text-to-image, `i2i` command for image-to-image.

```bash
# Generate a marketing image (TEXT-TO-IMAGE) - outputs JSON for channel delivery
./marketing.py image "Luxury perfume product shot, elegant glass bottle on marble surface"

# Generate with specific quality (affects model selection)
./marketing.py image "Product shot" --quality premium

# Preview cost before generating
./marketing.py image "Product shot" --estimate

# IMAGE-TO-IMAGE: Edit an existing image (generate NEW static image from reference)
./marketing.py i2i "Remove the background, keep only the product" -r product_photo.jpg

# IMAGE-TO-IMAGE: Style transfer (generate NEW styled image)
./marketing.py i2i "Apply anime style to this photo" -r portrait.jpg --mode style_transfer

# IMAGE-TO-IMAGE: Multi-image fusion - combine 2+ images into one
./marketing.py i2i "Place the person from image 1 into the background from image 2" \
  -r person.jpg background.jpg --mode fusion

# IMAGE-TO-IMAGE: Generate variations from a reference image
./marketing.py i2i "Create different variations of this logo for seasons" \
  -r logo.jpg --mode image_set --count 4

# Generate a marketing video (requires SDK) - outputs JSON for channel delivery
./marketing.py video "Cinematic drone shot of modern skyscraper at sunset"

# Create a full campaign - outputs JSON for channel delivery
./marketing.py campaign --product "Organic Coffee" --audience "health-conscious millennials"

# Get batch cost estimate
./marketing.py estimate image --quantity 20 --quality standard

# All commands output JSON that the calling system uses to post to current channel
```

## Marketing Story Generator

Create cohesive multi-page marketing narratives with AI-generated landing pages, ready for Netlify deployment.

### Story Command

```bash
# Generate a 4-page marketing story (default)
./marketing.py story --product "Eco-Friendly Water Bottle" --theme sustainable-adventure

# Build story around your product photo
./marketing.py story --product "Smart Watch" --theme tech-innovation --reference-image ./product-photo.jpg

# Use original photo in Solution section, generate variations for other sections
./marketing.py story --product "Luxury Skincare" --theme luxury-lifestyle \
  --reference-image ./product.jpg --use-original

# Preview cost before generating
./marketing.py story --product "Smart Watch" --theme tech-innovation --estimate

# Include video for hero and CTA sections
./marketing.py story --product "Luxury Skincare" --theme luxury-lifestyle --include-video

# Generate 6-page comprehensive story
./marketing.py story --product "Organic Tea" --theme wellness-health --pages 6

# Custom output directory
./marketing.py story --product "Baby Products" --theme family-home --output ./my-story
```

### Available Themes

| Theme | Style | Best For |
|-------|-------|----------|
| `sustainable-adventure` | Earthy greens, natural | Eco-friendly products |
| `luxury-lifestyle` | Black, gold, elegant | Premium/high-end products |
| `tech-innovation` | Dark blue, cyan accents | Tech/gadget products |
| `wellness-health` | Soft greens, warm neutrals | Health/wellness products |
| `family-home` | Warm browns, cozy feel | Family/home products |

### Building Stories Around Your Product Photos

You can attach your own product photos and the story will be built around them:

```bash
# Use your product photo as reference for all sections
./marketing.py story --product "My Product" --reference-image ./my-product.jpg

# Use multiple reference images
./marketing.py story --product "My Product" \
  --reference-image ./product-front.jpg \
  --reference-image ./product-in-use.jpg

# Use original image directly in Solution section (no generation)
./marketing.py story --product "My Product" \
  --reference-image ./product.jpg \
  --use-original
```

**How it works:**
- **Without `--reference-image`**: AI generates all visuals from text prompts
- **With `--reference-image`**: Uses image-to-image generation to create variations of your product
- **With `--use-original`**: Uses your original photo for the Solution section, generates variations for other sections

**Best practices:**
- Use clear, well-lit product photos
- The AI will maintain product identity while adapting to different contexts
- Works with URLs (`https://...`) or local file paths

### Story Structure (Sections)

| Section | Purpose | Video? |
|---------|---------|--------|
| **Hero** | Grab attention with emotional hook | ✅ Optional |
| **Problem** | Agitate the pain point | ❌ |
| **Solution** | Present product as answer | ✅ Optional |
| **Benefits** | Show key advantages | ❌ |
| **Social Proof** | Build trust with testimonials | ❌ |
| **CTA** | Drive action | ✅ Optional |

### Output Files

When you run the story command, it creates:

```
marketing_story/                    # or your --output directory
├── index.html                      # Complete landing page
├── story_manifest.json             # Metadata for Netlify deployment
└── (assets embedded via URLs)      # Images/videos from BytePlus
```

### Netlify Integration

The story output is ready for Netlify deployment:

```bash
# After generating story
cd marketing_story

# Deploy to Netlify (using netlify skill)
netlify deploy --prod --message "Marketing story for Eco Bottle"
```

### Image vs Video Generation

| Feature | Image (Seedream) | Video (Seedance) |
|---------|------------------|------------------|
| **SDK Required** | No (REST API) | Yes (`byteplus-python-sdk-v2`) |
| **Endpoint** | `/api/v3/images/generations` | `content_generation.tasks` |
| **Cost** | $0.03-0.04/image | $0.001-0.003/K tokens |
| **Min Size** | 1024x1024 (921600 pixels) | 480p, 720p, 1080p, 2K |

## Smart Model Selection

The skill automatically selects the optimal model based on your requirements:

### Auto-Detection Rules

The skill automatically detects what type of generation you need and picks the right model:

| Generation Type | Input | Auto-Selected Model | Why |
|----------------|-------|---------------------|-----|
| **Text-to-Image** | Text prompt only | `seedream-5.0` | Best quality for text-based generation |
| **Image-to-Image** | Text + reference image(s) | `seedream-4.0` or `seedream-4.5` | Only models supporting image-to-image |
| **Multi-image Fusion** | Text + 3+ reference images | `seedream-4.5` | Better quality for complex fusion tasks |

### Quality Levels
| Level | Use Case | Text-to-Image | Image-to-Image | Video Model/Resolution |
|-------|----------|---------------|----------------|------------------------|
| `draft` | Quick iterations, concepts | Seedream 3.0 | Seedream 4.0 | Seedance Lite @ 480p-720p |
| `standard` | Most social content | Seedream 5.0 | Seedream 4.0 | Seedance Lite @ 720p-1080p |
| `high` | Professional marketing | Seedream 5.0 | Seedream 4.5 | Seedance Pro @ 1080p |
| `premium` | Print, high-end ads | Seedream 5.0 | Seedream 4.5 | Seedance Pro @ 1080p-2K |

### Platform Optimizations
| Platform | Image Size | Video Resolution | Notes |
|----------|------------|------------------|-------|
| Instagram | 1080x1080 | 1080p | Balanced quality |
| TikTok | 1080x1920 | 720p | Mobile-optimized, cost-effective |
| YouTube | 1280x720 | 1080p | Professional look |
| LinkedIn | 1200x627 | 1080p | Business-appropriate |
| Twitter | 1200x675 | 1080p | Feed-optimized |

### Cost Optimization Flags
```bash
--quality draft      # Lowest cost (~$0.01/image)
--quality standard   # Balanced (default)
--quality high       # Professional
--quality premium    # Maximum quality
--urgency asap       # Prioritize speed over cost
--has-text           # Use higher quality for text clarity
--estimate           # Preview cost without generating
```

### Examples
```bash
# Draft for quick iteration (cheapest)
./marketing.py image "Coffee cup concept" --quality draft

# Estimate batch cost for 50 images
./marketing.py estimate image --quantity 50 --quality standard

# High-quality product shot with text
./marketing.py image "Sale 50% Off" --quality high --has-text

# Urgent request - fastest generation
./marketing.py image "Breaking news graphic" --urgency asap
```

## Image-to-Image Generation (for Static Images)

**IMPORTANT:** The marketing-creator skill supports image-to-image generation for **STATIC IMAGES** (not just videos). You can provide a reference image and generate a new static image based on it.

Use this for:
- **Editing product photos**: Remove backgrounds, change colors, add elements
- **Style transfer**: Make a photo look like a painting, sketch, or 3D render
- **Multi-image fusion**: Combine product + background + props into one image
- **Generate variations**: Create seasonal versions of a logo or product shot
- **Subject preservation**: Keep a character/product consistent across different scenes

### How It Works

1. **Input**: Text prompt + 1-10 reference images (URLs or file paths)
2. **Processing**: Seedream 4.0 or 4.5 analyzes the reference images and generates a new static image
3. **Output**: A new JPEG image (1K-4K resolution) that incorporates elements from the reference images

**Models Used:** `seedream-4.0` or `seedream-4.5` (both support image-to-image for static outputs)

**Auto-Model Selection:** The skill automatically selects `seedream-4.0` or `seedream-4.5` based on your quality requirements and the number of reference images.

### Generation Modes

| Mode | Description | Use Cases | Images Needed |
|------|-------------|-----------|---------------|
| `single` | Single image → single image | Edit, enhance, or modify one image | 1 |
| `fusion` | Multi-image → single image | Combine elements from multiple images | 2-10 |
| `style_transfer` | Apply style from reference | Match brand style, artistic effects | 1 |
| `edit` | Add/remove/modify elements | Remove backgrounds, add objects | 1 |
| `subject_preservation` | Keep subject consistent | Product variations, character poses | 1 |
| `image_set` | Generate related image set | Campaign series, seasonal variations | 1 |

### Supported Models

| Model | Cost | Best For |
|-------|------|----------|
| `seedream-4.0` | $0.03/image | Standard image-to-image, editing |
| `seedream-4.5` | $0.04/image | Higher quality, complex fusions |

### CLI Examples

```bash
# Edit an image - remove background
./marketing.py i2i "Remove the background, keep only the smartphone" \
  -r product_photo.jpg --mode edit

# Style transfer - apply anime style
./marketing.py i2i "Apply anime style, keep the character pose" \
  -r portrait.jpg --mode style_transfer --platform instagram

# Multi-image fusion - combine product with lifestyle background
./marketing.py i2i "Place the product from image 1 on the table from image 2" \
  -r product.jpg lifestyle_bg.jpg --mode fusion

# Subject preservation - generate variations
./marketing.py i2i "Show this watch in different lighting conditions" \
  -r watch.jpg --mode subject_preservation --count 4

# Image set generation - create campaign series
./marketing.py i2i "Create seasonal variations of this logo" \
  -r logo.jpg --mode image_set --count 4 --platform instagram

# Preview cost
./marketing.py i2i "Edit image" -r photo.jpg --estimate --count 3
```

### Prompt Tips for Image-to-Image

**For Editing:**
- Be specific about what to change: "Remove the red car and replace with a blue bicycle"
- Mention what to keep: "Keep the background, change only the foreground subject"

**For Style Transfer:**
- Reference the style explicitly: "Apply the artistic style from the reference image"
- Specify content changes: "Keep the pose, change the outfit color to blue"

**For Multi-Image Fusion:**
- Describe which image provides which element: "Use image 1 as the subject, image 2 as background"
- Specify composition: "Place the person from image 1 into the scene from image 2"

**For Image Sets:**
- Trigger with keywords: "a series", "a set", "different variations"
- Specify the relationship: "four scenes in spring, summer, autumn, winter"

## Models Available

### Image Generation (Seedream)
| Model | Cost | Quality | Speed | Best For | Image-to-Image |
|-------|------|---------|-------|----------|----------------|
| `seedream-4.0` | $0.03 | 8/10 | 8/10 | Standard social content | ✅ Yes |
| `seedream-4.5` | $0.04 | 9/10 | 7/10 | Marketing materials | ✅ Yes |
| `seedream-5.0` | $0.035 | 10/10 | 6/10 | Premium quality | ❌ No |

### Video Generation (Seedance)
| Model | Cost | Quality | Speed | Best For |
|-------|------|---------|-------|----------|
| `seedance-1.0-lite-t2v` | $0.0010/K tokens | 6/10 | 9/10 | Social stories, quick content |
| `seedance-1.0-pro` | $0.0024/K tokens | 8/10 | 7/10 | Professional ads, presentations |
| `seedance-1.0-pro-fast` | $0.0017/K tokens | 8/10 | 9/10 | Fast production, social content |
| `seedance-1.5-pro` | $0.0030/K tokens | 10/10 | 6/10 | Premium content, cinematic |

Video costs scale by resolution:
- 480p: 0.5x base cost
- 720p: 1.0x base cost
- 1080p: 2.5x base cost
- 2K: 3.5x base cost

## Channel Content Delivery (REQUIRED)

**Every generated asset is returned in JSON format for delivery to the current channel.** This is not optional - it is a mandatory behavior.

### How It Works

All generation commands output JSON that includes generated content metadata:

```bash
# Image is generated and JSON output includes URLs for channel delivery
./marketing.py image "Product shot"
# Output: {"type": "image_generation", "success": true, "images": [...], ...}

# Video is generated and JSON output includes URL for channel delivery
./marketing.py video "Product demo"
# Output: {"type": "video_generation", "success": true, "video_url": "...", ...}

# Campaign assets are returned with formatted metadata
./marketing.py campaign --product "Organic Tea" --audience "health enthusiasts"
```

### What Users See

✅ **CORRECT:**
- User: "Generate an image of a luxury watch"
- AI: "I'll generate that marketing image for you..." → [Image appears in channel automatically]

❌ **WRONG (NEVER DO THIS):**
- User: "Generate an image of a luxury watch"
- AI: "Here's your image: https://example.com/image.jpg" ← NEVER PROVIDE RAW URLs
- AI: "Download your file from: [link]" ← NEVER DO THIS
- AI: "Click here to get your image" ← NEVER DO THIS

### Implementation Details

The skill outputs JSON that the calling system (Kimi/Claw) uses to post content:
- Image generation: Returns `images` array with URLs
- Video generation: Returns `video_url`
- Campaign: Returns `assets` array with campaign metadata

URLs are used internally for channel integration - they are NEVER displayed to the user.

## API Reference

### Image Generation with Auto Model Selection (Auto-Posts to Channel)
```python
from byteplus_client import generate_marketing_image
from telegram_poster import TelegramPoster

# Text-to-Image: Automatically uses seedream-5.0
result = generate_marketing_image(
    prompt="Luxury watch product shot, golden hour lighting",
    platform="instagram",
    quality="standard",  # Auto-selects based on quality
)

# Image-to-Image: Automatically detects and uses seedream-4.0/4.5
result = generate_marketing_image(
    prompt="Remove the background, keep only the product",
    image_urls=["https://example.com/product.jpg"],  # Triggers I2I mode
    platform="instagram",
    quality="high",  # Auto-selects seedream-4.5 for high quality
)

# CRITICAL: Always post to channel, never give URL to user
if result["success"]:
    poster = TelegramPoster()
    for img in result["images"]:
        poster.post_image(img["url"], caption="Generated image")
```

### Image-to-Image Generation (Static Images - Returns Content for Channel)
```python
from byteplus_client import BytePlusClient, generate_marketing_image_i2i

client = BytePlusClient()

# All examples below generate NEW static images from reference images
# Uses seedream-4.0 or seedream-4.5 (NOT video models)

# Single image editing
result = client.edit_image(
    prompt="Remove the background, keep only the product",
    image_path="https://example.com/product.jpg",
    model="seedream-4.0",
    size="2K"
)

# Style transfer
result = client.style_transfer(
    content_prompt="A modern office interior",
    style_image="https://example.com/anime_style.jpg",
    model="seedream-4.0"
)

# Multi-image fusion
result = client.fuse_images(
    images=["person.jpg", "background.jpg", "props.jpg"],
    prompt="Place the person in the background with the props",
    model="seedream-4.5"
)

# Generate variations
result = client.generate_variations(
    reference_image="logo.jpg",
    prompt="Create different seasonal variations",
    n=4,
    model="seedream-4.0"
)

# General image-to-image with mode selection
result = client.generate_image_to_image(
    prompt="Your transformation prompt",
    reference_images=["image1.jpg", "image2.jpg"],
    model="seedream-4.0",
    mode="fusion",  # single, fusion, style_transfer, edit, subject_preservation, image_set
    n=1
)

# Convenience function with platform optimization
result = generate_marketing_image_i2i(
    prompt="Apply cinematic lighting",
    reference_images=["product.jpg"],
    mode="edit",
    platform="instagram",
    style="product"
)

# CRITICAL: Return content for channel delivery, never give URL to user directly
if result["success"]:
    output = {
        "type": "image_to_image_generation",
        "success": True,
        "images": result["images"],
    }
    print(json.dumps(output))
```

### Video Generation (Returns Content for Channel)
```python
# Async pattern - submit job and poll
response = requests.post(
    "https://api.byteplus.com/seedance/v1/videos",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "seedance-1-0-pro-250528",
        "prompt": "Your prompt",
        "resolution": "1080p",
        "duration": 5,
        "aspect_ratio": "16:9",
        "audio": True
    }
)
job_id = response.json()["id"]

# Poll for completion and get video URL
# ... polling logic ...
video_url = status.json()["video_url"]

# CRITICAL: Return content for channel delivery, never give URL to user directly
output = {
    "type": "video_generation",
    "success": True,
    "video_url": video_url,
    "caption": "Generated marketing video",
}
print(json.dumps(output))
```

### CRITICAL RULE REMINDER
```python
# ❌ WRONG - Never do this:
print(f"Here's your image: {image_url}")
print(f"Download from: {video_url}")

# ✅ CORRECT - Always return content for channel delivery:
output = {
    "type": "image_generation",
    "success": True,
    "images": [{"url": image_url}],
    "caption": "Generated marketing image",
}
print(json.dumps(output))
# The calling system will handle posting to the current channel
```

## Pricing (Estimated)

| Model | Resolution | Cost per Generation |
|-------|------------|---------------------|
| Seedream 4.0 (Image/Text-to-Image) | 1024x1024 | $0.03 |
| Seedream 4.0 (Image-to-Image) | 1024x1024 | $0.03 |
| Seedream 4.5 (Image-to-Image) | 1024x1024 | $0.04 |
| Seedream 5.0 (Image/Text-to-Image) | 1024x1024 | $0.035 |
| Seedance (Video) | Varies | Per token pricing |

**Image-to-Image Notes:**
- Same pricing as text-to-image for the same model
- Multi-image fusion counts as 1 generation (1 output image)
- Image set generation counts as N generations (N output images)

## Deployment

Deploy the marketing-creator skill to a remote host (e.g., kai) via SSH.

### Deploy to kai

```bash
# Deploy to default host (kai)
./deploy.py

# Deploy to specific host
./deploy.py --host myserver

# Deploy and verify
./deploy.py --verify

# Deploy and test
./deploy.py --test
```

### What Gets Deployed

The deployment script will:
1. Connect to the remote host via SSH
2. Create the skill directory: `/home/ubuntu/.config/agents/skills/marketing-creator`
3. Copy all skill files (Python scripts, configs, etc.)
4. Install Python dependencies on the remote host
5. Make scripts executable

### Manual Deployment

If you prefer manual deployment:

```bash
# Create remote directory
ssh kai "mkdir -p /home/ubuntu/.config/agents/skills/marketing-creator"

# Copy files
scp *.py *.json *.txt *.sh kai:/home/ubuntu/.config/agents/skills/marketing-creator/

# Install dependencies on remote
ssh kai "cd /home/ubuntu/.config/agents/skills/marketing-creator && pip install -r requirements.txt"

# Make executable
ssh kai "chmod +x /home/ubuntu/.config/agents/skills/marketing-creator/marketing.py"
```

### Post-Deployment Configuration

After deployment, SSH into kai and configure:

```bash
ssh kai
cd ~/.config/agents/skills/marketing-creator

# Edit config.json with API keys
nano config.json

# Test the installation
python3 test_setup.py

# Generate a test image
./marketing.py image "Test product shot" --estimate
```

## File Structure

```
skills/marketing-creator/
├── SKILL.md              # This file
├── config.json           # API keys and configuration
├── requirements.txt      # Python dependencies
├── install.sh            # Installation script
├── marketing.py          # Main CLI tool - outputs JSON for channel delivery
├── byteplus_client.py    # BytePlus API client wrapper (includes image-to-image)
├── model_selector.py     # Smart model selection engine
├── deploy.py             # Deployment script to remote hosts
├── api_reference.py      # Complete API documentation
├── test_setup.py         # Setup verification script
└── examples/             # Example prompts and outputs
    └── prompts.md
```

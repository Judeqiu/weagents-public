# Example Marketing Prompts

## Telegram Posting Examples

### Generate and Post to Telegram

```bash
# Generate image and auto-post to default Telegram chat
./marketing.py image "Premium wireless earbuds floating, studio lighting" --post-to-telegram

# Generate with custom caption
./marketing.py image "New summer collection" --post-to-telegram --caption "☀️ Summer vibes are here! Check out our new collection."

# Generate video and post
./marketing.py video "Product 360 rotation" --post-to-telegram --caption "See it from every angle 🎬"

# Post to specific channel
./marketing.py image "Flash sale graphic" --post-to-telegram --telegram-chat "@yourbrandchannel"

# Full campaign with Telegram posting
./marketing.py campaign \
    --product "Organic Matcha" \
    --audience "health enthusiasts" \
    --platform instagram \
    --post-to-telegram
```

### Telegram Setup Required

Add to `config.json`:
```json
{
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN_FROM_BOTFATHER",
    "default_chat_id": "YOUR_CHAT_ID",
    "enabled": true
  }
}
```

Get bot token from [@BotFather](https://t.me/botfather)
Get chat ID from [@userinfobot](https://t.me/userinfobot)

## Smart Model Selection Examples

The marketing creator automatically selects the optimal model based on your requirements. Use `--quality` and `--estimate` flags to control cost and preview expenses.

### Quality Levels & Expected Costs

| Quality | Image Cost | Video Cost (5s) | Best For |
|---------|-----------|-----------------|----------|
| `draft` | ~$0.01 | ~$0.03-0.05 | Quick concepts, iterations |
| `standard` | ~$0.02 | ~$0.05-0.25 | Most social media content |
| `high` | ~$0.03 | ~$0.25-0.50 | Professional marketing |
| `premium` | ~$0.05 | ~$0.50-0.75 | High-end campaigns, print |

### Preview Costs Before Generating

```bash
# See cost estimate before generating
./marketing.py image "Product concept" --quality standard --estimate

# Compare different quality levels
./marketing.py image "Product concept" --quality draft --estimate
./marketing.py image "Product concept" --quality premium --estimate

# Batch cost estimation
./marketing.py estimate image --quantity 50 --quality standard
./marketing.py estimate video --quantity 10 --quality high --video-resolution 1080p
```

### Platform-Optimized Generation

```bash
# TikTok (auto-selects 720p for mobile)
./marketing.py video "Dance trend" --platform tiktok --quality standard

# Instagram Reels (auto-selects 1080p)
./marketing.py video "Product showcase" --platform instagram --quality high

# YouTube (auto-selects 1080p-2K)
./marketing.py video "Brand story" --platform youtube --quality premium
```

## Image Generation Examples

### Product Photography
```bash
./marketing.py image "Premium wireless earbuds floating in mid-air, soft studio lighting, gradient background from navy to electric blue, reflection on glossy black surface, commercial product photography, 8K detail, Apple-style aesthetic"
```

### Lifestyle
```bash
./marketing.py image "Young professional woman working on laptop in modern coworking space, natural window lighting, plants in background, candid authentic moment, warm tones, lifestyle brand photography" --platform instagram --style lifestyle
```

### Food/Beverage
```bash
./marketing.py image "Artisan coffee cup from above, latte art visible, marble table surface, morning sunlight, steam rising, cozy cafe atmosphere, food photography, appetizing warm colors" --platform instagram
```

### Tech/Innovation
```bash
./marketing.py image "Futuristic AI chip visualization, glowing neural pathways, deep blue and purple color scheme, holographic elements, cinematic lighting, tech company keynote aesthetic" --style cinematic
```

### Fashion
```bash
./marketing.py image "Elegant minimalist fashion lookbook shot, model in neutral tones, clean white studio background, soft diffused lighting, high-end editorial style, Vogue aesthetic" --platform instagram
```

## Video Generation Examples

### Product Showcase
```bash
./marketing.py video "Smooth 360-degree camera orbit around premium smartwatch on display stand, dramatic product lighting highlighting metal finish, luxury timepiece aesthetic, shallow depth of field" --platform youtube --resolution 1080p --duration 8
```

### Social Media Hook
```bash
./marketing.py video "Fast-paced product unboxing sequence, hands opening premium packaging, reveal moment with satisfying peel, top-down camera angle, trendy social media style" --platform tiktok --resolution 720p --duration 5
```

### Brand Story
```bash
./marketing.py video "Cinematic sunrise over mountain landscape, slow pan across golden peaks, peaceful nature scene, aspirational outdoor brand aesthetic, inspiring and uplifting mood" --platform instagram --duration 10
```

### App/Software Demo
```bash
./marketing.py video "Abstract visualization of data flowing through network, glowing connection points, UI elements floating in 3D space, SaaS company aesthetic, professional tech visualization" --platform linkedin --resolution 1080p
```

## Campaign Examples

### Full Campaign - Beauty Product
```bash
./marketing.py campaign --product "Organic Vitamin C Serum" --audience "health-conscious women 25-40" --platform instagram
```

### Full Campaign - Tech Gadget
```bash
./marketing.py campaign --product "AI-Powered Smart Home Hub" --audience "tech-savvy early adopters" --platform youtube --video --duration 8
```

### Full Campaign - Food Brand
```bash
./marketing.py campaign --product "Plant-Based Protein Bars" --audience "fitness enthusiasts and busy professionals" --platform tiktok
```

## Platform-Specific Tips

### Instagram
- Use square (1:1) or portrait (4:5) for feed posts
- Use 9:16 for Reels and Stories
- Style: Polished, aesthetic, aspirational
- Best models: seedream-5.0 for images

### TikTok
- Always use 9:16 vertical format
- Hook in first 1-2 seconds
- Style: Authentic, energetic, trending
- Best resolution: 720p for faster generation

### YouTube
- Use 16:9 for standard videos
- Use high resolution (1080p or 2K)
- Style: Professional, narrative-driven
- Longer durations (8-15s) work well

### LinkedIn
- Use 16:9 or 1:1
- Style: Professional, informative
- Avoid overly salesy imagery
- Focus on value proposition

## Prompt Engineering Tips

### Strong Prompts Include:
1. **Subject**: What is the main focus?
2. **Setting**: Where is it? What's the environment?
3. **Lighting**: Natural, studio, dramatic, golden hour?
4. **Style**: Cinematic, minimalist, lifestyle, commercial?
5. **Quality markers**: 8K, professional photography, detailed

### Example Formula:
```
[Subject] + [Setting/Background] + [Lighting] + [Camera/Style] + [Quality]
```

### Before/After:
- Weak: "A car driving"
- Strong: "Red sports car driving along winding coastal highway at golden hour, camera tracking from the side, ocean waves visible in background, cinematic depth of field, commercial automotive photography"

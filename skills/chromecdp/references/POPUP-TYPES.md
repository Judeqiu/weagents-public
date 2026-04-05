# Popup Types and Handling Strategies

## Overview

The popup handler detects and manages common blocking UI elements that interfere with automation.

## Supported Popup Types

### 1. Cookie Consent Banners

**Visual indicators:**
- Banner at top/bottom of page
- "Accept Cookies", "Got it", "I Agree" buttons
- Privacy policy links

**Common selectors:**
```css
.cc-banner, .cc-window, #onetrust-banner-sdk
[class*="cookie"], [id*="cookie"]
```

**Handling strategy:**
- Look for accept/allow buttons first
- Fallback to dismiss/close if no accept button
- Some banners can be safely ignored if they don't block content

### 2. Warning/Alert Dialogs

**Visual indicators:**
- Centered modal dialogs
- Warning icons
- "Continue", "Dismiss", "OK" buttons

**Common selectors:**
```css
[role="alert"], [role="dialog"]
.alert, .warning, .modal
```

**Handling strategy:**
- Always attempt to close if blocking interaction
- Prefer "Continue" or "OK" over "Cancel" for progress

### 3. Newsletter Signup Overlays

**Visual indicators:**
- Email input field
- "Subscribe", "Join" CTAs
- "No thanks" dismiss option

**Common selectors:**
```css
[class*="newsletter"], [class*="subscribe"]
```

**Handling strategy:**
- Look for "No thanks", "Maybe later", or close button
- Don't interact with email fields

### 4. Age Verification Gates

**Visual indicators:**
- "You must be 18+" messages
- Date of birth input
- "Enter" or "I am 18+" buttons

**Common selectors:**
```css
[class*="age"], [class*="verify"]
```

**Handling strategy:**
- Click "Enter", "Yes", "I am 18" if available
- Some sites require DOB input (manual intervention)

### 5. Permission Requests

**Types:**
- Location access
- Notification permission
- Camera/microphone access

**Handling strategy:**
- Generally should be dismissed/ignored
- Look for "Block" or "Don't allow" options

## Confidence Scoring

The handler uses a confidence score (0-1) to determine if an element is actually a popup:

- **0.8-1.0**: High confidence - multiple indicators match
- **0.5-0.8**: Medium confidence - some indicators match
- **0.4-0.5**: Low confidence - minimal indicators
- **Below 0.4**: Not considered a popup

## Extending Detection

To add new popup types, edit `chromecdp-popup-handler.py`:

```python
POPUP_PATTERNS = {
    "your_popup_type": {
        "selectors": [
            '[class*="your-class"]',
            '#your-id',
        ],
        "text_patterns": [
            r"pattern.*to.*match",
            r"another pattern",
        ],
        "close_selectors": [
            'button:has-text("Close")',
            '.your-close-class',
        ],
    },
    # ... existing patterns
}
```

## Best Practices

1. **Always check for popups after navigation**
2. **Use `--auto-close` for known-safe sites**
3. **Review screenshots after handling to verify**
4. **Add site-specific selectors if needed**
5. **Don't auto-click on payment or confirmation dialogs**

## Safety Warnings

⚠️ **Never auto-close:**
- CAPTCHA challenges
- Payment confirmation dialogs
- Account deletion confirmations
- Legal agreement acceptances
- Two-factor authentication prompts

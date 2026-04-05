# CDP Operations Reference

## Natural Language to Technical Mapping

This reference shows how natural language requests map to browser tool actions.

### Navigation Requests

| Natural Language | Technical Action |
|-----------------|------------------|
| "Open [URL]" | `browser(action: "open", url: "URL", target: "host")` |
| "Go to [URL]" | Same as above |
| "Navigate to [URL]" | Same as above |
| "Visit [URL]" | Same as above |
| "Refresh the page" | `browser(action: "navigate", targetId: ID, url: current_url)` |
| "Go back" | `browser(action: "act", targetId: ID, kind: "evaluate", fn: "history.back()")` |

### Screenshot Requests

| Natural Language | Technical Action |
|-----------------|------------------|
| "Take a screenshot" | `browser(action: "screenshot", type: "png", fullPage: true)` |
| "Show me the page" | Same as above |
| "What does it look like?" | Same as above |
| "Capture [element]" | `browser(action: "screenshot", ref: "e1", type: "png")` |

### Click Requests

| Natural Language | Technical Action |
|-----------------|------------------|
| "Click [element]" | `browser(action: "act", targetId: ID, kind: "click", ref: "e1")` |
| "Press [button]" | Same as above |
| "Select [option]" | Same as above |
| "Tap [element]" | Same as above |
| "Double-click [element]" | `browser(action: "act", targetId: ID, kind: "click", ref: "e1", doubleClick: true)` |

### Typing Requests

| Natural Language | Technical Action |
|-----------------|------------------|
| "Type [text]" | `browser(action: "act", targetId: ID, kind: "type", ref: "e1", text: "text")` |
| "Fill [field] with [text]" | Same as above |
| "Enter [text] in [field]" | Same as above |
| "Input [text]" | Same as above |
| "Clear [field]" | `browser(action: "act", targetId: ID, kind: "evaluate", fn: "document.querySelector('selector').value = ''")` |

### Scrolling Requests

| Natural Language | Technical Action |
|-----------------|------------------|
| "Scroll down" | `browser(action: "act", targetId: ID, kind: "evaluate", fn: "window.scrollBy(0, 800)")` |
| "Scroll up" | `browser(action: "act", targetId: ID, kind: "evaluate", fn: "window.scrollBy(0, -800)")` |
| "Scroll to [element]" | `browser(action: "act", targetId: ID, kind: "click", ref: "e1")` (clicks to scroll into view) |
| "Go to the bottom" | `browser(action: "act", targetId: ID, kind: "evaluate", fn: "window.scrollTo(0, document.body.scrollHeight)")` |
| "Go to the top" | `browser(action: "act", targetId: ID, kind: "evaluate", fn: "window.scrollTo(0, 0)")` |

### Waiting Requests

| Natural Language | Technical Action |
|-----------------|------------------|
| "Wait" | `browser(action: "act", targetId: ID, kind: "wait", timeMs: 2000)` |
| "Wait [X] seconds" | `browser(action: "act", targetId: ID, kind: "wait", timeMs: X*1000)` |
| "Let it load" | Same as "Wait" |
| "Wait for [element]" | `browser(action: "act", targetId: ID, kind: "wait", loadState: "networkidle")` |

### Popup Handling

| Natural Language | Technical Action |
|-----------------|------------------|
| "Close any popups" | `exec("python3 scripts/chromecdp-popup-handler.py --auto-close")` |
| "Handle cookies" | Same as above |
| "Dismiss warnings" | Same as above |
| "Check for popups" | `exec("python3 scripts/chromecdp-popup-handler.py")` |

### Information Extraction

| Natural Language | Technical Action |
|-----------------|------------------|
| "What's on the page?" | `browser(action: "snapshot", targetId: ID)` |
| "Read the content" | Same as above |
| "Find [text]" | `browser(action: "act", targetId: ID, kind: "evaluate", fn: "document.body.innerText.includes('text')")` |
| "Check if [condition]" | Use evaluate with JavaScript condition |

### Form Submissions

| Natural Language | Technical Action |
|-----------------|------------------|
| "Submit the form" | `browser(action: "act", targetId: ID, kind: "press", key: "Enter")` or click submit button |
| "Press Enter" | `browser(action: "act", targetId: ID, kind: "press", key: "Enter")` |

## Multi-Step Workflows

### Login Flow
```
User: "Log me into [site] with username [user] and password [pass]"

Steps:
1. Open the site
2. Check for popups
3. Find and fill username field
4. Find and fill password field
5. Click login button
6. Wait for navigation
7. Take screenshot to confirm
```

### Search Flow
```
User: "Search for [term] on [site]"

Steps:
1. Open the site
2. Check for popups
3. Find search box
4. Type search term
5. Submit search
6. Wait for results
7. Take screenshot
```

### Data Extraction Flow
```
User: "Get the prices from this product page"

Steps:
1. Navigate to page
2. Check for popups
3. Scroll to ensure all content loaded
4. Extract price elements via JavaScript
5. Report findings
```

## Error Handling Patterns

### If Chrome isn't running:
```
1. Run chromecdp-start.sh
2. Wait for it to be ready
3. Retry the operation
```

### If element not found:
```
1. Take screenshot to see current state
2. Check if we need to scroll
3. Check if popups are blocking
4. Try alternative selectors
5. Report what was found instead
```

### If navigation fails:
```
1. Check network connectivity
2. Verify URL is correct
3. Try HTTP vs HTTPS
4. Check if site blocks automation
5. Report the issue
```

## Best Practices

1. **Always check for popups** after navigation
2. **Take screenshots** before and after important actions
3. **Wait appropriately** after clicks and navigation
4. **Scroll into view** before clicking elements
5. **Verify success** with screenshots
6. **Handle errors gracefully** with fallbacks

## Response Templates

### After Navigation:
"I've opened [URL]. Here's what the page looks like: [screenshot]"

### After Click:
"I clicked the [element]. Here's the result: [screenshot]"

### After Typing:
"I've entered [text] in the [field] field. [screenshot]"

### After Handling Popups:
"I found and closed [N] popup(s): [types]. The page is now clear. [screenshot]"

### When Element Not Found:
"I couldn't find [element]. Here's what I see on the page: [screenshot]. Would you like me to try something else?"

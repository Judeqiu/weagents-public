---
name: netlify-deploy
description: "Deploy and manage Netlify sites. Use when: (1) Creating new Netlify sites, (2) Deploying static sites, (3) Managing Netlify functions, (4) Viewing site status, (5) Managing environment variables, (6) Opening Netlify dashboard."
---

# Netlify Deploy

Deploy and manage Netlify sites using the Netlify CLI.

## Prerequisites

### 1. Install Netlify CLI
```bash
npm install -g netlify-cli
```

### 2. Login to Netlify
```bash
# Create login ticket
netlify login --request "OpenClaw agent login"

# Open authorize URL in browser (use Chrome with CDP)
# Then check status
netlify login --check <ticket-id>
```

## Authentication Status

Check if logged in:
```bash
netlify status
```

Expected output:
```
Current Netlify User
Email: your-email@example.com
Teams:
  - Your Team Name
```

## Common Commands

### Site Management

| Command | Description |
|---------|-------------|
| `netlify sites:create` | Create new site |
| `netlify sites:list` | List all sites |
| `netlify sites:delete` | Delete a site |
| `netlify link` | Link current folder to Netlify site |
| `netlify unlink` | Unlink from Netlify site |

### Deployment

| Command | Description |
|---------|-------------|
| `netlify deploy` | Deploy to draft URL |
| `netlify deploy --prod` | Deploy to production |
| `netlify deploy --dir=build` | Deploy specific directory |

### Functions

| Command | Description |
|---------|-------------|
| `netlify functions:create` | Create new function |
| `netlify functions:list` | List deployed functions |
| `netlify functions:invoke` | Invoke a function |

### Environment Variables

| Command | Description |
|---------|-------------|
| `netlify env:list` | List environment variables |
| `netlify env:set KEY=VALUE` | Set environment variable |
| `netlify env:unset KEY` | Remove environment variable |

### Other

| Command | Description |
|---------|-------------|
| `netlify open --admin` | Open site admin dashboard |
| `netlify open --site` | Open live site |
| `netlify build` | Build locally |
| `netlify env:import` | Import env vars from file |

## Workflow

### 1. Login (one-time)
```bash
netlify login --request "OpenClaw agent login"
# Open authorize URL in browser
netlify login --check <ticket-id>
```

### 2. Create or Link Site
```bash
# Create new site
netlify sites:create

# Or link existing site
netlify link
```

### 3. Deploy
```bash
# Deploy to draft
netlify deploy

# Deploy to production
netlify deploy --prod
```

### 4. Open Dashboard
```bash
netlify open --admin
```

## Using with Chrome (Optional)

For visual interaction, open Netlify in Chrome:
```bash
# Using Chrome CDP
node -e "
const CDP = require('chrome-remote-interface');
(async () => {
  const client = await CDP({ port: 9222 });
  const { Page } = client;
  await Page.navigate({ url: 'https://app.netlify.com' });
  await client.close();
})();
"
```

## Notes

- Netlify CLI must be logged in before running commands
- Use `--prod` flag for production deployment
- Default deploy directory is `dist`, use `--dir` for custom
- Functions go in `netlify/functions` folder

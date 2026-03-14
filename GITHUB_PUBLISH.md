# How to Publish to GitHub

## Step 1: Create GitHub Repository

1. Go to https://github.com/vikasgaddu1
2. Click **"New repository"** (green button)
3. Fill in:
   - **Repository name:** `crf-annotation-mcp`
   - **Description:** `MCP server for querying SDTM annotations from annotated CRF PDFs`
   - **Visibility:** Public
   - **❌ DO NOT** check "Initialize with README" (we already have one)
4. Click **"Create repository"**

## Step 2: Push Code to GitHub

GitHub will show you commands. Use these instead (already configured):

```bash
cd /data/.openclaw/workspace/crf-annotation-mcp

# Rename branch to main
git branch -M main

# Add remote (GitHub will give you this URL after creating repo)
git remote add origin https://github.com/vikasgaddu1/crf-annotation-mcp.git

# Push
git push -u origin main
```

**Note:** You'll be prompted for GitHub credentials. If you have 2FA enabled, use a Personal Access Token instead of your password.

## Step 3: Add Repository Topics

On the GitHub repo page:
1. Click **"⚙️ Settings"** (gear icon) next to "About"
2. Add topics:
   - `mcp`
   - `model-context-protocol`
   - `sdtm`
   - `cdisc`
   - `clinical-programming`
   - `ai-assistant`
   - `claude`
   - `python`
   - `pharmaceutical`
3. Save changes

## Step 4: Enable Features

In **Settings** → **General**:
- ✅ Issues
- ✅ Discussions (optional, but recommended)

## Step 5: Add Description & Website (Optional)

In the "About" section:
- **Website:** https://clawhub.com or your blog
- **Description:** "MCP server for querying SDTM annotations from annotated CRF PDFs. Works with Claude Desktop and other MCP clients."

---

## 🎉 Done!

Your repo will be live at:
**https://github.com/vikasgaddu1/crf-annotation-mcp**

Next: Post about it on LinkedIn!

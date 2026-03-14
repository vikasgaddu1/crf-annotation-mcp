# Quick Start Guide

Get up and running with CRF Annotation MCP in 5 minutes.

## 1. Install

```bash
# Clone the repo
git clone https://github.com/vikasgaddu1/crf-annotation-mcp.git
cd crf-annotation-mcp

# Install with uv (recommended)
uv pip install -e .
```

## 2. Test It Out (No MCP Required)

Try the example to see how it works:

```bash
# Run the example
python examples/example_usage.py
```

You'll see output like:

```
======================================================================
CRF Annotation Query Example
======================================================================

1. All Domains:
----------------------------------------------------------------------
  DM (has SUPP): 3 annotations
  AE: 2 annotations
  VS: 2 annotations

2. DM Domain Annotations (includes SUPPDM):
----------------------------------------------------------------------
  DM.USUBJID - Page 1 - (Subject ID)
  DM.RFSTDTC - Page 1 - (Study start date)
  DM.BRTHDTC - Page 2 - (Date of birth)
  SUPPDM.RACE2 - Page 2 - (Secondary race)

...
```

## 3. Configure Claude Desktop

**macOS config:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows config:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this:

```json
{
  "mcpServers": {
    "crf-annotations": {
      "command": "uv",
      "args": [
        "--directory",
        "/FULL/PATH/TO/crf-annotation-mcp",
        "run",
        "crf-annotation-mcp"
      ],
      "env": {
        "CRF_PDF_PATH": "/FULL/PATH/TO/your_annotated_crf.pdf"
      }
    }
  }
}
```

**⚠️ Important:** Replace `/FULL/PATH/TO/` with actual absolute paths!

## 4. Restart Claude Desktop

Fully quit and restart Claude Desktop.

## 5. Try It!

Ask Claude:

- **"List all SDTM domains in the CRF"**
- **"Show me all DM annotations"**
- **"What's annotated on page 5?"**
- **"Search for 'adverse event' annotations"**

## What If It Doesn't Work?

### Check the config file:
```bash
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Windows (PowerShell)
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
```

### Check the logs:
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Windows
# Open: %APPDATA%\Claude\logs\
```

### Common issues:

1. **Invalid JSON** - No trailing commas allowed
2. **Relative paths** - Must use absolute paths (not `~/` or `.\`)
3. **PDF not found** - Check that `CRF_PDF_PATH` points to a real file

## Next Steps

✅ **Working?** Check out [SETUP_GUIDE.md](SETUP_GUIDE.md) for advanced features

✅ **Want to customize?** See [README.md](README.md) for architecture details

✅ **Found a bug?** Open an issue: https://github.com/vikasgaddu1/crf-annotation-mcp/issues

---

**Need help?** Check the [troubleshooting section](SETUP_GUIDE.md#troubleshooting) in the setup guide.

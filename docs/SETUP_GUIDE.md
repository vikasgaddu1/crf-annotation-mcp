# CRF Annotation MCP Setup Guide

Complete guide to setting up the CRF Annotation MCP server with various AI assistants.

## Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`
- An annotated CRF PDF file

## Installation

### Option 1: Using `uv` (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/vikasgaddu1/crf-annotation-mcp.git
cd crf-annotation-mcp

# Install dependencies
uv pip install -e .
```

### Option 2: Using `pip`

```bash
# Clone the repository
git clone https://github.com/vikasgaddu1/crf-annotation-mcp.git
cd crf-annotation-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Configuration

### 1. Prepare Your Annotated CRF PDF

Your CRF PDF should have annotations (comments) in this format:

```
DM.USUBJID
DM.RFSTDTC (Page 3, Study start date)
SUPPDM.RACE2 (Page 2, Secondary race)
AE.AEDECOD (Page 15-18, Adverse event term)
```

**Supported formats:**
- Simple: `DOMAIN.VARIABLE`
- With page: `DOMAIN.VARIABLE (Page N)`
- With description: `DOMAIN.VARIABLE (Page N, Description)`

### 2. Claude Desktop Configuration

Edit your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "crf-annotations": {
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/crf-annotation-mcp",
        "run",
        "crf-annotation-mcp"
      ],
      "env": {
        "CRF_PDF_PATH": "/full/path/to/your/annotated_crf.pdf"
      }
    }
  }
}
```

**Important:** Use absolute paths for both the project directory and PDF file.

### 3. Restart Claude Desktop

After saving the config, fully quit and restart Claude Desktop.

## Verification

Once configured, you should see the CRF annotation tools available in Claude Desktop.

Try asking:
- "List all SDTM domains in the CRF"
- "Show me all DM annotations"
- "What's on page 5 of the CRF?"
- "Search for annotations containing 'adverse event'"

## Example Queries

### Query by Domain (includes SUPP automatically)

```
User: "Show me all DM domain annotations"

Claude will use: get_annotations(domain="DM", include_supp=true)

Returns: DM.USUBJID, DM.RFSTDTC, SUPPDM.RACE2, etc.
```

### Query by Page

```
User: "What domains are annotated on page 15?"

Claude will use: get_annotations(page=15)

Returns: All annotations found on page 15
```

### Search by Keyword

```
User: "Find all annotations related to dates"

Claude will use: search_annotations(query="date")

Returns: DM.RFSTDTC, DM.BRTHDTC, AE.AESTDTC, etc.
```

### Get Overview

```
User: "Give me an overview of all domains"

Claude will use: list_domains()

Returns: Summary of each domain with annotation counts
```

## Programmatic Usage (Without MCP)

You can also use the library directly in Python:

```python
from crf_annotation_mcp import AnnotationParser, AnnotationQuery

# Parse PDF
parser = AnnotationParser("path/to/crf.pdf")
annotations = parser.parse()

# Query annotations
query = AnnotationQuery(annotations)

# Get DM domain (includes SUPPDM)
dm_annotations = query.get_annotations(domain="DM")

# Search
results = query.search_annotations("adverse event")

# List all domains
domains = query.list_domains()
```

See `examples/example_usage.py` for a complete example.

## Troubleshooting

### MCP Server Not Appearing in Claude Desktop

1. Check that the config file is valid JSON (no trailing commas)
2. Verify paths are absolute (not relative)
3. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`

### "PDF not found" Error

- Ensure `CRF_PDF_PATH` points to an existing PDF file
- Use absolute paths (not `~` or relative paths)
- Check file permissions

### No Annotations Found

- Verify your PDF has actual annotations/comments
- Annotations must be in the format `DOMAIN.VARIABLE`
- Try opening the PDF in Adobe Reader and checking the comments panel

### ImportError or Module Not Found

```bash
# Reinstall dependencies
uv pip install -e .

# Or if using pip
pip install -e .
```

## Advanced Configuration

### Multiple CRF Files

To work with multiple CRFs, create separate MCP server entries:

```json
{
  "mcpServers": {
    "crf-study-001": {
      "command": "uv",
      "args": ["--directory", "/path/to/crf-annotation-mcp", "run", "crf-annotation-mcp"],
      "env": {"CRF_PDF_PATH": "/path/to/study_001_crf.pdf"}
    },
    "crf-study-002": {
      "command": "uv",
      "args": ["--directory", "/path/to/crf-annotation-mcp", "run", "crf-annotation-mcp"],
      "env": {"CRF_PDF_PATH": "/path/to/study_002_crf.pdf"}
    }
  }
}
```

### Custom Annotation Patterns

To support custom annotation formats, edit `src/crf_annotation_mcp/parser.py` and modify the `ANNOTATION_PATTERN` regex.

## Integration with Other Tools

### With annoSDTMCheck

1. Annotate your CRF PDF
2. Use **crf-annotation-mcp** during study setup to query annotations
3. After dataset creation, use **annoSDTMCheck** to validate annotations against data

### With Define.xml

Future versions will support exporting query results to Define.xml format.

## Support

- **Issues:** https://github.com/vikasgaddu1/crf-annotation-mcp/issues
- **Discussions:** https://github.com/vikasgaddu1/crf-annotation-mcp/discussions

## Next Steps

Once you have it working:

1. Try the example queries above
2. Explore combining it with other MCP servers
3. Consider contributing improvements or additional features

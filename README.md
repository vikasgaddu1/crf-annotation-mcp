# CRF Annotation MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to query SDTM annotations from annotated CRF PDFs.

## Features

- **Read annotated CRF PDFs** - Extract SDTM domain/variable annotations from PDF comments
- **Domain-aware queries** - Automatically includes SUPP domains when querying parent domains
- **Natural language interface** - Ask questions like "Give me all annotations for DM domain"
- **SDTM-compliant** - Understands SDTM domain relationships and naming conventions
- **MCP integration** - Works with any MCP-compatible AI assistant (Claude Desktop, Cline, etc.)

## Use Cases

- "Show me all DM annotations" → Returns DM + SUPPDM annotations
- "What CRF pages contain adverse event data?" → Returns AE domain page references
- "List all variables annotated for vital signs" → Returns VS annotations
- "Which domains are annotated on page 15?" → Cross-reference page to domains

## Architecture

```
crf-annotation-mcp/
├── src/
│   └── crf_annotation_mcp/
│       ├── server.py          # MCP server implementation
│       ├── parser.py           # PDF annotation extraction
│       ├── query.py            # Annotation query engine
│       └── models.py           # Data models (Annotation, Domain, etc.)
├── tests/
├── examples/
│   └── sample_annotated_crf.pdf
└── README.md
```

## Installation

```bash
# Clone the repo
git clone https://github.com/vikasgaddu1/crf-annotation-mcp.git
cd crf-annotation-mcp

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "crf-annotations": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/crf-annotation-mcp",
        "run",
        "crf-annotation-mcp"
      ],
      "env": {
        "CRF_PDF_PATH": "/path/to/your/annotated_crf.pdf"
      }
    }
  }
}
```

### Cursor

Add to Cursor settings (Settings → Features → Model Context Protocol):

```json
{
  "mcpServers": {
    "crf-annotations": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/crf-annotation-mcp",
        "run",
        "crf-annotation-mcp"
      ],
      "env": {
        "CRF_PDF_PATH": "/path/to/your/annotated_crf.pdf"
      }
    }
  }
}
```

### Cline (VSCode Extension)

Add to VSCode settings (`settings.json`):

```json
{
  "cline.mcpServers": {
    "crf-annotations": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/crf-annotation-mcp",
        "run",
        "crf-annotation-mcp"
      ],
      "env": {
        "CRF_PDF_PATH": "/path/to/your/annotated_crf.pdf"
      }
    }
  }
}
```

### Continue (VSCode Extension)

Add to `~/.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "crf-annotations",
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/crf-annotation-mcp",
        "run",
        "crf-annotation-mcp"
      ],
      "env": {
        "CRF_PDF_PATH": "/path/to/your/annotated_crf.pdf"
      }
    }
  ]
}
```

### Zed Editor

Add to Zed settings (Settings → Assistant → MCP):

```json
{
  "assistant": {
    "version": "2",
    "provider": {
      "name": "anthropic",
      "mcpServers": {
        "crf-annotations": {
          "command": "uv",
          "args": [
            "--directory",
            "/path/to/crf-annotation-mcp",
            "run",
            "crf-annotation-mcp"
          ],
          "env": {
            "CRF_PDF_PATH": "/path/to/your/annotated_crf.pdf"
          }
        }
      }
    }
  }
}
```

**Note:** Replace `/path/to/crf-annotation-mcp` with the actual installation path and `/path/to/your/annotated_crf.pdf` with your PDF file path.

## MCP Tools

### `get_annotations`
Query annotations by domain, page, or variable.

**Parameters:**
- `domain` (optional): SDTM domain (e.g., "DM", "AE", "VS")
- `page` (optional): CRF page number
- `variable` (optional): Variable name (e.g., "USUBJID", "AEDECOD")
- `include_supp` (default: true): Include SUPP domain annotations

**Examples:**
```python
# Get all DM annotations (includes SUPPDM automatically)
get_annotations(domain="DM")

# Get annotations on page 5
get_annotations(page=5)

# Get specific variable across all domains
get_annotations(variable="USUBJID")
```

### `list_domains`
List all SDTM domains found in the annotated CRF.

**Returns:** Array of domain names with annotation counts

### `get_page_mapping`
Get a mapping of CRF pages to SDTM domains.

**Returns:** Dictionary of page numbers to domains

### `search_annotations`
Free-text search across all annotations.

**Parameters:**
- `query`: Search term (e.g., "date of birth", "adverse event")

## How It Works

1. **Extract annotations** - Reads PDF comments/annotations using PyMuPDF
2. **Parse SDTM metadata** - Identifies domain, variable, and page references
3. **Build query index** - Creates searchable index of annotations
4. **Serve via MCP** - Exposes tools for AI assistants to query

## Annotation Format Expected

The parser expects annotations in this format:

```
DM.USUBJID
DM.RFSTDTC (Page 3, Question 5)
SUPPDM.RACE2 (Page 2, Multi-select option)
AE.AEDECOD (Page 15-18, Free text)
```

## Integration with annoSDTMCheck

This MCP server is designed to complement [annoSDTMCheck](https://github.com/vikasgaddu1/annoSDTMCheck):

- **annoSDTMCheck**: Validates annotations against actual SDTM datasets
- **crf-annotation-mcp**: Makes annotations queryable via AI assistants

Workflow:
1. Annotate your CRF PDF with SDTM mappings
2. Use **crf-annotation-mcp** during study setup to query annotations
3. After dataset creation, use **annoSDTMCheck** to validate

## Roadmap

- [ ] Support for Excel annotation specs (in addition to PDF)
- [ ] Integration with Define.xml for variable metadata
- [ ] Annotation validation (detect malformed annotations)
- [ ] Export query results to Define.xml or spreadsheet
- [ ] Support for ODM-XML CRF annotations

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

MIT

## Contact

Vikas Gaddu - [@vikasgaddu1](https://github.com/vikasgaddu1)

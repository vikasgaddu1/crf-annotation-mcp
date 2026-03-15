# CRF Annotation MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to query SDTM annotations from annotated CRF PDFs.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** — Check with `python --version` or `python3 --version`
- **uv** (recommended) or **pip** — [uv](https://docs.astral.sh/uv/) is a fast Python package manager. Install with:
  - **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
  - **macOS/Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **An annotated CRF PDF** — Or use the sample file included in `examples/acrf.pdf` (FreeText annotations; the format used in real annotated CRFs)

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
├── .cursor/
│   └── mcp.json               # MCP config (create this for Cursor)
├── docs/
│   ├── SETUP_GUIDE.md         # Detailed setup instructions
│   └── QUICKSTART.md          # 5-minute setup guide
├── examples/
│   ├── acrf.pdf               # Sample annotated CRF (FreeText format)
│   ├── sample_annotated_crf.pdf
│   └── example_usage.py
├── src/
│   └── crf_annotation_mcp/
│       ├── server.py          # MCP server implementation
│       ├── parser.py          # PDF annotation extraction
│       ├── query.py           # Annotation query engine
│       └── models.py          # Data models
├── tests/
├── README.md
└── pyproject.toml
```

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/vikasgaddu1/crf-annotation-mcp.git
cd crf-annotation-mcp
```

### Step 2: Install the project

**Option A: Using uv (recommended)**

If you have [uv](https://docs.astral.sh/uv/) installed, you can skip creating a venv — `uv run` handles it automatically:

```bash
uv pip install -e .
```

**Option B: Using pip with a virtual environment**

Using a virtual environment avoids conflicts with other Python packages (fastapi, jupyter, streamlit, etc.):

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# Install the project
pip install -e .
```

### Step 3: Verify installation

Run the server to confirm it works (it will exit with an error about `CRF_PDF_PATH` — that's expected):

```bash
# With uv:
uv run crf-annotation-mcp

# With pip (after activating venv):
crf-annotation-mcp
```

You should see: `CRF_PDF_PATH environment variable not set`. That means the server is installed correctly.

### Troubleshooting: Dependency Conflicts

If you see errors about `starlette`, `anyio`, or `packaging` version conflicts when installing, you're likely using a global Python with other packages. **Use a virtual environment** (Option B above) to isolate this project's dependencies.

## Configuration

### Quick Start: Cursor (First-Time Setup)

If you're using Cursor and want to get started quickly:

1. **Complete Installation** (see above) — clone the repo and run `uv pip install -e .` or `pip install -e .`

2. **Create the MCP config file** — Create a file at `.cursor/mcp.json` in the project root (same folder as `pyproject.toml`):

   ```
   crf-annotation-mcp/
   ├── .cursor/
   │   └── mcp.json    ← Create this file
   ├── pyproject.toml
   └── ...
   ```

3. **Add this configuration** to `.cursor/mcp.json` (replace paths with your actual paths):

   **Windows:**
   ```json
   {
     "mcpServers": {
       "crf-annotations": {
         "command": "uv",
         "args": [
           "--directory",
           "C:\\path\\to\\crf-annotation-mcp",
           "run",
           "crf-annotation-mcp"
         ],
         "env": {
           "CRF_PDF_PATH": "C:\\path\\to\\crf-annotation-mcp\\examples\\acrf.pdf"
         }
       }
     }
   }
   ```

   **macOS/Linux:**
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
           "CRF_PDF_PATH": "/path/to/crf-annotation-mcp/examples/acrf.pdf"
         }
       }
     }
   }
   ```

4. **Restart Cursor completely** — Close and reopen Cursor (or File → Exit, then reopen). MCP config changes require a full restart.

5. **Verify it works** — Open a new chat in Cursor. The Agent should now have access to CRF annotation tools. Try asking: *"List all domains in the annotated CRF"* or *"What annotations are in the DM domain?"* You can also check **Settings → Tools & MCP** (Ctrl+Shift+J) to see if `crf-annotations` is listed and enabled.

**Usage tip:** You don't need to say "use MCP" — the Agent picks up tools automatically. For CRF-specific queries, phrasing like *"What VS variables are annotated in my CRF?"* or *"Query the annotations for the EX domain"* helps the Agent use the right tools.

**Don't have uv?** Install it (see Prerequisites) or use your venv's Python. If you used `pip install -e .` in a virtual environment, use this config instead (replace paths):

   ```json
   {
     "mcpServers": {
       "crf-annotations": {
         "command": "C:\\path\\to\\crf-annotation-mcp\\.venv\\Scripts\\python.exe",
         "args": ["-m", "crf_annotation_mcp.server"],
         "env": {
           "CRF_PDF_PATH": "C:\\path\\to\\your\\annotated_crf.pdf"
         }
       }
     }
   }
   ```

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

### Cursor (Alternative: Global config)

You can also add the server to `~/.cursor/mcp.json` (in your home directory) for all projects. See [Quick Start: Cursor](#quick-start-cursor-first-time-setup) above for the config format.

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

### Which CRF does the MCP use?

The MCP uses **one CRF at a time**, chosen by the `CRF_PDF_PATH` environment variable in your mcp.json. There is no default — whatever path you set is the CRF the server loads.

- **PDF location:** The PDF can be **anywhere** on your system. It does not need to be in the `examples/` folder. Use `acrf.pdf` as the reference — it uses FreeText annotations (the standard format for annotated CRFs), not sticky comments.
- **Multiple CRFs:** To switch to a different CRF, change `CRF_PDF_PATH` in `.cursor/mcp.json` to the new file path, then **restart Cursor** so the MCP server reloads with the new path. You cannot query multiple CRFs in the same session.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **Server doesn't appear in Cursor** | Restart Cursor completely (File → Exit, then reopen). MCP config is loaded on startup. |
| **"CRF_PDF_PATH environment variable not set"** | Add the `env` block with `CRF_PDF_PATH` to your mcp.json. Use the full path to your PDF. |
| **"uv: command not found"** | Install [uv](https://docs.astral.sh/uv/) or use the pip/venv alternative in the Cursor Quick Start section. |
| **Server fails to start** | Check **Output** panel (Ctrl+Shift+U / Cmd+Shift+U) → select "MCP Logs" for error details. |
| **Wrong path on Windows** | Use double backslashes in JSON: `"C:\\Users\\you\\path\\to\\file.pdf"` |

## MCP Tools

### `get_annotations`
Query annotations by domain, page, or variable.

**Parameters:**
- `domain` (optional): SDTM domain (e.g., "DM", "AE", "VS", "EX")
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

### `get_domain_relationships`
Get SUPP domain relationships for a parent domain (e.g., DM → SUPPDM).

**Parameters:**
- `domain`: Parent domain (e.g., "DM", "CM", "QS")

## How It Works

1. **Extract annotations** - Reads PDF comments/annotations using PyMuPDF
2. **Parse SDTM metadata** - Identifies domain, variable, and page references
3. **Build query index** - Creates searchable index of annotations
4. **Serve via MCP** - Exposes tools for AI assistants to query

## Annotation Format Expected

The parser supports two annotation formats:

**1. FreeText annotations** (typical for annotated CRFs, as in `acrf.pdf`):
- `DOMAIN=Description` (e.g., `VS=Vital Signs`) — sets domain context
- `VARIABLE` (e.g., `VSTEST`, `SITEID`) — variable under current domain
- `VARIABLE when X = Y` (e.g., `SCORRES when SCTESTCD = SUBJINIT`)
- `VARIABLE / VARIABLE2 when X = Y` (e.g., `VSORRES / VSORRESU when VSTESTCD = SYSBP`)
- `VARIABLE in SUPPDOMAIN` (e.g., `RACEOTH in SUPPDM`)

**2. Sticky-note format** (legacy):
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

Contributions welcome! See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for setup details.

## License

MIT

## Contact

Vikas Gaddu - [@vikasgaddu1](https://github.com/vikasgaddu1)

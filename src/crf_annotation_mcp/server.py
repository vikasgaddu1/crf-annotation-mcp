"""MCP server for CRF annotation queries."""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .parser import AnnotationParser
from .query import AnnotationQuery
from .models import Annotation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize server
app = Server("crf-annotation-mcp")

# Global query engine (initialized on startup)
query_engine: AnnotationQuery | None = None


def load_annotations(pdf_path: str) -> AnnotationQuery:
    """Load and parse annotations from PDF."""
    logger.info(f"Loading annotations from: {pdf_path}")
    parser = AnnotationParser(pdf_path)
    annotations = parser.parse()
    logger.info(f"Loaded {len(annotations)} annotations")
    return AnnotationQuery(annotations)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="get_annotations",
            description=(
                "Query SDTM annotations by domain, page, or variable. "
                "Automatically includes SUPP domains when querying parent domain "
                "(e.g., querying DM returns DM + SUPPDM)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "SDTM domain (e.g., DM, AE, VS)",
                    },
                    "page": {
                        "type": "integer",
                        "description": "CRF page number",
                    },
                    "variable": {
                        "type": "string",
                        "description": "Variable name (e.g., USUBJID, AEDECOD)",
                    },
                    "include_supp": {
                        "type": "boolean",
                        "description": "Include SUPP domain annotations (default: true)",
                        "default": True,
                    },
                },
            },
        ),
        Tool(
            name="list_domains",
            description="List all SDTM domains found in the annotated CRF with summary statistics.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_page_mapping",
            description="Get a mapping of CRF pages to SDTM domains.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="search_annotations",
            description="Free-text search across all annotations (domain, variable, description).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (e.g., 'date of birth', 'adverse event')",
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_domain_relationships",
            description="Get related domains (SUPP domains, related datasets) for a given domain.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "SDTM domain (e.g., DM, AE)",
                    }
                },
                "required": ["domain"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if query_engine is None:
        return [TextContent(type="text", text="Error: Annotations not loaded")]

    try:
        if name == "get_annotations":
            domain = arguments.get("domain")
            page = arguments.get("page")
            variable = arguments.get("variable")
            include_supp = arguments.get("include_supp", True)

            results = query_engine.get_annotations(
                domain=domain, page=page, variable=variable, include_supp=include_supp
            )

            if not results:
                return [TextContent(type="text", text="No annotations found matching criteria.")]

            # Format results
            output_lines = [f"Found {len(results)} annotation(s):\n"]
            for anno in results:
                output_lines.append(str(anno))

            return [TextContent(type="text", text="\n".join(output_lines))]

        elif name == "list_domains":
            domains = query_engine.list_domains()

            output_lines = ["SDTM Domains in CRF:\n"]
            for domain in domains:
                supp_indicator = " (has SUPP)" if domain.has_supp else ""
                output_lines.append(
                    f"• {domain.domain}{supp_indicator}: "
                    f"{domain.annotation_count} annotations, "
                    f"{len(domain.variables)} variables, "
                    f"pages {', '.join(map(str, domain.pages))}"
                )

            return [TextContent(type="text", text="\n".join(output_lines))]

        elif name == "get_page_mapping":
            mappings = query_engine.get_page_mapping()

            output_lines = ["CRF Page to Domain Mapping:\n"]
            for mapping in mappings:
                domains_str = ", ".join(mapping.domains)
                output_lines.append(
                    f"Page {mapping.page}: {domains_str} ({mapping.annotation_count} annotations)"
                )

            return [TextContent(type="text", text="\n".join(output_lines))]

        elif name == "search_annotations":
            query = arguments.get("query", "")
            results = query_engine.search_annotations(query)

            if not results:
                return [TextContent(type="text", text=f"No annotations found matching '{query}'.")]

            output_lines = [f"Search results for '{query}' ({len(results)} found):\n"]
            for anno in results:
                output_lines.append(str(anno))

            return [TextContent(type="text", text="\n".join(output_lines))]

        elif name == "get_domain_relationships":
            domain = arguments.get("domain", "")
            relationships = query_engine.get_domain_relationships(domain)

            output_lines = [f"Relationships for {domain}:\n"]
            if relationships["supp"]:
                output_lines.append(f"SUPP domains: {', '.join(relationships['supp'])}")
            else:
                output_lines.append("No SUPP domain found")

            return [TextContent(type="text", text="\n".join(output_lines))]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point for the MCP server."""
    global query_engine

    # Get PDF path from environment
    pdf_path = os.getenv("CRF_PDF_PATH")
    if not pdf_path:
        logger.error("CRF_PDF_PATH environment variable not set")
        sys.exit(1)

    # Load annotations
    try:
        query_engine = load_annotations(pdf_path)
    except Exception as e:
        logger.error(f"Failed to load annotations: {e}", exc_info=True)
        sys.exit(1)

    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

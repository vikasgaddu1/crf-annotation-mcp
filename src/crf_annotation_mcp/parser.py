"""PDF annotation parser for extracting SDTM annotations."""

import re
from pathlib import Path
from typing import List, Optional
import fitz  # PyMuPDF

from .models import Annotation


class AnnotationParser:
    """Parser for extracting SDTM annotations from annotated CRF PDFs."""

    # Pattern: DM.USUBJID or SUPPDM.QNAM
    ANNOTATION_PATTERN = re.compile(
        r"(?P<domain>[A-Z]{2,8})\.(?P<variable>[A-Z0-9_]+)"
        r"(?:\s*\(Page\s*(?P<page>\d+)(?:,\s*(?P<description>[^)]+))?\))?"
    )

    def __init__(self, pdf_path: str):
        """Initialize the parser with a PDF path."""
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

    def parse(self) -> List[Annotation]:
        """Extract all SDTM annotations from the PDF."""
        annotations = []

        with fitz.open(self.pdf_path) as doc:
            for page_num, page in enumerate(doc, start=1):
                # Get all annotations (comments) on this page
                annot_list = page.annots()
                if not annot_list:
                    continue

                for annot in annot_list:
                    # Get annotation content
                    content = annot.info.get("content", "")
                    if not content:
                        continue

                    # Try to parse SDTM annotation
                    parsed = self._parse_annotation(content, page_num)
                    if parsed:
                        annotations.extend(parsed)

        return annotations

    def _parse_annotation(self, text: str, default_page: int) -> List[Annotation]:
        """Parse a single annotation text into Annotation objects."""
        annotations = []

        # Split on newlines to handle multiple annotations in one comment
        for line in text.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            # Try to match the pattern
            matches = self.ANNOTATION_PATTERN.finditer(line)
            for match in matches:
                domain = match.group("domain")
                variable = match.group("variable")
                page_str = match.group("page")
                description = match.group("description")

                # Use page from annotation if provided, else use PDF page number
                page = int(page_str) if page_str else default_page

                # Check if this is a SUPP domain
                is_supp = domain.startswith("SUPP")

                annotations.append(
                    Annotation(
                        domain=domain,
                        variable=variable,
                        page=page,
                        question=None,  # Could be enhanced to parse question numbers
                        description=description.strip() if description else None,
                        raw_text=line,
                        is_supp=is_supp,
                    )
                )

        return annotations

    @staticmethod
    def parse_from_text(text: str, page: int = 1) -> List[Annotation]:
        """Parse annotations from raw text (for testing or text-based specs)."""
        parser = AnnotationParser.__new__(AnnotationParser)
        return parser._parse_annotation(text, page)

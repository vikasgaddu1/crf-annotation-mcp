"""PDF annotation parser for extracting SDTM annotations."""

import re
from pathlib import Path
from typing import List, Optional
import fitz  # PyMuPDF

from .models import Annotation


class AnnotationParser:
    """Parser for extracting SDTM annotations from annotated CRF PDFs.

    Supports two annotation formats:
    - Sticky notes: DOMAIN.VARIABLE (Page N, description)
    - FreeText (typical annotated CRF): DOMAIN=Name, VARIABLE, VARIABLE when X=Y, etc.
    """

    # Pattern: DM.USUBJID or SUPPDM.QNAM (sticky-note format)
    ANNOTATION_PATTERN = re.compile(
        r"(?P<domain>[A-Z]{2,8})\.(?P<variable>[A-Z0-9_]+)"
        r"(?:\s*\(Page\s*(?P<page>\d+)(?:,\s*(?P<description>[^)]+))?\))?"
    )

    # Pattern: DOMAIN=Description (e.g., DM=Demographics, VS=Vital Signs)
    DOMAIN_HEADER_PATTERN = re.compile(
        r"^(?P<domain>[A-Z]{2,8})\s*=\s*(?P<description>.+)$"
    )

    # Pattern: VARIABLE in SUPPDOMAIN (e.g., RACEOTH in SUPPDM)
    SUPP_VAR_PATTERN = re.compile(
        r"^(?P<variable>[A-Z0-9_]+)\s+in\s+(?P<domain>SUPP[A-Z]{2,8})$",
        re.IGNORECASE,
    )

    # Pattern: VARIABLE / VARIABLE2 when X = Y (e.g., VSORRES / VSORRESU when VSTESTCD = SYSBP)
    MULTI_VAR_PATTERN = re.compile(
        r"(?P<variable>[A-Z0-9_]+)(?:\s*/\s*(?P<variable2>[A-Z0-9_]+))?"
        r"(?:\s+when\s+[A-Z0-9_]+\s*=\s*[^,\s]+(?:\s*,\s*[^,\s]+)*)?",
        re.IGNORECASE,
    )

    # Standalone SDTM variable (uppercase, alphanumeric, underscore)
    VAR_ONLY_PATTERN = re.compile(r"^([A-Z][A-Z0-9_]{1,7})$")

    def __init__(self, pdf_path: str):
        """Initialize the parser with a PDF path."""
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

    def parse(self) -> List[Annotation]:
        """Extract all SDTM annotations from the PDF."""
        annotations = []
        current_domain: Optional[str] = None

        with fitz.open(self.pdf_path) as doc:
            for page_num, page in enumerate(doc, start=1):
                # Get all annotations (Text, FreeText, etc.) on this page
                annot_list = page.annots()
                if not annot_list:
                    continue

                for annot in annot_list:
                    content = self._get_annotation_content(annot)
                    if not content:
                        continue

                    parsed, current_domain = self._parse_annotation(
                        content, page_num, current_domain
                    )
                    if parsed:
                        annotations.extend(parsed)

        return annotations

    def _get_annotation_content(self, annot) -> str:
        """Get text content from annotation (supports Text and FreeText)."""
        content = annot.info.get("content", "")
        if content:
            return content.strip()
        # FreeText may store content differently; try content property
        if hasattr(annot, "get_text") and callable(annot.get_text):
            return (annot.get_text() or "").strip()
        return ""

    def _parse_annotation(
        self, text: str, default_page: int, current_domain: Optional[str]
    ) -> tuple[List[Annotation], Optional[str]]:
        """Parse a single annotation text into Annotation objects."""
        annotations = []
        domain = current_domain

        for line in text.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("[NOT SUBMITTED]"):
                continue

            # 1. DOMAIN=Description (sets context)
            domain_match = self.DOMAIN_HEADER_PATTERN.match(line)
            if domain_match:
                domain = domain_match.group("domain")
                continue

            # 2. DOMAIN.VARIABLE (sticky-note format)
            matches = list(self.ANNOTATION_PATTERN.finditer(line))
            if matches:
                for m in matches:
                    page_str = m.group("page")
                    page = int(page_str) if page_str else default_page
                    annotations.append(
                        self._make_annotation(
                            m.group("domain"),
                            m.group("variable"),
                            page,
                            m.group("description"),
                            line,
                        )
                    )
                continue

            # 3. VARIABLE in SUPPDOMAIN
            supp_match = self.SUPP_VAR_PATTERN.match(line)
            if supp_match:
                annotations.append(
                    self._make_annotation(
                        supp_match.group("domain"),
                        supp_match.group("variable"),
                        default_page,
                        None,
                        line,
                    )
                )
                continue

            # 4. VARIABLE or VARIABLE when X=Y or VARIABLE / VARIABLE2 when X=Y
            multi_match = self.MULTI_VAR_PATTERN.match(line)
            if multi_match and domain:
                var1 = multi_match.group("variable")
                var2 = multi_match.group("variable2")
                if self._is_sdtm_variable(var1):
                    annotations.append(
                        self._make_annotation(domain, var1, default_page, None, line)
                    )
                if var2 and self._is_sdtm_variable(var2):
                    annotations.append(
                        self._make_annotation(domain, var2, default_page, None, line)
                    )
                continue

            # 5. Standalone VARIABLE (use current domain)
            var_match = self.VAR_ONLY_PATTERN.match(line)
            if var_match and domain:
                var = var_match.group(1)
                if self._is_sdtm_variable(var):
                    annotations.append(
                        self._make_annotation(domain, var, default_page, None, line)
                    )

        return annotations, domain

    def _is_sdtm_variable(self, name: str) -> bool:
        """Check if string looks like an SDTM variable name."""
        return bool(re.match(r"^[A-Z][A-Z0-9_]{0,7}$", name))

    def _make_annotation(
        self,
        domain: str,
        variable: str,
        page: int,
        description: Optional[str],
        raw_text: str,
    ) -> Annotation:
        """Create an Annotation model instance."""
        return Annotation(
            domain=domain,
            variable=variable,
            page=page,
            question=None,
            description=description.strip() if description else None,
            raw_text=raw_text,
            is_supp=domain.startswith("SUPP"),
        )

    @staticmethod
    def parse_from_text(text: str, page: int = 1) -> List[Annotation]:
        """Parse annotations from raw text (for testing or text-based specs)."""
        parser = AnnotationParser.__new__(AnnotationParser)
        annotations, _ = parser._parse_annotation(text, page, None)
        return annotations

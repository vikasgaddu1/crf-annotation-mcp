"""Query engine for SDTM annotations."""

from collections import defaultdict
from typing import List, Dict, Optional
from .models import Annotation, DomainSummary, PageMapping


class AnnotationQuery:
    """Query engine for SDTM annotations with domain-aware logic."""

    def __init__(self, annotations: List[Annotation]):
        """Initialize with a list of annotations."""
        self.annotations = annotations
        self._index_annotations()

    def _index_annotations(self):
        """Build internal indexes for fast querying."""
        self.by_domain: Dict[str, List[Annotation]] = defaultdict(list)
        self.by_page: Dict[int, List[Annotation]] = defaultdict(list)
        self.by_variable: Dict[str, List[Annotation]] = defaultdict(list)

        for anno in self.annotations:
            self.by_domain[anno.domain].append(anno)
            if anno.page:
                self.by_page[anno.page].append(anno)
            self.by_variable[anno.variable].append(anno)

    def get_annotations(
        self,
        domain: Optional[str] = None,
        page: Optional[int] = None,
        variable: Optional[str] = None,
        include_supp: bool = True,
    ) -> List[Annotation]:
        """
        Query annotations with optional filters.

        Args:
            domain: SDTM domain (e.g., "DM", "AE"). If include_supp=True,
                   also returns SUPP<domain> annotations.
            page: CRF page number
            variable: Variable name
            include_supp: If True and domain is specified, include SUPP domain

        Returns:
            List of matching annotations
        """
        # Start with all annotations, then narrow down with each filter
        results = self.annotations

        if domain:
            domain_set = {domain}
            if include_supp and not domain.startswith("SUPP"):
                domain_set.add(f"SUPP{domain}")
            results = [a for a in results if a.domain in domain_set]

        if page is not None:
            results = [a for a in results if a.page == page]

        if variable:
            results = [a for a in results if a.variable == variable]

        return results

    def list_domains(self) -> List[DomainSummary]:
        """List all domains with summary statistics."""
        summaries = []

        for domain, annos in self.by_domain.items():
            # Skip SUPP domains for now (they'll be flagged in parent domain)
            if domain.startswith("SUPP"):
                continue

            variables = sorted(set(a.variable for a in annos))
            pages = sorted(set(a.page for a in annos if a.page))

            # Check if this domain has a SUPP
            supp_domain = f"SUPP{domain}"
            has_supp = supp_domain in self.by_domain

            summaries.append(
                DomainSummary(
                    domain=domain,
                    annotation_count=len(annos),
                    variables=variables,
                    pages=pages,
                    has_supp=has_supp,
                )
            )

        return sorted(summaries, key=lambda x: x.domain)

    def get_page_mapping(self) -> List[PageMapping]:
        """Get mapping of CRF pages to SDTM domains."""
        mappings = []

        for page, annos in sorted(self.by_page.items()):
            domains = sorted(set(a.domain for a in annos))
            mappings.append(
                PageMapping(page=page, domains=domains, annotation_count=len(annos))
            )

        return mappings

    def search_annotations(self, query: str) -> List[Annotation]:
        """
        Free-text search across all annotations.

        Searches in: domain, variable, description, and raw text.
        """
        query_lower = query.lower()
        results = []

        for anno in self.annotations:
            searchable = " ".join(
                filter(
                    None,
                    [
                        anno.domain,
                        anno.variable,
                        anno.description or "",
                        anno.raw_text,
                    ],
                )
            ).lower()

            if query_lower in searchable:
                results.append(anno)

        return results

    def get_domain_relationships(self, domain: str) -> Dict[str, List[str]]:
        """
        Get related domains for a given domain.

        Returns:
            Dictionary with 'supp', 'related' keys
        """
        relationships = {"supp": [], "related": []}

        # Check for SUPP domain
        supp_domain = f"SUPP{domain}"
        if supp_domain in self.by_domain:
            relationships["supp"].append(supp_domain)

        # Could be extended to detect related domains based on common variables
        # (e.g., domains sharing USUBJID, --SEQ, etc.)

        return relationships

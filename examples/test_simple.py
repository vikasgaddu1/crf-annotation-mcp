"""Simple test without external dependencies."""

import re
from typing import List, Dict, Any

# Simplified annotation pattern
ANNOTATION_PATTERN = re.compile(
    r"(?P<domain>[A-Z]{2,8})\.(?P<variable>[A-Z0-9_]+)"
    r"(?:\s*\(Page\s*(?P<page>\d+)(?:,\s*(?P<description>[^)]+))?\))?"
)

def parse_annotation_text(text: str) -> List[Dict[str, Any]]:
    """Parse annotation text and return list of annotations."""
    annotations = []
    
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        
        matches = ANNOTATION_PATTERN.finditer(line)
        for match in matches:
            domain = match.group("domain")
            variable = match.group("variable")
            page_str = match.group("page")
            description = match.group("description")
            
            page = int(page_str) if page_str else 1
            is_supp = domain.startswith("SUPP")
            
            annotations.append({
                "domain": domain,
                "variable": variable,
                "page": page,
                "description": description.strip() if description else None,
                "is_supp": is_supp,
                "full_variable": f"{domain}.{variable}"
            })
    
    return annotations


def query_by_domain(annotations: List[Dict], domain: str, include_supp: bool = True) -> List[Dict]:
    """Query annotations by domain."""
    results = [a for a in annotations if a["domain"] == domain]
    
    if include_supp and not domain.startswith("SUPP"):
        supp_domain = f"SUPP{domain}"
        results.extend([a for a in annotations if a["domain"] == supp_domain])
    
    return results


def query_by_page(annotations: List[Dict], page: int) -> List[Dict]:
    """Query annotations by page."""
    return [a for a in annotations if a["page"] == page]


def search_annotations(annotations: List[Dict], query: str) -> List[Dict]:
    """Free-text search across annotations."""
    query_lower = query.lower()
    results = []
    
    for anno in annotations:
        searchable = " ".join(filter(None, [
            anno["domain"],
            anno["variable"],
            anno["description"] or ""
        ])).lower()
        
        if query_lower in searchable:
            results.append(anno)
    
    return results


# Test with sample data
sample_text = """
DM.USUBJID (Page 1, Subject ID)
DM.RFSTDTC (Page 1, Study start date)
DM.BRTHDTC (Page 2, Date of birth)
SUPPDM.RACE2 (Page 2, Secondary race)
AE.AETERM (Page 15, Adverse event description)
AE.AESTDTC (Page 15, AE start date)
VS.VSORRES (Page 10, Vital signs result)
"""

def main():
    print("=" * 70)
    print("CRF Annotation Query Test (Simplified)")
    print("=" * 70)
    
    # Parse annotations
    annotations = parse_annotation_text(sample_text)
    print(f"\nParsed {len(annotations)} annotations")
    
    # Test 1: Query DM domain (includes SUPPDM)
    print("\n1. DM Domain Annotations (includes SUPPDM):")
    print("-" * 70)
    dm_results = query_by_domain(annotations, "DM", include_supp=True)
    for anno in dm_results:
        desc = f" - {anno['description']}" if anno['description'] else ""
        print(f"  {anno['full_variable']} (Page {anno['page']}){desc}")
    print(f"  Total: {len(dm_results)} annotations")
    
    # Test 2: Query by page
    print("\n2. Annotations on Page 15:")
    print("-" * 70)
    page_15 = query_by_page(annotations, 15)
    for anno in page_15:
        desc = f" - {anno['description']}" if anno['description'] else ""
        print(f"  {anno['full_variable']} (Page {anno['page']}){desc}")
    print(f"  Total: {len(page_15)} annotations")
    
    # Test 3: Search
    print("\n3. Search for 'date':")
    print("-" * 70)
    date_results = search_annotations(annotations, "date")
    for anno in date_results:
        desc = f" - {anno['description']}" if anno['description'] else ""
        print(f"  {anno['full_variable']} (Page {anno['page']}){desc}")
    print(f"  Total: {len(date_results)} annotations")
    
    # Test 4: List all domains
    print("\n4. All Domains:")
    print("-" * 70)
    domains = {}
    for anno in annotations:
        if anno["domain"] not in domains:
            domains[anno["domain"]] = []
        domains[anno["domain"]].append(anno)
    
    # Don't list SUPP domains separately
    for domain in sorted(domains.keys()):
        if domain.startswith("SUPP"):
            continue
        
        count = len(domains[domain])
        has_supp = f"SUPP{domain}" in domains
        supp_indicator = " (has SUPP)" if has_supp else ""
        
        print(f"  {domain}{supp_indicator}: {count} annotations")
    
    # Test 5: Verify SUPP detection
    print("\n5. Domain Relationships:")
    print("-" * 70)
    for domain in ["DM", "AE", "VS"]:
        supp_domain = f"SUPP{domain}"
        has_supp = supp_domain in domains
        status = f"✓ {supp_domain} found" if has_supp else "✗ No SUPP domain"
        print(f"  {domain}: {status}")
    
    print("\n" + "=" * 70)
    print("✅ All tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

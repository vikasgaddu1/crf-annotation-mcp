"""Example usage of the CRF Annotation Query Engine."""

from crf_annotation_mcp import AnnotationParser, AnnotationQuery

# Example: Parse annotations from text (simulating PDF extraction)
sample_annotations = """
DM.USUBJID (Page 1, Subject ID)
DM.RFSTDTC (Page 1, Study start date)
DM.BRTHDTC (Page 2, Date of birth)
SUPPDM.RACE2 (Page 2, Secondary race)
AE.AETERM (Page 15, Adverse event description)
AE.AESTDTC (Page 15, AE start date)
AE.AESER (Page 16, Serious AE flag)
VS.VSORRES (Page 10, Vital signs result)
VS.VSORRESU (Page 10, Units)
"""

def main():
    """Demonstrate query capabilities."""
    
    # Parse annotations from text
    annotations = AnnotationParser.parse_from_text(sample_annotations)
    
    # Initialize query engine
    query = AnnotationQuery(annotations)
    
    print("=" * 70)
    print("CRF Annotation Query Example")
    print("=" * 70)
    
    # 1. List all domains
    print("\n1. All Domains:")
    print("-" * 70)
    for domain in query.list_domains():
        supp = " (has SUPP)" if domain.has_supp else ""
        print(f"  {domain.domain}{supp}: {domain.annotation_count} annotations")
    
    # 2. Query DM domain (includes SUPPDM)
    print("\n2. DM Domain Annotations (includes SUPPDM):")
    print("-" * 70)
    dm_annotations = query.get_annotations(domain="DM", include_supp=True)
    for anno in dm_annotations:
        print(f"  {anno}")
    
    # 3. Query specific page
    print("\n3. Annotations on Page 15:")
    print("-" * 70)
    page_15 = query.get_annotations(page=15)
    for anno in page_15:
        print(f"  {anno}")
    
    # 4. Search by keyword
    print("\n4. Search for 'date':")
    print("-" * 70)
    date_results = query.search_annotations("date")
    for anno in date_results:
        print(f"  {anno}")
    
    # 5. Page mapping
    print("\n5. Page to Domain Mapping:")
    print("-" * 70)
    for mapping in query.get_page_mapping():
        print(f"  Page {mapping.page}: {', '.join(mapping.domains)}")
    
    # 6. Domain relationships
    print("\n6. DM Domain Relationships:")
    print("-" * 70)
    relationships = query.get_domain_relationships("DM")
    print(f"  SUPP domains: {relationships['supp'] or 'None'}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

"""Tests for annotation query engine."""

import pytest
from crf_annotation_mcp.parser import AnnotationParser
from crf_annotation_mcp.query import AnnotationQuery


@pytest.fixture
def sample_annotations():
    """Create sample annotations for testing."""
    text = """
    DM.USUBJID (Page 1, Subject ID)
    DM.RFSTDTC (Page 1, Study start date)
    DM.BRTHDTC (Page 2, Date of birth)
    SUPPDM.RACE2 (Page 2, Secondary race)
    AE.AETERM (Page 15, Adverse event description)
    AE.AESTDTC (Page 15, AE start date)
    VS.VSORRES (Page 10, Vital signs result)
    """
    return AnnotationParser.parse_from_text(text)


@pytest.fixture
def query_engine(sample_annotations):
    """Create query engine from sample annotations."""
    return AnnotationQuery(sample_annotations)


def test_query_by_domain(query_engine):
    """Test querying by domain."""
    dm_annotations = query_engine.get_annotations(domain="DM", include_supp=False)
    assert len(dm_annotations) == 3
    assert all(a.domain == "DM" for a in dm_annotations)


def test_query_by_domain_with_supp(query_engine):
    """Test querying domain with SUPP included."""
    dm_annotations = query_engine.get_annotations(domain="DM", include_supp=True)
    assert len(dm_annotations) == 4  # 3 DM + 1 SUPPDM
    domains = set(a.domain for a in dm_annotations)
    assert "DM" in domains
    assert "SUPPDM" in domains


def test_query_by_page(query_engine):
    """Test querying by page number."""
    page_15 = query_engine.get_annotations(page=15)
    assert len(page_15) == 2
    assert all(a.page == 15 for a in page_15)
    assert all(a.domain == "AE" for a in page_15)


def test_query_by_variable(query_engine):
    """Test querying by variable name."""
    usubjid = query_engine.get_annotations(variable="USUBJID")
    assert len(usubjid) == 1
    assert usubjid[0].variable == "USUBJID"
    assert usubjid[0].domain == "DM"


def test_list_domains(query_engine):
    """Test listing all domains."""
    domains = query_engine.list_domains()
    
    # Should have DM, AE, VS (SUPPDM not counted separately)
    assert len(domains) == 3
    domain_names = [d.domain for d in domains]
    assert "DM" in domain_names
    assert "AE" in domain_names
    assert "VS" in domain_names
    
    # DM should show it has SUPP
    dm_summary = next(d for d in domains if d.domain == "DM")
    assert dm_summary.has_supp


def test_get_page_mapping(query_engine):
    """Test page to domain mapping."""
    mappings = query_engine.get_page_mapping()
    
    # Should have mappings for pages 1, 2, 10, 15
    assert len(mappings) >= 3
    
    # Page 15 should have AE
    page_15 = next(m for m in mappings if m.page == 15)
    assert "AE" in page_15.domains


def test_search_annotations(query_engine):
    """Test free-text search."""
    # Search for "date"
    date_results = query_engine.search_annotations("date")
    assert len(date_results) >= 2  # RFSTDTC, BRTHDTC, AESTDTC
    
    # Search for "adverse"
    ae_results = query_engine.search_annotations("adverse")
    assert len(ae_results) >= 1
    assert all(a.domain == "AE" for a in ae_results)


def test_get_domain_relationships(query_engine):
    """Test domain relationship detection."""
    dm_rels = query_engine.get_domain_relationships("DM")
    assert "SUPPDM" in dm_rels["supp"]
    
    ae_rels = query_engine.get_domain_relationships("AE")
    assert len(ae_rels["supp"]) == 0  # No SUPPAE in sample data


def test_empty_query_returns_all(query_engine):
    """Test that query with no filters returns all annotations."""
    all_annotations = query_engine.get_annotations()
    assert len(all_annotations) == 7  # Total annotations in sample

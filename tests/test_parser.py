"""Tests for annotation parser."""

import pytest
from crf_annotation_mcp.parser import AnnotationParser


def test_parse_simple_annotation():
    """Test parsing a simple domain.variable annotation."""
    text = "DM.USUBJID"
    annotations = AnnotationParser.parse_from_text(text, page=1)
    
    assert len(annotations) == 1
    assert annotations[0].domain == "DM"
    assert annotations[0].variable == "USUBJID"
    assert annotations[0].page == 1
    assert not annotations[0].is_supp


def test_parse_annotation_with_page():
    """Test parsing annotation with page reference."""
    text = "DM.RFSTDTC (Page 3)"
    annotations = AnnotationParser.parse_from_text(text, page=1)
    
    assert len(annotations) == 1
    assert annotations[0].domain == "DM"
    assert annotations[0].variable == "RFSTDTC"
    assert annotations[0].page == 3  # Should use page from annotation, not default


def test_parse_annotation_with_description():
    """Test parsing annotation with description."""
    text = "DM.BRTHDTC (Page 2, Date of birth)"
    annotations = AnnotationParser.parse_from_text(text, page=1)
    
    assert len(annotations) == 1
    assert annotations[0].domain == "DM"
    assert annotations[0].variable == "BRTHDTC"
    assert annotations[0].page == 2
    assert annotations[0].description == "Date of birth"


def test_parse_supp_domain():
    """Test parsing SUPP domain annotation."""
    text = "SUPPDM.RACE2 (Page 2, Secondary race)"
    annotations = AnnotationParser.parse_from_text(text, page=2)
    
    assert len(annotations) == 1
    assert annotations[0].domain == "SUPPDM"
    assert annotations[0].variable == "RACE2"
    assert annotations[0].is_supp


def test_parse_multiple_annotations():
    """Test parsing multiple annotations from same text."""
    text = """
    DM.USUBJID
    DM.RFSTDTC (Page 3)
    SUPPDM.RACE2 (Page 2, Secondary race)
    """
    annotations = AnnotationParser.parse_from_text(text, page=1)
    
    assert len(annotations) == 3
    domains = [a.domain for a in annotations]
    assert "DM" in domains
    assert "SUPPDM" in domains


def test_parse_ae_domain():
    """Test parsing AE domain annotations."""
    text = "AE.AEDECOD (Page 15, Adverse event description)"
    annotations = AnnotationParser.parse_from_text(text, page=15)
    
    assert len(annotations) == 1
    assert annotations[0].domain == "AE"
    assert annotations[0].variable == "AEDECOD"
    assert annotations[0].page == 15


def test_full_variable_property():
    """Test the full_variable property."""
    text = "VS.VSORRES"
    annotations = AnnotationParser.parse_from_text(text, page=10)
    
    assert annotations[0].full_variable == "VS.VSORRES"


def test_annotation_str_representation():
    """Test string representation of annotation."""
    text = "DM.RFSTDTC (Page 3, Study start date)"
    annotations = AnnotationParser.parse_from_text(text, page=1)
    
    str_repr = str(annotations[0])
    assert "DM.RFSTDTC" in str_repr
    assert "Page 3" in str_repr
    assert "Study start date" in str_repr

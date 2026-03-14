"""Data models for CRF annotations."""

from typing import Optional, List
from pydantic import BaseModel, Field


class Annotation(BaseModel):
    """Represents a single SDTM annotation from a CRF."""

    domain: str = Field(..., description="SDTM domain (e.g., DM, AE, VS)")
    variable: str = Field(..., description="SDTM variable name (e.g., USUBJID, AEDECOD)")
    page: Optional[int] = Field(None, description="CRF page number")
    question: Optional[str] = Field(None, description="CRF question number or identifier")
    description: Optional[str] = Field(None, description="Free-text description")
    raw_text: str = Field(..., description="Original annotation text")
    is_supp: bool = Field(default=False, description="Whether this is a SUPP domain annotation")

    @property
    def full_variable(self) -> str:
        """Returns the fully qualified variable name (DOMAIN.VARIABLE)."""
        return f"{self.domain}.{self.variable}"

    def __str__(self) -> str:
        parts = [self.full_variable]
        if self.page:
            parts.append(f"Page {self.page}")
        if self.question:
            parts.append(f"Q{self.question}")
        if self.description:
            parts.append(f"({self.description})")
        return " - ".join(parts)


class DomainSummary(BaseModel):
    """Summary of annotations for a domain."""

    domain: str
    annotation_count: int
    variables: List[str]
    pages: List[int]
    has_supp: bool = False


class PageMapping(BaseModel):
    """Mapping of CRF page to SDTM domains."""

    page: int
    domains: List[str]
    annotation_count: int

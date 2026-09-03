from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator


class SourceMapping(BaseModel):
    start: int = 0
    length: int = 0
    filename: str = ""
    lines: List[int] = Field(default_factory=list)


class VerificationResult(BaseModel):
    compilation: bool = False
    execution: bool = False
    state_change: bool = False
    impact: bool = False
    reproducibility: bool = False
    logs: str = ""
    evidence_level: str = "E0"


class Finding(BaseModel):
    finding_id: str
    source: str = "slither"
    detector: str
    severity: str = "INFO"
    confidence: str = "UNKNOWN"
    contract: str
    function: Optional[str] = None
    description: str
    source_mapping: Optional[SourceMapping] = None

    # E0-E5 Evidence hierarchy
    static_evidence: bool = True
    build_verified: bool = False
    execution_verified: bool = False
    state_change_verified: bool = False
    economic_impact_verified: bool = False
    reproducible: bool = False

    ai_result: Optional[Dict[str, Any]] = None
    verification_result: Optional[VerificationResult] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def evidence_level(self) -> str:
        """Determine evidence level from E0-E5 hierarchy."""
        if not self.static_evidence:
            return "E0"
        if not self.build_verified:
            return "E1"
        if not self.execution_verified:
            return "E2"
        if not self.state_change_verified:
            return "E3"
        if not self.economic_impact_verified:
            return "E4"
        if not self.reproducible:
            return "E5"
        return "E5+"

    @validator("severity", pre=True)
    def uppercase_severity(cls, v: str) -> str:
        return v.upper() if v else "INFO"

    @validator("confidence", pre=True)
    def uppercase_confidence(cls, v: str) -> str:
        return v.upper() if v else "UNKNOWN"

    @validator("source")
    def default_source(cls, v: str) -> str:
        return v if v else "slither"
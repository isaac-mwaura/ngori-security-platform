from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SourceMapping(BaseModel):
    start: int = 0
    length: int = 0
    filename: str = ""
    lines: List[int] = Field(default_factory=list)


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

    # E0-E5 Evidence
    static_evidence: bool = True
    build_verified: bool = False
    execution_verified: bool = False
    state_change_verified: bool = False
    economic_impact_verified: bool = False
    reproducible: bool = False

    ai_result: Optional[Dict[str, Any]] = None
    verification_result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
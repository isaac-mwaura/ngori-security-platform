from pydantic import BaseModel
from typing import Optional, List, Dict

class SourceMapping(BaseModel):
    start: int
    length: int
    filename: str

class Finding(BaseModel):
    finding_id: str  # e.g., "NGORI-001"
    source: str = "slither"
    detector: str
    severity: str = "INFO"  # e.g., "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"
    confidence: str = "UNKNOWN"  # e.g., "HIGH", "MEDIUM", "LOW"
    contract: str
    function: Optional[str] = None
    description: str
    source_mapping: Optional[SourceMapping] = None

    # Evidence Model (E0-E5)
    static_evidence: bool = True
    build_verified: bool = False
    execution_verified: bool = False
    state_change_verified: bool = False
    economic_impact_verified: bool = False
    reproducible: bool = False
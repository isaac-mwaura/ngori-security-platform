import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from src.models.finding import Finding

def finding_to_record(finding: Finding) -> dict:
    return {
        "schema_version": "ngori-0.1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "finding_id": finding.finding_id,
        "source": finding.source,
        "detector": finding.detector,
        "contract": finding.contract,
        "function": finding.function,
        "severity": finding.severity,
        "confidence": finding.confidence,
        "description": finding.description,
        "source_mapping": finding.source_mapping.model_dump() if finding.source_mapping else None,
        "evidence": {
            "E0_static": finding.static_evidence,
            "E1_build": finding.build_verified,
            "E2_execution": finding.execution_verified,
            "E3_state_change": finding.state_change_verified,
            "E4_economic_impact": finding.economic_impact_verified,
            "E5_reproducible": finding.reproducible,
        },
        "ai": finding.ai_result,
        "verification": finding.verification_result,
        "metadata": finding.metadata,
    }

def export_jsonl(findings: List[Finding], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for finding in findings:
            record = finding_to_record(finding)
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
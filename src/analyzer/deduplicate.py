from typing import List
from src.models.finding import Finding

def deduplicate_findings(findings: List[Finding]) -> List[Finding]:
    """Remove duplicate findings based on a fingerprint."""
    seen = set()
    unique_findings = []
    for finding in findings:
        fingerprint = f"{finding.detector}:{finding.contract}:{finding.function}"
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_findings.append(finding)
    return unique_findings
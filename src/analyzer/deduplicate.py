import hashlib
from typing import List
from src.models.finding import Finding

def deduplicate_findings(findings: List[Finding]) -> List[Finding]:
    seen = set()
    unique = []
    for finding in findings:
        mapping = finding.source_mapping
        fingerprint = "|".join([
            finding.detector,
            finding.contract,
            finding.function or "",
            str(mapping.start if mapping else 0),
            str(mapping.length if mapping else 0),
        ])
        digest = hashlib.sha256(fingerprint.encode()).hexdigest()
        if digest not in seen:
            seen.add(digest)
            unique.append(finding)
    return unique
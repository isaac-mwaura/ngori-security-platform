import hashlib
from typing import List
from src.models.finding import Finding


def deduplicate_findings(findings: List[Finding]) -> List[Finding]:
    """Deterministically deduplicate findings using a canonical fingerprint.

    Two findings are considered duplicates if they share the same:
    - detector
    - contract
    - function
    - source location (start/length)

    The fingerprint is a SHA-256 hash of the canonical tuple, ensuring
    deterministic behavior across runs.
    """
    seen: set = set()
    unique: List[Finding] = []

    for finding in findings:
        mapping = finding.source_mapping
        if mapping is None:
            fingerprint = hashlib.sha256(
                "|".join([
                    finding.detector,
                    finding.contract,
                    finding.function or "",
                    "0",
                    "0",
                ]).encode()
            ).hexdigest()
        else:
            fingerprint = hashlib.sha256(
                "|".join([
                    finding.detector,
                    finding.contract,
                    finding.function or "",
                    str(mapping.start if mapping else 0),
                    str(mapping.length if mapping else 0),
                ]).encode()
            ).hexdigest()

        if fingerprint not in seen:
            seen.add(fingerprint)
            unique.append(finding)

    return unique
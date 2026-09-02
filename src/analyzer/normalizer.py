import json
import hashlib
from typing import List
from src.models.finding import Finding, SourceMapping

def normalize_slither_output(raw_json_path: str) -> List[Finding]:
    findings = []
    with open(raw_json_path, 'r') as f:
        data = json.load(f)

    # Slither's structure: data["results"]["detectors"] is a list
    detectors = data.get("results", {}).get("detectors", [])

    for detector in detectors:
        if not isinstance(detector, dict):
            continue
        for element in detector.get("elements", []):
            if not isinstance(element, dict):
                continue
            # Create a deterministic ID
            id_hash = hashlib.sha256(
                f"{detector.get('name', 'unknown')}{element.get('name', 'unknown')}".encode()
            ).hexdigest()[:8]
            finding_id = f"NGORI-{id_hash}"

            mapping = SourceMapping(
                start=element.get("source_mapping", {}).get("start", 0),
                length=element.get("source_mapping", {}).get("length", 0),
                filename=element.get("source_mapping", {}).get("filename_short", "")
            )

            finding = Finding(
                finding_id=finding_id,
                detector=detector.get('name', 'unknown'),
                severity=detector.get("severity", "INFO").upper(),
                confidence=detector.get("confidence", "UNKNOWN").upper(),
                contract=element.get("name", "Unknown"),
                description=element.get("description", "No description"),
                source_mapping=mapping
            )
            findings.append(finding)

    return findings
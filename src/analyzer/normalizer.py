import hashlib
import json
from typing import List
from src.models.finding import Finding, SourceMapping

def normalize_slither_output(raw_json_path: str) -> List[Finding]:
    findings = []
    with open(raw_json_path, "r") as f:
        data = json.load(f)

    detectors = data.get("results", {}).get("detectors", [])

    for detector in detectors:
        if not isinstance(detector, dict):
            continue

        detector_name = detector.get("check", detector.get("name", "unknown"))
        severity = detector.get("impact", detector.get("severity", "INFO")).upper()
        confidence = detector.get("confidence", "UNKNOWN").upper()
        description = detector.get("description", "No description")
        elements = detector.get("elements", [])

        for element in elements:
            if not isinstance(element, dict):
                continue

            mapping_data = element.get("source_mapping", {})
            type_specific = element.get("type_specific_fields", {})
            parent = type_specific.get("parent", {})

            # Extract contract name - try multiple approaches
            contract_name = "Unknown"

            # Method 1: parent.type == "contract" (most common in Slither output)
            if isinstance(parent, dict) and parent.get("type") == "contract":
                contract_name = parent.get("name", "Unknown")

            # Method 2: from source mapping filename
            if contract_name == "Unknown":
                filename = mapping_data.get("filename_short", "")
                if filename:
                    contract_name = filename.replace(".sol", "")

            # Method 3: traverse up through type_specific_fields
            if contract_name == "Unknown":
                current = parent
                max_iterations = 10
                for _ in range(max_iterations):
                    if isinstance(current, dict) and current.get("type") == "contract":
                        contract_name = current.get("name", "Unknown")
                        break
                    parent_fields = current.get("type_specific_fields", {})
                    if isinstance(parent_fields, dict):
                        current = parent_fields.get("parent", {})
                    else:
                        break

            function_name = None
            if element.get("type") == "function":
                function_name = element.get("name")
            elif isinstance(parent, dict) and parent.get("type") == "function":
                function_name = parent.get("name")

            source_lines = mapping_data.get("lines", [])

            fingerprint = "|".join([
                detector_name,
                contract_name,
                function_name or "",
                str(mapping_data.get("start", 0)),
                str(mapping_data.get("length", 0)),
            ])
            finding_hash = hashlib.sha256(fingerprint.encode()).hexdigest()[:12]

            finding = Finding(
                finding_id=f"NGORI-{finding_hash}",
                detector=detector_name,
                severity=severity,
                confidence=confidence,
                contract=contract_name,
                function=function_name,
                description=description,
                source_mapping=SourceMapping(
                    start=mapping_data.get("start", 0),
                    length=mapping_data.get("length", 0),
                    filename=mapping_data.get("filename_short", ""),
                    lines=source_lines,
                ),
                metadata={
                    "slither_id": detector.get("id"),
                    "reference": detector.get("reference"),
                    "element_type": element.get("type"),
                },
            )
            findings.append(finding)

    return findings
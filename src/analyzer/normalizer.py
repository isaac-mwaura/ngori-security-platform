import hashlib
import json
import logging
from typing import List, Optional, Dict, Any

from src.models.finding import Finding, SourceMapping

logger = logging.getLogger(__name__)


def _extract_contract_name(parent: dict, filename_short: str, max_iterations: int = 10) -> str:
    """Extract contract name from parent dict, falling back to filename."""
    if parent.get("type") == "contract":
        return parent.get("name", "Unknown")

    # Traverse up through type_specific_fields
    current = parent
    for _ in range(max_iterations):
        if isinstance(current, dict) and current.get("type") == "contract":
            return current.get("name", "Unknown")
        parent_fields = current.get("type_specific_fields", {})
        if isinstance(parent_fields, dict):
            current = parent_fields.get("parent", {})
        else:
            break

    # Fallback to filename
    if filename_short:
        return filename_short.replace(".sol", "")
    return "Unknown"


def normalize_slither_output(raw_json_path: str) -> List[Finding]:
    """Normalize Slither JSON output into NGORI Finding model objects.

    Maps Slither's tool-specific output to NGORI's canonical finding schema.
    Preserves provenance (original detector names) and handles edge cases
    like missing fields, malformed JSON, and unexpected structures.
    """
    findings = []
    try:
        with open(raw_json_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        logger.error("Failed to load Slither output: %s", exc)
        return findings

    detectors = data.get("results", {}).get("detectors", [])

    if not detectors:
        logger.warning("No detectors found in Slither output")
        return findings

    for detector in detectors:
        if not isinstance(detector, dict):
            continue

        detector_name = detector.get("check", detector.get("name", "unknown"))
        severity = detector.get("impact", detector.get("severity", "INFO")).upper()
        confidence = detector.get("confidence", "UNKNOWN").upper()
        description = detector.get("description", "No description")
        elements = detector.get("elements", [])

        if not isinstance(elements, list):
            logger.warning("Expected elements list, got %s", type(elements))
            continue

        for element in elements:
            if not isinstance(element, dict):
                continue

            mapping_data = element.get("source_mapping", {})
            type_specific = element.get("type_specific_fields", {})
            parent = type_specific.get("parent", {}) if isinstance(type_specific, dict) else {}

            # Extract contract name - try multiple approaches
            contract_name = "Unknown"

            # Method 1: parent.type == "contract" (most common in Slither output)
            if isinstance(parent, dict) and parent.get("type") == "contract":
                contract_name = parent.get("name", "Unknown")

            # Method 2: from source mapping filename
            if contract_name == "Unknown":
                filename = mapping_data.get("filename_short", "")
                if filename:
                    contract_name = _extract_contract_name(parent, filename)

            # Method 3: traverse up through type_specific_fields
            if contract_name == "Unknown":
                contract_name = _extract_contract_name(parent, mapping_data.get("filename_short", ""), max_iterations=10)

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
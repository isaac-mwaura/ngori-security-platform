from collections import Counter
from typing import Any, Dict, List
from src.models.contract import Contract
from src.models.finding import Finding
from src.ai.router import GroqRouter

SYSTEM_PROMPT = """
You are NGORI's smart-contract security analyst.

Analyze ONLY the supplied evidence.

Do not invent source code, execution results, or impact.

Return valid JSON with exactly these fields:

{
  "classification": "vulnerability | informational | false_positive",
  "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
  "confidence": "HIGH | MEDIUM | LOW",
  "reason": "short evidence-based explanation",
  "false_positive_risk": "HIGH | MEDIUM | LOW",
  "recommended_verification": "specific verification step"
}
"""

def _messages(finding: Finding) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Detector: {finding.detector}
Slither severity: {finding.severity}
Slither confidence: {finding.confidence}
Contract: {finding.contract}
Function: {finding.function or "N/A"}

Description:
{finding.description}

Source mapping:
{finding.source_mapping.model_dump() if finding.source_mapping else "N/A"}
"""},
    ]


def triage_vulnerabilities(contract: Contract) -> Dict[str, Any]:
    if not contract.vulnerabilities:
        return {"priority": "SAFE", "recommendation": "No issues found", "actions": []}

    severities = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for vulnerability in contract.vulnerabilities:
        severities[vulnerability.severity] = severities.get(vulnerability.severity, 0) + 1

    if severities["CRITICAL"] > 0:
        priority = "IMMEDIATE"
        recommendation = "Critical vulnerabilities found - fix immediately"
    elif severities["HIGH"] > 1:
        priority = "URGENT"
        recommendation = "High severity issues require urgent attention"
    elif severities["HIGH"] > 0 or severities["MEDIUM"] > 2:
        priority = "HIGH"
        recommendation = "Significant issues need to be addressed"
    elif severities["MEDIUM"] > 0:
        priority = "MEDIUM"
        recommendation = "Medium priority issues should be reviewed"
    else:
        priority = "LOW"
        recommendation = "Minor issues can be addressed in routine maintenance"

    actions = [
        f"Fix {vulnerability.name} ({vulnerability.severity})"
        for vulnerability in contract.vulnerabilities
        if vulnerability.severity in ["CRITICAL", "HIGH"]
    ]
    if not actions:
        actions.append("Review all vulnerabilities")

    return {
        "priority": priority,
        "recommendation": recommendation,
        "actions": actions[:3],
        "severity_counts": severities,
    }

def groq_triage_finding(
    finding: Finding,
    passes: int = 4,
) -> Dict[str, Any]:
    router = GroqRouter()
    results = []
    passes = max(1, min(passes, router.available() or 1))

    for _ in range(passes):
        result = router.complete_json(_messages(finding))
        if "error" not in result:
            results.append(result)

    if not results:
        return {"error": "AI triage failed", "votes": []}

    def majority(field: str, default: str):
        values = [r.get(field, default) for r in results]
        return Counter(values).most_common(1)[0][0]

    classifications = [r.get("classification", "informational") for r in results]
    classification = majority("classification", "informational")
    severity = majority("severity", finding.severity)
    confidence = majority("confidence", "LOW")
    false_positive_risk = majority("false_positive_risk", "MEDIUM")

    reasons = []
    verification = []
    for result in results:
        if result.get("reason"):
            reasons.append(result["reason"])
        if result.get("recommended_verification"):
            verification.append(result["recommended_verification"])

    agreement = Counter(classifications).most_common(1)[0][1] / len(classifications)

    return {
        "classification": classification,
        "severity": severity,
        "confidence": confidence,
        "reason": reasons[0] if reasons else "",
        "false_positive_risk": false_positive_risk,
        "recommended_verification": verification[0] if verification else "",
        "ensemble": {
            "passes": len(results),
            "agreement": round(agreement, 3),
            "votes": results,
        },
    }
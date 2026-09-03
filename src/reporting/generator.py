from typing import List
from src.models.finding import Finding

def generate_report(findings: List[Finding], output_path: str) -> None:
    report = f"# NGORI Security Report\n\n**Total Findings:** {len(findings)}\n\n"
    if not findings:
        report += "No findings were identified.\n"

    for finding in findings:
        report += f"## {finding.finding_id}: {finding.detector}\n\n"
        report += f"- **Severity:** {finding.severity}\n"
        report += f"- **Confidence:** {finding.confidence}\n"
        report += f"- **Contract:** `{finding.contract}`\n"
        if finding.function:
            report += f"- **Function:** `{finding.function}`\n"
        report += f"- **Description:** {finding.description}\n\n"
        report += "### Evidence\n\n"
        report += f"- E0 Static: {'✅ PASS' if finding.static_evidence else '❌ FAIL'}\n"
        report += f"- E1 Build: {'✅ PASS' if finding.build_verified else '❌ FAIL'}\n"
        report += f"- E2 Execution: {'✅ PASS' if finding.execution_verified else '❌ FAIL'}\n"
        report += f"- E3 State Change: {'✅ PASS' if finding.state_change_verified else '❌ FAIL'}\n"
        report += f"- E4 Impact: {'✅ PASS' if finding.economic_impact_verified else '❌ FAIL'}\n"
        report += f"- E5 Reproducible: {'✅ PASS' if finding.reproducible else '❌ FAIL'}\n\n"
        if finding.ai_result:
            ai = finding.ai_result
            report += "### AI Assessment\n\n"
            report += f"- Classification: {ai.get('classification', 'N/A')}\n"
            report += f"- Severity: {ai.get('severity', 'N/A')}\n"
            report += f"- Confidence: {ai.get('confidence', 'N/A')}\n"
            report += f"- False-positive risk: {ai.get('false_positive_risk', 'N/A')}\n"
            report += f"- Reason: {ai.get('reason', 'N/A')}\n"
            ensemble = ai.get("ensemble", {})
            if ensemble:
                report += f"- Ensemble agreement: {ensemble.get('agreement', 'N/A')}\n"
        report += "\n---\n\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
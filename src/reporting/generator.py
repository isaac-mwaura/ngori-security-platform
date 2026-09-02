from typing import List
from src.models.finding import Finding

def generate_report(findings: List[Finding], output_path: str) -> None:
    """Generate a human-readable markdown report."""
    report = "# NGORI Security Report\n\n"

    if not findings:
        report += "No findings were identified.\n"
        with open(output_path, 'w') as f:
            f.write(report)
        return

    report += f"**Total Findings:** {len(findings)}\n\n"

    for finding in findings:
        report += f"## {finding.finding_id}: {finding.detector}\n"
        report += f"- **Severity:** {finding.severity}\n"
        report += f"- **Confidence:** {finding.confidence}\n"
        report += f"- **Contract:** `{finding.contract}`\n"
        if finding.function:
            report += f"- **Function:** `{finding.function}`\n"
        report += f"- **Description:** {finding.description}\n\n"
        report += "### Evidence:\n"
        report += f"- **E0 (Static):** {'✅' if finding.static_evidence else '❌'}\n"
        report += f"- **E1 (Build):** {'✅' if finding.build_verified else '❌'}\n"
        report += f"- **E2 (Execution):** {'✅' if finding.execution_verified else '❌'}\n"
        report += f"- **E3 (State Change):** {'✅' if finding.state_change_verified else '❌'}\n"
        report += f"- **E4 (Economic/Privilege Impact):** {'✅' if finding.economic_impact_verified else '❌'}\n"
        report += f"- **E5 (Reproducible):** {'✅' if finding.reproducible else '❌'}\n"
        report += "\n---\n\n"

    with open(output_path, 'w') as f:
        f.write(report)
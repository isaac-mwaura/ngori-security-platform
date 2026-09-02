from typing import Dict, Any
from ..models.contract import Contract

def generate_report(contract: Contract, triage_result: Dict[str, Any]) -> str:
    """
    Generate a human-readable security report.
    """
    summary = contract.summary()
    
    report = f"""
# Security Audit Report
## Contract: {contract.name}

### Executive Summary
- Total Issues: {summary['total_issues']}
- Priority Level: {triage_result['priority']}
- Recommendation: {triage_result['recommendation']}

### Severity Distribution
- CRITICAL: {triage_result['severity_counts'].get('CRITICAL', 0)}
- HIGH: {triage_result['severity_counts'].get('HIGH', 0)}
- MEDIUM: {triage_result['severity_counts'].get('MEDIUM', 0)}
- LOW: {triage_result['severity_counts'].get('LOW', 0)}

### Recommended Actions
"""
    
    for i, action in enumerate(triage_result['actions'], 1):
        report += f"{i}. {action}\n"
    
    report += "\n### Detailed Findings\n"
    
    for vuln in contract.vulnerabilities:
        report += f"""
#### {vuln.name} ({vuln.severity})
- Description: {vuln.description}
- Lines: {', '.join(map(str, vuln.line_numbers))}
- Recommendation: {vuln.recommendation}
"""
    
    report += """
### Conclusion
This report was generated using automated static analysis and AI triage.
Manual review is recommended for critical vulnerabilities.
"""
    
    return report
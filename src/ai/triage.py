from typing import Dict, Any, List
from ..models.contract import Contract, Vulnerability

def triage_vulnerabilities(contract: Contract) -> Dict[str, Any]:
    """
    Use AI to triage and prioritize vulnerabilities.
    
    This simulates AI triage - in production, this would use an LLM.
    """
    if not contract.vulnerabilities:
        return {"priority": "SAFE", "recommendation": "No issues found", "actions": []}
    
    # Count severities
    severities = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for vuln in contract.vulnerabilities:
        severities[vuln.severity] = severities.get(vuln.severity, 0) + 1
    
    # Determine priority
    if severities["CRITICAL"] > 0:
        priority = "IMMEDIATE"
        recommendation = "Critical vulnerabilities found - fix immediately"
    elif severities["HIGH"] > 1 or severities["CRITICAL"] > 0:
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
    
    # Generate triage actions
    actions = []
    for vuln in contract.vulnerabilities:
        if vuln.severity in ["CRITICAL", "HIGH"]:
            actions.append(f"Fix {vuln.name} ({vuln.severity})")
    
    if not actions:
        actions.append("Review all vulnerabilities")
    
    return {
        "priority": priority,
        "recommendation": recommendation,
        "actions": actions[:3],  # Limit to top 3
        "severity_counts": severities
    }
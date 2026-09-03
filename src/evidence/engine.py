from src.models.finding import Finding

def update_evidence(finding: Finding, verification_result: dict) -> Finding:
    finding.verification_result = verification_result
    finding.build_verified = bool(verification_result.get("build", False))
    finding.execution_verified = bool(verification_result.get("execution", False))
    finding.state_change_verified = bool(verification_result.get("state_change", False))
    finding.economic_impact_verified = bool(verification_result.get("impact", False))
    finding.reproducible = bool(verification_result.get("reproducible", False))
    return finding
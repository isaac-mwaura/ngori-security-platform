from src.models.finding import Finding

def update_evidence(finding: Finding, verification_result: dict) -> Finding:
    """Update a finding's evidence model with verification results."""
    finding.build_verified = verification_result.get("build", False)
    finding.execution_verified = verification_result.get("test", False)
    finding.state_change_verified = verification_result.get("state_change", False)
    finding.economic_impact_verified = verification_result.get("impact", False)
    finding.reproducible = verification_result.get("reproducible", False)
    return finding
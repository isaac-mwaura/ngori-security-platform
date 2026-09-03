from src.models.finding import Finding, VerificationResult


def update_evidence(finding: Finding, verification_result: dict) -> Finding:
    """Update finding evidence level based on Foundry verification results.

    Implements the E0-E5 evidence hierarchy:
    E0 - Static: Slither identified the issue
    E1 - Build: The candidate verification harness compiles
    E2 - Execution: The PoC/test actually executes successfully
    E3 - State Change: We demonstrate an actual relevant state transition
    E4 - Impact: Security-relevant consequence demonstrated
    E5 - Reproducibility: Independently reproducible in clean environment

    No shortcuts: E0 → detected, E1 → compiled, E2 → executed, E3 → state changed,
    E4 → security impact demonstrated, E5 → independently reproducible.
    """
    finding.verification_result = VerificationResult(
        compilation=verification_result.get("build", False),
        execution=verification_result.get("execution", False),
        state_change=verification_result.get("state_change", False),
        impact=verification_result.get("impact", False),
        reproducibility=verification_result.get("reproducible", False),
        logs=verification_result.get("stderr", "") + "\n" + verification_result.get("stdout", ""),
    )

    # E0: Static evidence (Slither always runs if we have findings)
    finding.static_evidence = True

    # E1: Build verified
    finding.build_verified = bool(verification_result.get("build", False))

    # E2: Execution verified (only if build passed)
    finding.execution_verified = bool(
        verification_result.get("execution", False)
        and verification_result.get("build", False)
    )

    # E3: State change verified (only if execution passed)
    finding.state_change_verified = bool(
        verification_result.get("state_change", False)
        and verification_result.get("execution", False)
        and verification_result.get("build", False)
    )

    # E4: Economic impact demonstrated (only if state change confirmed)
    finding.economic_impact_verified = bool(
        verification_result.get("impact", False)
        and verification_result.get("state_change", False)
        and verification_result.get("execution", False)
        and verification_result.get("build", False)
    )

    # E5: Reproducibility (only if all above passed)
    finding.reproducible = bool(
        verification_result.get("reproducible", False)
        and verification_result.get("impact", False)
        and verification_result.get("state_change", False)
        and verification_result.get("execution", False)
        and verification_result.get("build", False)
    )

    return finding
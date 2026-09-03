from dataclasses import dataclass
from typing import List, Optional
from src.models.finding import Finding, VerificationResult


@dataclass
class Vulnerability:
    """Represents a security vulnerability in a contract."""
    name: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    line_numbers: List[int]
    recommendation: str


@dataclass
class Contract:
    """Represents a smart contract."""
    name: str
    code: str
    vulnerabilities: Optional[List[Vulnerability]] = None
    findings: Optional[List[Finding]] = None

    def has_issues(self) -> bool:
        """Check if the contract has any vulnerabilities."""
        return bool(self.vulnerabilities or (self.findings and len(self.findings) > 0))

    def summary(self) -> dict:
        """Generate a summary of the contract."""
        issues: List[dict] = []

        if self.vulnerabilities:
            for vuln in self.vulnerabilities:
                issues.append({
                    "name": vuln.name,
                    "severity": vuln.severity,
                    "description": vuln.description,
                    "line_numbers": vuln.line_numbers,
                })

        if self.findings:
            for finding in self.findings:
                issues.append({
                    "finding_id": finding.finding_id,
                    "detector": finding.detector,
                    "severity": finding.severity,
                    "evidence_level": finding.evidence_level,
                })

        severities = {}
        for issue in issues:
            sev = issue.get("severity", "INFO")
            severities[sev] = severities.get(sev, 0) + 1

        return {
            "name": self.name,
            "total_issues": len(issues),
            "severities": severities,
            "findings": len(self.findings) if self.findings else 0,
        }
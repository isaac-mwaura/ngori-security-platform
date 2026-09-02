from dataclasses import dataclass
from typing import List, Optional

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
    
    def has_issues(self) -> bool:
        """Check if the contract has any vulnerabilities."""
        return bool(self.vulnerabilities)
    
    def summary(self) -> dict:
        """Generate a summary of the contract."""
        if not self.vulnerabilities:
            return {"name": self.name, "total_issues": 0, "severities": {}}
        
        severities = {}
        for vuln in self.vulnerabilities:
            severities[vuln.severity] = severities.get(vuln.severity, 0) + 1
        
        return {
            "name": self.name,
            "total_issues": len(self.vulnerabilities),
            "severities": severities
        }
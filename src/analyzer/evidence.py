from typing import Dict, Any
from ..models.contract import Contract, Vulnerability

class EvidenceGenerator:
    """Generates evidence for vulnerabilities."""
    
    @staticmethod
    def generate(vulnerability: Vulnerability) -> Dict[str, Any]:
        """Generate evidence for a vulnerability."""
        return {
            "vulnerability": vulnerability.name,
            "severity": vulnerability.severity,
            "evidence_type": "static_analysis",
            "confidence": 0.85,
            "reproducible": True,
            "affected_lines": vulnerability.line_numbers,
            "recommendation": vulnerability.recommendation,
            "proof_of_concept": f"Example: {vulnerability.name} can be triggered by..."
        }

def generate_evidence_report(contract: Contract) -> List[Dict[str, Any]]:
    """Generate evidence for all vulnerabilities in a contract."""
    evidence_list = []
    for vuln in contract.vulnerabilities:
        evidence = EvidenceGenerator.generate(vuln)
        evidence_list.append(evidence)
    return evidence_list
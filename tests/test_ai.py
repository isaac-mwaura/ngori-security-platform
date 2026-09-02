import unittest
from src.models.contract import Contract, Vulnerability
from src.ai.triage import triage_vulnerabilities
from src.ai.reporter import generate_report

class TestAI(unittest.TestCase):
    
    def test_triage_without_issues(self):
        contract = Contract(
            name="SecureContract",
            code="// Secure code",
            vulnerabilities=[]
        )
        
        result = triage_vulnerabilities(contract)
        
        self.assertEqual(result['priority'], "SAFE")
        self.assertEqual(result['recommendation'], "No issues found")
    
    def test_triage_critical_priority(self):
        contract = Contract(
            name="VulnerableContract",
            code="vulnerable",
            vulnerabilities=[
                Vulnerability(
                    name="Critical Issue",
                    severity="CRITICAL",
                    description="Critical bug",
                    line_numbers=[1],
                    recommendation="Fix immediately"
                )
            ]
        )
        
        result = triage_vulnerabilities(contract)
        
        self.assertEqual(result['priority'], "IMMEDIATE")
        self.assertGreater(result['severity_counts']['CRITICAL'], 0)
        self.assertGreater(len(result['actions']), 0)
    
    def test_report_generation(self):
        contract = Contract(
            name="TestContract",
            code="test",
            vulnerabilities=[
                Vulnerability(
                    name="Test Issue",
                    severity="HIGH",
                    description="Test description",
                    line_numbers=[1],
                    recommendation="Test recommendation"
                )
            ]
        )
        
        triage = triage_vulnerabilities(contract)
        report = generate_report(contract, triage)
        
        self.assertIn("TestContract", report)
        self.assertIn("Test Issue", report)
        self.assertIn("HIGH", report)

if __name__ == "__main__":
    unittest.main()
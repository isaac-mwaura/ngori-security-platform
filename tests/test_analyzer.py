import unittest
from src.models.contract import Contract, Vulnerability
from src.analyzer.static import run_static_analysis
from src.analyzer.evidence import EvidenceGenerator, generate_evidence_report

class TestAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.contract = Contract(
            name="TestContract",
            code="tx.origin block.timestamp call.value delegatecall selfdestruct"
        )
    
    def test_static_analysis_finds_issues(self):
        result = run_static_analysis(self.contract)
        self.assertTrue(result.has_issues())
        self.assertGreaterEqual(len(result.vulnerabilities), 1)
    
    def test_static_analysis_identifies_specific_issues(self):
        result = run_static_analysis(self.contract)
        vuln_names = [v.name for v in result.vulnerabilities]
        
        self.assertIn("Use of tx.origin", vuln_names)
        self.assertIn("Timestamp Manipulation", vuln_names)
        self.assertIn("Unsafe External Call", vuln_names)
    
    def test_evidence_generator(self):
        vuln = Vulnerability(
            name="Test Vulnerability",
            severity="HIGH",
            description="Test description",
            line_numbers=[1, 2],
            recommendation="Fix it"
        )
        
        evidence = EvidenceGenerator.generate(vuln)
        
        self.assertEqual(evidence['vulnerability'], "Test Vulnerability")
        self.assertEqual(evidence['severity'], "HIGH")
        self.assertTrue(evidence['reproducible'])
    
    def test_evidence_report(self):
        contract = Contract(
            name="TestContract",
            code="tx.origin call.value"
        )
        contract = run_static_analysis(contract)
        
        evidence_list = generate_evidence_report(contract)
        
        self.assertEqual(len(evidence_list), len(contract.vulnerabilities))

if __name__ == "__main__":
    unittest.main()
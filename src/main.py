import subprocess
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from src.analyzer.normalizer import normalize_slither_output
from src.analyzer.deduplicate import deduplicate_findings
from src.ai.triage import groq_triage_finding
from src.ai.router import GroqRouter
from src.verification.foundry import run_foundry_test
from src.evidence.engine import update_evidence
from src.reporting.generator import generate_report
from src.models.finding import Finding

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
BLOCKCHAIN_DIR = PROJECT_ROOT / "blockchain"

def run_slither(contract_path: str, output_path: str) -> None:
    """Run Slither static analysis on a contract."""
    abs_contract = os.path.abspath(contract_path)
    abs_output = os.path.abspath(output_path)
    env = os.environ.copy()
    env["PATH"] = f"{os.path.expanduser('/home/arch/.config/.foundry/bin')}:{env.get('PATH', '')}"
    subprocess.run(
        ["slither", abs_contract, "--json", abs_output],
        cwd=BLOCKCHAIN_DIR,
        env=env,
        timeout=120
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <contract_file.sol>")
        sys.exit(1)

    contract_path = sys.argv[1]
    print(f"\n🔍 Analyzing contract: {Path(contract_path).stem}")
    print("=" * 60)

    # 1. Run Slither
    print("📊 Running Slither static analysis...")
    raw_json_path = BLOCKCHAIN_DIR / "evidence" / "slither_raw.json"
    os.makedirs(BLOCKCHAIN_DIR / "evidence", exist_ok=True)
    run_slither(contract_path, str(raw_json_path))

    # 2. Normalize Findings
    print("📝 Normalizing findings...")
    findings = normalize_slither_output(str(raw_json_path))

    # 3. Deduplicate
    print("🧹 Deduplicating findings...")
    findings = deduplicate_findings(findings)

    if not findings:
        print("No findings detected. Exiting.")
        sys.exit(0)

    # 4. AI Triage & Verification
    print("🤖 AI Triage in progress...")
    router = GroqRouter()
    verified_findings = []
    for finding in findings:
        # Triage
        ai_result = groq_triage_finding(finding)
        # Update finding with AI result if needed
        # ...

        # Verify
        verification_result = run_foundry_test(str(contract_path))
        finding = update_evidence(finding, verification_result)
        verified_findings.append(finding)

    # 5. Generate Report
    print("📄 Generating report...")
    report_path = PROJECT_ROOT / "reports" / f"{Path(contract_path).stem}.md"
    os.makedirs(PROJECT_ROOT / "reports", exist_ok=True)
    generate_report(verified_findings, str(report_path))

    print(f"✅ Report generated: {report_path}")

if __name__ == "__main__":
    main()
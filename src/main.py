import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from src.analyzer.normalizer import normalize_slither_output
from src.analyzer.deduplicate import deduplicate_findings
from src.ai.triage import groq_triage_finding
from src.verification.foundry import run_foundry_test
from src.evidence.engine import update_evidence
from src.reporting.generator import generate_report
from src.dataset.exporter import export_jsonl

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BLOCKCHAIN_DIR = PROJECT_ROOT / "blockchain"
EVIDENCE_DIR = BLOCKCHAIN_DIR / "evidence"
REPORT_DIR = PROJECT_ROOT / "reports"
DATASET_DIR = PROJECT_ROOT / "dataset"


def run_slither(contract_path: str, output_path: str) -> None:
    """Run Slither static analysis on a contract.

    Slither may return non-zero exit code when vulnerabilities are found,
    but the JSON output is still valid. We check that output was generated,
    not that the process exit code.
    """
    contract = Path(contract_path).resolve()
    output = Path(output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["slither", str(contract), "--json", str(output)],
        capture_output=True,
        text=True,
        timeout=120,
    )

    # Slither may return 1 if vulnerabilities found, but output JSON is still valid
    if not output.exists():
        raise RuntimeError("Slither failed to generate output:\n" + result.stderr)


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <contract_file.sol>")
        sys.exit(1)

    contract_path = Path(sys.argv[1]).resolve()
    if not contract_path.exists():
        print(f"Contract not found: {contract_path}")
        sys.exit(1)

    print(f"\n🔍 Analyzing: {contract_path.name}")
    print("=" * 60)

    raw_json = EVIDENCE_DIR / "slither_raw.json"

    # E0: Static Analysis - Slither runs and produces JSON output
    print("📊 Running Slither (E0: Static)...")
    run_slither(str(contract_path), str(raw_json))

    # Normalize Slither output into NGORI Finding model objects
    print("📝 Normalizing findings...")
    findings = normalize_slither_output(str(raw_json))

    # Deduplicate findings using deterministic fingerprinting
    print("🧹 Deduplicating...")
    findings = deduplicate_findings(findings)

    if not findings:
        print("No findings detected.")
        sys.exit(0)

    print(f"Found {len(findings)} findings.")

    # AI + Verification for each finding
    for index, finding in enumerate(findings, start=1):
        print(f"\n🤖 Finding {index}/{len(findings)}: {finding.detector}")

        # AI Triage (Groq consensus-based, with deterministic fallback)
        print("   AI triage...")
        ai_result = groq_triage_finding(finding, passes=4)
        finding.ai_result = ai_result
        ai_classification = ai_result.get("classification", "ERROR")
        print(f"   AI classification: {ai_classification}")

        # Foundry Verification
        print("   🔬 Running Foundry verification...")
        verification = run_foundry_test(str(contract_path))
        finding = update_evidence(finding, verification)

        # Classify evidence level
        ev_level = finding.evidence_level
        print(f"   Evidence level: {ev_level}")

    # Generate Reports
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"{contract_path.stem}.md"
    generate_report(findings, str(report_path))

    # Export Dataset
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    dataset_path = DATASET_DIR / f"{contract_path.stem}.jsonl"
    export_jsonl(findings, str(dataset_path))

    print("\n" + "=" * 60)
    print("✅ NGORI COMPLETE")
    print(f"📄 Report: {report_path}")
    print(f"🧠 Dataset: {dataset_path}")
    print(f"📊 Evidence levels: {[f.evidence_level for f in findings]}")


if __name__ == "__main__":
    main()
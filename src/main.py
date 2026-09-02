import sys
import json
from pathlib import Path
from .models.contract import Contract
from .analyzer.static import run_static_analysis
from .analyzer.evidence import generate_evidence_report
from .ai.triage import triage_vulnerabilities
from .ai.reporter import generate_report
from .utils.validators import validate_contract_code

def main():
    """Command-line interface for the security platform."""
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <contract_file.sol>")
        print("Example: python -m src.main examples/vulnerable_contract.sol")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Read contract
    try:
        with open(file_path, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)
    
    # Validate contract
    is_valid, errors = validate_contract_code(code)
    if not is_valid:
        print("ERROR: Invalid contract code:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    # Create contract object
    contract = Contract(
        name=Path(file_path).stem,
        code=code
    )
    
    print(f"\n🔍 Analyzing contract: {contract.name}")
    print("=" * 60)
    
    # Run analysis
    print("\n📊 Running static analysis...")
    contract = run_static_analysis(contract)
    
    # Generate evidence
    print("📝 Generating evidence...")
    evidence = generate_evidence_report(contract)
    
    # AI triage
    print("🤖 AI triage in progress...")
    triage_result = triage_vulnerabilities(contract)
    
    # Generate report
    print("📄 Generating report...")
    report = generate_report(contract, triage_result)
    
    # Display results
    print("\n" + "=" * 60)
    print("📋 ANALYSIS COMPLETE")
    print("=" * 60)
    print(report)
    
    # Save report
    output_file = f"{contract.name}_report.txt"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_file}")

if __name__ == "__main__":
    main()
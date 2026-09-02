# NGORI Security Platform

AI-assisted smart contract security analysis platform with evidence-based reporting.

## Features

- **Static Analysis**: Simulated security pattern detection
- **AI Triage**: Automatic prioritization of vulnerabilities
- **Evidence Generation**: Reproducible evidence for each finding
- **Comprehensive Reports**: Human-readable security audits
- **Extensible**: Easy to add new vulnerability patterns

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Analyze a contract:

```bash
python -m src.main examples/vulnerable_contract.sol
```

Example output:

```text
🔍 Analyzing contract: VulnerableBank
============================================================
📊 Running static analysis...
📝 Generating evidence...
🤖 AI triage in progress...
📄 Generating report...

============================================================
📋 ANALYSIS COMPLETE
============================================================

# Security Audit Report
## Contract: VulnerableBank

### Executive Summary
- Total Issues: 3
- Priority Level: URGENT
- Recommendation: High severity issues require urgent attention
...
```

## Architecture

- `analyzer/`: Static analysis and evidence generation
- `ai/`: Triage and reporting
- `models/`: Data structures
- `utils/`: Validation utilities
- `examples/`: Sample vulnerable contracts

## Skills Demonstrated

- ✅ Security analysis
- ✅ AI integration patterns
- ✅ Evidence-based reporting
- ✅ Structured outputs
- ✅ Clean architecture

## Evidence Model

Each vulnerability includes:

E0: Static evidence (code patterns)

E1: Compiled proof (simulated)

E2: Executed demonstration (simulated)

E3: State change analysis (simulated)

E4: Economic impact (simulated)

E5: Reproducibility (simulated)

## License

MIT
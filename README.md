# NGORI Security Platform

AI-assisted smart contract security analysis platform with evidence-based reporting.

## Features

- **Static Analysis**: Simulated security pattern detection
- **AI Triage**: Automatic prioritization of vulnerabilities
- **Evidence Generation**: Reproducible evidence for each finding
- **Comprehensive Reports**: Human-readable security audits
- **Extensible**: Easy to add new vulnerability patterns

## Current Status

> **Note:** This is a **prototype** demonstrating security analysis patterns. The static analysis uses rule-based pattern matching, and the evidence model (E0–E5) is currently **simulated** to showcase the architecture.

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

## Evidence Model (currently simulated)

| Stage | Description | Status |
|-------|-------------|--------|
| E0 | Static evidence (code patterns) | ✅ Pattern matching |
| E1 | Compiled proof | 🔄 Simulated |
| E2 | Executed demonstration | 🔄 Simulated |
| E3 | State change analysis | 🔄 Simulated |
| E4 | Economic impact | 🔄 Simulated |
| E5 | Reproducibility | 🔄 Simulated |

*The architecture supports full implementation with real tools (Slither, Foundry) in future iterations.*

## Roadmap

- [ ] Integrate real static analysis (Slither)
- [ ] Add real contract compilation (Foundry)
- [ ] Execute actual test cases
- [ ] Generate real economic impact analysis

MIT
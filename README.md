# NGORI Security Platform

NGORI is a smart‑contract security analysis tool that combines static analysis, AI‑assisted triage, and Foundry‑based verification. It produces a structured security report and a JSONL dataset for further analysis.

## How it works

1. **Static analysis** – runs Slither on a Solidity contract and extracts findings.
2. **Normalization** – converts Slither’s output into a consistent internal format.
3. **Deduplication** – merges duplicate findings from different detectors.
4. **AI triage** (optional) – sends each finding to Groq (four keys) for severity and false‑positive assessment.
5. **Verification** – compiles and tests the contract with Foundry; checks for state changes and reproducibility markers.
6. **Reporting** – generates a markdown report and a JSONL dataset.

## Requirements

- Python 3.10+
- Foundry (forge, anvil, cast)
- Slither (install via pip)
- Groq API keys (optional, for AI triage)

## Installation

Clone the repository and set up the Python environment:

```bash
git clone https://github.com/isaac-mwaura/ngori-security-platform.git
cd ngori-security-platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

import os
import json
from groq import Groq
from dotenv import load_dotenv
from src.models.finding import Finding

load_dotenv()

def groq_triage_finding(finding: Finding) -> dict:
    """Send a finding to Groq for triage."""
    api_key = os.getenv("GROQ_API_KEY_1")
    if not api_key:
        return {"error": "GROQ_API_KEY_1 not set in .env file"}

    client = Groq(api_key=api_key)

    prompt = f"""
You are a security expert. Analyze this smart contract vulnerability finding and return a structured JSON.

**Finding:**
- **Detector:** {finding.detector}
- **Severity (from Slither):** {finding.severity}
- **Confidence (from Slither):** {finding.confidence}
- **Contract:** {finding.contract}
- **Function:** {finding.function}
- **Description:** {finding.description}

**Return a JSON object with:**
- `classification`: "vulnerability", "informational", or "false_positive"
- `severity`: "CRITICAL", "HIGH", "MEDIUM", "LOW"
- `confidence`: "HIGH", "MEDIUM", "LOW"
- `reason`: Brief justification
- `false_positive_risk`: "HIGH", "MEDIUM", "LOW"
- `recommended_verification`: A short recommendation for how to verify this finding
"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gemma-7b-it",
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
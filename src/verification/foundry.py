import os
import subprocess
from pathlib import Path

def run_foundry_test(contract_path: str) -> dict:
    project_root = Path(__file__).resolve().parents[2]
    blockchain_dir = project_root / "blockchain"

    result = {
        "build": False,
        "execution": False,
        "state_change": False,
        "impact": False,
        "reproducible": False,
        "stdout": "",
        "stderr": "",
    }

    if not blockchain_dir.exists():
        result["error"] = "blockchain directory not found"
        return result

    try:
        build = subprocess.run(
            ["forge", "build"],
            cwd=blockchain_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        result["build"] = build.returncode == 0
        if not result["build"]:
            result["stderr"] = build.stderr
            return result

        test = subprocess.run(
            ["forge", "test", "--match-contract", "VulnerableBankTest", "-vv"],
            cwd=blockchain_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        result["execution"] = test.returncode == 0
        result["stdout"] = test.stdout
        result["stderr"] = test.stderr

        if result["execution"]:
            output = test.stdout + "\n" + test.stderr
            result["state_change"] = "NGORI_STATE_CHANGE=1" in output
            result["impact"] = "NGORI_IMPACT=1" in output
            result["reproducible"] = "NGORI_REPRODUCIBLE=1" in output

        return result

    except subprocess.TimeoutExpired:
        return {**result, "error": "Foundry test timed out"}
    except Exception as exc:
        return {**result, "error": str(exc)}
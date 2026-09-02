from typing import List
from ..models.contract import Contract, Vulnerability

def run_static_analysis(contract: Contract) -> Contract:
    """
    Run static analysis on a contract.
    
    This simulates finding vulnerabilities in a contract.
    In production, this would integrate with Slither or similar.
    """
    # Simulate analysis - in reality, this would parse the code
    vulnerabilities = []
    
    # Check for common vulnerable patterns (simulated)
    code = contract.code.lower()
    
    if "tx.origin" in code:
        vulnerabilities.append(Vulnerability(
            name="Use of tx.origin",
            severity="HIGH",
            description="Using tx.origin for authorization is vulnerable to phishing attacks",
            line_numbers=[0],
            recommendation="Use msg.sender instead of tx.origin"
        ))
    
    if "block.timestamp" in code and "require" not in code:
        vulnerabilities.append(Vulnerability(
            name="Timestamp Manipulation",
            severity="MEDIUM",
            description="Block timestamp can be manipulated by miners",
            line_numbers=[0],
            recommendation="Use block.number or consider multi-party verification"
        ))
    
    if "selfdestruct" in code:
        vulnerabilities.append(Vulnerability(
            name="Selfdestruct",
            severity="HIGH",
            description="Selfdestruct can be used to kill the contract unexpectedly",
            line_numbers=[0],
            recommendation="Use a multi-sig or timelock for selfdestruct"
        ))
    
    if "call.value" in code:
        vulnerabilities.append(Vulnerability(
            name="Unsafe External Call",
            severity="CRITICAL",
            description="Unchecked external call can lead to reentrancy attacks",
            line_numbers=[0],
            recommendation="Use send() or transfer() instead of call.value"
        ))
    
    if "delegatecall" in code:
        vulnerabilities.append(Vulnerability(
            name="Delegatecall",
            severity="CRITICAL",
            description="Unchecked delegatecall can lead to storage corruption",
            line_numbers=[0],
            recommendation="Check contract address and use a proxy pattern"
        ))
    
    contract.vulnerabilities = vulnerabilities
    return contract
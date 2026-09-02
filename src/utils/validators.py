from typing import List, Tuple

def validate_contract_code(code: str) -> Tuple[bool, List[str]]:
    """
    Validate smart contract code.
    """
    errors = []
    
    if not code or len(code.strip()) == 0:
        errors.append("Contract code is empty")
        return False, errors
    
    if not code.strip().startswith("pragma"):
        errors.append("Missing pragma directive")
    
    if "contract" not in code.lower():
        errors.append("No contract declaration found")
    
    # Check for basic syntax issues
    open_braces = code.count('{')
    close_braces = code.count('}')
    
    if open_braces != close_braces:
        errors.append("Unbalanced braces")
    
    return len(errors) == 0, errors
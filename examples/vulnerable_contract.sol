pragma solidity ^0.8.0;

contract VulnerableBank {
    address public owner;
    mapping(address => uint) public balances;
    
    constructor() {
        owner = msg.sender;
    }
    
    // Vulnerable: Uses tx.origin for authorization
    function withdraw(uint amount) public {
        require(tx.origin == owner, "Not authorized");
        balances[msg.sender] -= amount;
        msg.sender.call.value(amount)();
    }
    
    // Vulnerable: Block timestamp dependency
    function claimReward() public {
        if (block.timestamp % 2 == 0) {
            balances[msg.sender] += 1 ether;
        }
    }
    
    // Vulnerable: Unsafe external call
    function transferTo(address to, uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        to.call.value(amount)("");
    }
}
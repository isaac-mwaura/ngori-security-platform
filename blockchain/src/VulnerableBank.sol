// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VulnerableBank {
    uint256 public totalBalance;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function deposit() external payable {
        totalBalance += msg.value;
    }

    // Withdrawal - update total balance
    function withdraw(uint256 amount) external {
        require(totalBalance >= amount, "insufficient balance");
        totalBalance -= amount;
    }

    // tx.origin vulnerability
    function transferOwnership(address newOwner) external {
        require(tx.origin == owner, "Not owner");
        owner = newOwner;
    }

    // Unprotected selfdestruct
    function kill() external {
        selfdestruct(payable(owner));
    }
}
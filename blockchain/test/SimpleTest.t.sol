 // SPDX-License-Identifier: MIT
 pragma solidity ^0.8.20;

 import "forge-std/Test.sol";
 import "../src/VulnerableBank.sol";

 contract SimpleTest is Test {
     VulnerableBank bank;

     function setUp() public {
         bank = new VulnerableBank();
         vm.deal(address(this), 10 ether);
         bank.deposit{value: 10 ether}();
     }

     function testSimpleDepositWithdraw() public {
         // Before: bank has 10 ether
         uint256 before = address(bank).balance;
         
         // Withdraw 5 ether
         bank.withdraw(5 ether);
         
         // After: bank should have 5 ether
         uint256 afterBalance = address(bank).balance;
         
         // Bank should have 5 ether remaining (10 - 5)
         assertGt(before, afterBalance);
     }
 }

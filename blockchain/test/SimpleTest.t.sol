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
         // Before: bank records 10 ether
         uint256 before = bank.totalBalance();
         
         // Withdraw 5 ether
         bank.withdraw(5 ether);
         
         // After: bank records 5 ether
         uint256 afterBalance = bank.totalBalance();
         
         assertEq(afterBalance, 5 ether);
         assertLt(afterBalance, before);
     }
 }

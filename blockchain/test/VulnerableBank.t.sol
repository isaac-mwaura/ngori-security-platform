 // SPDX-License-Identifier: MIT
 pragma solidity ^0.8.20;

 import "forge-std/Test.sol";
 import "../src/VulnerableBank.sol";

 contract VulnerableBankTest is Test {
     VulnerableBank bank;

     function setUp() public {
         bank = new VulnerableBank();
         vm.deal(address(this), 10 ether);
         bank.deposit{value: 10 ether}();
     }

     function testBasicDepositWithdraw() public {
         uint256 before = bank.totalBalance();
         bank.withdraw(10 ether);
         uint256 afterBalance = bank.totalBalance();
         assertEq(afterBalance, 0 ether);
     }
     
     function testPartialWithdraw() public {
         uint256 before = bank.totalBalance();
         bank.withdraw(5 ether);
         uint256 afterBalance = bank.totalBalance();
         assertEq(afterBalance, 5 ether);
     }
 }

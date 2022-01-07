// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] public funders;

    constructor() public {
        // set the owner to the person who deploys the contract
        owner = msg.sender;
    }

    function fund() public payable {
        // spend minimum of $50
        uint256 minimumUSD = 5 * 10**18;
        require(getConversionRate(msg.value) >= minimumUSD, "Not enough ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        uint256 priceInWei = uint256(answer) * 10**10;
        return priceInWei;
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethAmount * ethPrice) / 10**18;
        return ethAmountInUsd;
    }

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Dude, you're not the person who deployed the contract"
        );
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 funderId = 0; funderId < funders.length; funderId++) {
            address funder = funders[funderId];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}

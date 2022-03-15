// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    // token address -> staker address -> total amount
    mapping(address => mapping(address => uint256)) public stakingBalance;

    // number of tokens that each users staked
    mapping(address => uint256) public uniqueTokensStaked;

    // token address to token price feed address from chainlink
    mapping(address => address) public tokenPriceFeedMapping;

    /// @return The address of the allowed token
    address[] public allowedTokens;
    // list of stakers
    address[] public stakers;

    IERC20 public dappToken;

    constructor(address _dappTokenAddress) {
        // to initialize our dappToken we have to pass
        // the address of deployed ERC20 (DappToken)
        dappToken = IERC20(_dappTokenAddress);
    }

    // function to associate token adresses with price feed addresses
    function setPriceFeedContract(address _token, address _priceFeed)
        public
        onlyOwner
    {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    function getAllowedTokensCount() public view returns (uint256 count) {
        return allowedTokens.length;
    }

    // stake tokens
    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0");
        require(tokenIsAllowed(_token), "Token not allowed!");
        // transfer money to the contract
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        updateUniqueTokensStaked(msg.sender, _token);
        // add the amount to stakingBalance mapping
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;
        // if this is the first time someone staked
        // add him to the list of stakers
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function ustakeTokens(address _token) public {
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Staking balance cannot be 0");
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender] = uniqueTokensStaked[msg.sender] - 1;
    }

    function issueTokens() public onlyOwner {
        for (uint256 stakerId = 0; stakerId < stakers.length; stakerId++) {
            address recipient = stakers[stakerId];
            // send them the token reward based on Total Value Locked
            // we're sending our dapp token
            // First calculate how much the current staker should receive
            uint256 stakerTotalValue = getStakerTotalValue(recipient);
            // to make the computation easier,
            // user receives the number of tokens equal to dollars staked
            dappToken.transfer(recipient, stakerTotalValue);
        }
    }

    function getStakerTotalValue(address _stakerAddress)
        public
        view
        returns (uint256)
    {
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_stakerAddress] > 0, "Nothing staked!");
        for (
            uint256 allowedTokensId = 0;
            allowedTokensId < allowedTokens.length;
            allowedTokensId++
        ) {
            totalValue =
                totalValue +
                getUserSingleTokenValue(
                    _stakerAddress,
                    allowedTokens[allowedTokensId]
                );
        }
        return totalValue;
    }

    function getUserSingleTokenValue(address _staker, address _token)
        public
        view
        returns (uint256)
    {
        if (uniqueTokensStaked[_staker] <= 0) {
            // check again if user has token staked
            // we don't want to use require,
            // because we want to keep going
            return 0;
        }

        (uint256 price, uint256 decimals) = getTokenValue(_token);
        uint256 totalValueInUsd = (stakingBalance[_token][_staker] * price) /
            (10**decimals);
        return totalValueInUsd;
    }

    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    function updateUniqueTokensStaked(address _staker, address _token)
        internal
    {
        if (stakingBalance[_token][_staker] <= 0) {
            uniqueTokensStaked[_staker] = uniqueTokensStaked[_staker] + 1;
        }
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        for (uint256 idx = 0; idx < allowedTokens.length; idx++) {
            if (allowedTokens[idx] == _token) {
                return true;
            }
        }
        return false;
    }
}

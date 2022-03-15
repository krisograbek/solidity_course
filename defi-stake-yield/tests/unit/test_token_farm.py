import pytest
from brownie import network, TokenFarm, exceptions
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAINS,
    get_contract,
    get_account,
    INITIAL_PRICE_FEED_VALUE,
)
from scripts.deploy_contracts import deploy_contracts


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("Only for local testing. Skipping...")

    account = get_account()
    # we need another account that did NOT deploy our contract
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_contracts()

    # Act
    dai_usd_price_feed = get_contract("dai_usd_price_feed")
    set_tx = token_farm.setPriceFeedContract(
        dapp_token, dai_usd_price_feed, {"from": account}
    )
    set_tx.wait(1)

    # Assert
    assert (
        token_farm.tokenPriceFeedMapping(dapp_token.address)
        == dai_usd_price_feed.address
    )
    assert token_farm.tokenPriceFeedMapping(dapp_token) == dai_usd_price_feed

    with pytest.raises(exceptions.VirtualMachineError):
        set_tx = token_farm.setPriceFeedContract(
            dapp_token, dai_usd_price_feed, {"from": non_owner}
        )
        set_tx.wait(1)


def test_stake_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("Only for local testing. Skipping...")

    account = get_account()
    # we need another account that did NOT deploy our contract
    token_farm, dapp_token = deploy_contracts()

    # Act
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})

    # Assert
    # staking balance of the dapp token for the account has been added
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    # the address has the number of unique tokens staked equal to 1
    assert token_farm.uniqueTokensStaked(account.address) == 1
    # the address has been added to the list of stakers
    assert token_farm.stakers(0) == account.address

    return token_farm, dapp_token


def test_issue_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("Only for local testing. Skipping...")

    account = get_account()
    not_owner = get_account(index=2)
    # we need another account that did NOT deploy our contract
    token_farm, dapp_token = test_stake_tokens(amount_staked)

    starting_balance = dapp_token.balanceOf(account.address)

    # Act
    tx = token_farm.issueTokens({"from": account})
    tx.wait(1)

    # Assert
    assert dapp_token.balanceOf(account.address) == (
        starting_balance + INITIAL_PRICE_FEED_VALUE
    )

    # raise exception for other accounts than contract owner
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.issueTokens({"from": not_owner})

from scripts.aave_borrow import get_asset_price, get_lending_pool, approve_erc20
from scripts.helpful_scripts import get_account
from brownie import config, network
from web3 import Web3


def test_get_asset_price():
    # Arrange
    asset_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )

    # assume eth cost range $1k - $10k
    # thus dai to eth 0.0001 - 0.001
    assert asset_price < 0.001
    assert asset_price > 0.0001


def test_get_lending_pool():
    # Arrange & Act
    lending_pool = get_lending_pool()

    assert lending_pool is not None


def test_approve_erc20():
    # Arrange
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    lending_pool = get_lending_pool()
    amount = Web3.toWei(0.01, "ether")
    # Act
    tx = approve_erc20(lending_pool.address, amount, erc20_address, account)
    # Assert
    # Patrick wrote this assert. I don't know why...
    assert tx is not True

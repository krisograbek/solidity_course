from brownie import interface, network, config
from scripts.helpful_scripts import get_account
from web3 import Web3


def get_weth():
    """
    Mints Weth by depositing Eth
    """
    account = get_account()
    # print(account)
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": Web3.toWei(0.1, "ether")})
    tx.wait(1)
    print("Received 0.1 WETH?")


def main():
    get_weth()

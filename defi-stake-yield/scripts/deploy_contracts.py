from brownie import DappToken, TokenFarm, config
from scripts.helpful_scripts import get_account


def deploy_contracts():
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})


def main():
    deploy_contracts()

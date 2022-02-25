from brownie import AdvancedCollectible, accounts
from scripts.helpful_scripts import get_account, fund_with_link
from web3 import Web3


def main():
    account = get_account()
    # get the last deployed advanced collectible
    advanced_collectible = AdvancedCollectible[-1]
    # fund the contract with link to generate a random number
    fund_with_link(advanced_collectible.address)
    # create collectible
    creation_tx = advanced_collectible.createCollectible({"from": account})
    creation_tx.wait(1)
    print("Created Collectible!!!")

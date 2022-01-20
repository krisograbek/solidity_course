from brownie import network, accounts, MockV3Aggregator


# Setting variables for Mock Aggregator
DECIMALS = 8
STARTING_PRICE = 300000000000

LOCAL_BLOCKCHAINS = ["development", "ganache-local"]
FORKED_BLOCKCHAINS = ["mainnet-fork", "mainnet-fork-net"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAINS
        or network.show_active() in FORKED_BLOCKCHAINS
    ):
        return accounts[0]
    else:
        return accounts.load("first-account")


def deploy_mocks():
    print(f"Deploying Mocks... ")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print(f"Mock Deployed!")

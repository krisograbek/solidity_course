from brownie import accounts, network, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork",
]

TEST_NETWORKS_LIST = ["rinkeby"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(accounts[0].balance())
        return accounts[0]
    if network.show_active() in TEST_NETWORKS_LIST:
        print(config["accounts"][network.show_active()]["name"])
        return accounts.load(config["accounts"][network.show_active()]["name"])
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])

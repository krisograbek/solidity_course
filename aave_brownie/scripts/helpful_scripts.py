from brownie import accounts, config, network

LOCAL_ENVS = ["mainnet-fork", "development"]

TEST_NETWORKS_LIST = ["rinkeby", "kovan"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_ENVS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in TEST_NETWORKS_LIST:
        print(config["networks"][network.show_active()]["account"])
        return accounts.load(config["networks"][network.show_active()]["account"])

    return None

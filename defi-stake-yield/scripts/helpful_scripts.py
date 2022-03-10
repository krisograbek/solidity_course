from brownie import Contract, config, network, accounts, MockWETH, MockDAI


LOCAL_BLOCKCHAINS = ["development", "mainnet-fork"]
TEST_NETWORKS = ["rinkeby", "kovan"]


def get_account(index=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAINS:
        return accounts[0]
    if network.show_active() in TEST_NETWORKS:
        return accounts.load(config["networks"][network.show_active()]["account"])
    return None


contract_to_mock = {
    "weth_token": MockWETH,
    "dai_token": MockDAI,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAINS:
        if len(contract_type) <= 0:
            deploy_mocks()

        contract = contract_type[-1]

    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name,
            contract_address,
            contract_type.abi,
        )

    return contract


def deploy_mocks():
    pass

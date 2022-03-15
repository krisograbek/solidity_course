from brownie import (
    Contract,
    config,
    network,
    accounts,
    MockWETH,
    MockDAI,
    MockV3Aggregator,
)
from web3 import Web3


LOCAL_BLOCKCHAINS = ["development", "mainnet-fork"]
TEST_NETWORKS = ["rinkeby", "kovan"]

DECIMALS = 18
INITIAL_PRICE_FEED_VALUE = 2500000000000000000000  # 2500 * 10 ** 18


def get_account(index=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAINS:
        return accounts[0]
    if network.show_active() in TEST_NETWORKS:
        return accounts.load(config["networks"][network.show_active()]["account"])
    return None


contract_to_mock = {
    "dai_usd_price_feed": MockV3Aggregator,
    "weth_token": MockWETH,
    "dai_token": MockDAI,
    "eth_usd_price_feed": MockV3Aggregator,
}


def get_contract(contract_name):
    """
    This function will either:
        - Get an address from the config
        - Or deploy a Mock to use for a network that doesn't have the contract
    Args:
        contract_name (string): This is the name of the contract that we will get
        from the config or deploy
    Returns:
        brownie.network.contract.ProjectContract: This is the most recently deployed
        Contract of the type specified by a dictionary. This could either be a mock
        or a 'real' contract on a live network.
    """
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


def deploy_mocks(decimals=DECIMALS, initial_price_feed=INITIAL_PRICE_FEED_VALUE):
    """
    Deploy mocks for local Blockchains
    """

    account = get_account()
    print(f"The current active network is {network.show_active()}")

    print("Deploying AggregatorV3...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_price_feed, {"from": account}
    )
    print(f"Deployed AggregatorV3 to {mock_price_feed.address} ")

    print("Deploying DAI Token...")
    dai_token = MockDAI.deploy({"from": account})
    print(f"Deployed DAI Token to {dai_token.address} ")
    print("Deploying WETH Token...")
    weth_token = MockWETH.deploy({"from": account})
    print(f"Deployed WETH Token to {weth_token.address} ")

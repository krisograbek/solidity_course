from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpers import get_account, deploy_mocks, LOCAL_BLOCKCHAINS


def deploy_fund_me():
    account = get_account()

    # price feed address
    # if we are on a persistent network like rinkeby, use the associated address
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    # otherwise use mocks
    else:
        print(f"Active network: {network.show_active()}")
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to  {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()

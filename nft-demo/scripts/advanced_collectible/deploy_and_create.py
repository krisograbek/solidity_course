from scripts.helpful_scripts import get_account, RARIBLE_URL
from brownie import AdvancedCollectible, network, config


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )


def main():
    deploy_and_create()

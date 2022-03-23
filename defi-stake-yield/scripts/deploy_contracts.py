from brownie import DappToken, TokenFarm, config, network
from scripts.helpful_scripts import get_account, get_contract
from web3 import Web3
import yaml
import json
import os
import shutil

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_contracts(frontend_update=False):
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # transfer dapp tokens to our token farm
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)

    weth_token = get_contract("weth_token")
    dai_token = get_contract("dai_token")

    # we're using the dict so, that the key is an actual token contract
    # and the value is a price feed contract
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        dai_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)

    # for i in range(token_farm.getAllowedTokensCount()):
    # print(f"Allowed token {i} - {token_farm.allowedTokens(i)}")

    if frontend_update:
        update_front_end()

    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    # loop through allowed tokens
    # key - token
    # value - price feed for the token
    for token in dict_of_allowed_tokens:
        # add the token address to allowed tokens
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)

        # TODO: uncomment
        # map tokens with their price feeds
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token].address, {"from": account}
        )
        set_tx.wait(1)

    return token_farm


def update_front_end():
    copy_folders_to_frontend("./build", "./frontend/src/chain-info")

    with open("brownie-config.yaml", "r") as config_yaml:
        config_dict = yaml.load(config_yaml, Loader=yaml.FullLoader)
        with open("./frontend/src/brownie-config.json", "w") as config_json:
            json.dump(config_dict, config_json)

    print("Frontend updated")


def copy_folders_to_frontend(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main():
    deploy_contracts(frontend_update=True)

import pytest
from brownie import network, AdvancedCollectible
import time
from scripts.helpful_scripts import LOCAL_ENVS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # deploy a new contract
    # create an nft
    # return random breed
    # arrange
    if network.show_active() in LOCAL_ENVS:
        pytest.skip("Only for real blockchains")

    # Act
    advanced_collectible, creating_tx = deploy_and_create()
    time.sleep(60)

    # Assert
    # our token counter should increase
    assert advanced_collectible.tokenCounter() == 1

import pytest
from brownie import network, AdvancedCollectible

from scripts.helpful_scripts import LOCAL_ENVS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    # deploy a new contract
    # create an nft
    # return random breed
    # arrange
    if network.show_active() not in LOCAL_ENVS:
        pytest.skip("Only for local testing")

    # Act
    advanced_collectible, creating_tx = deploy_and_create()
    # that's how we take advantage of events
    request_id = creating_tx.events["requestedCollectible"]["requestId"]
    # callBackWithRandomness(request_id, some_random_number, consumer_contract)
    random_number = 778
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, random_number, advanced_collectible.address, {"from": get_account()}
    )

    # Assert
    # our token counter should increase
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3

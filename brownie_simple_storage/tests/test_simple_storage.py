from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 10  # initial favNumber in SimpleStorage.sol

    # Assert
    assert starting_value == expected


def test_updating():
    # Arrange
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    new_value = 15
    transaction = simple_storage.store(new_value, {"from": account})
    transaction.wait(1)
    updated_value = simple_storage.retrieve()

    # Assert
    assert updated_value == new_value

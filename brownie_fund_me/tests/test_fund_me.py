from brownie import network, accounts, exceptions
import pytest
from scripts.helpers import get_account, LOCAL_BLOCKCHAINS
from scripts.deploy import deploy_fund_me


def test_fund_and_withdraw():
    # Arrange
    account = get_account()
    # Act
    fund_me = deploy_fund_me()
    # adding + 100 is a tip from Patrick
    entrance_fee = fund_me.getEntranceFee()  # + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # Assert
    print(f"Current entry fee {entrance_fee}")
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    # Act
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    # Assert
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip()

    # account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    # the next block the way of telling that we actually
    # want to see this exception
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})

from brownie import network, config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def approve_erc20(spender, amount, erc20_address, account):
    print("Approving erc20...")
    # ABI for ERC20 with the address
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    # return tx


def get_lending_pool():
    # ABI for addresses provider
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    # Address
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    # ABI for lending pool
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def get_borrowable_data(lending_pool, account):

    print("Getting data...")
    # returns 6 numbers
    # see: https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#getuseraccountdata
    data = lending_pool.getUserAccountData(account.address, {"from": account})
    total_collatheral_eth = Web3.fromWei(data[0], "ether")
    total_debt_eth = Web3.fromWei(data[1], "ether")
    available_borrow_eth = Web3.fromWei(data[2], "ether")
    print(
        f"Collatheral: {total_collatheral_eth}, total_debt: {total_debt_eth}, available to borrow: {available_borrow_eth}"
    )


def main():
    account = get_account(id="test1")
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # Address
    # ABI
    lending_pool = get_lending_pool()
    print("Lending pool address:", lending_pool)
    # approving from erc20
    approve_erc20(lending_pool.address, amount, erc20_address, account)

    # depositing
    print("Depositing ...")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")

    get_borrowable_data(lending_pool, account)

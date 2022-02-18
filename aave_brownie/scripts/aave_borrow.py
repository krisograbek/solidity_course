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
    total_collateral_eth = Web3.fromWei(data[0], "ether")
    total_debt_eth = Web3.fromWei(data[1], "ether")
    available_borrow_eth = Web3.fromWei(data[2], "ether")
    print(
        f"Collateral: {total_collateral_eth}, total_debt: {total_debt_eth}, available to borrow: {available_borrow_eth}"
    )

    return (float(available_borrow_eth), float(total_debt_eth))


def get_asset_price(asset_price_feed):
    # ABI
    # address
    dai_eth_price = interface.AggregatorV3Interface(asset_price_feed)
    # returns 5 values, but we're interested
    # only in the latest price which is at the index 1
    latest_price = dai_eth_price.latestRoundData()[1]
    converted_price = Web3.fromWei(latest_price, "ether")
    print(f"DAI/ETH price {converted_price} ")
    return float(converted_price)


def repay_all(amount, lending_pool, account):
    approve_erc20(
        lending_pool.address,
        Web3.toWei(amount, "ether"),
        config["networks"][network.show_active()]["dai_token_address"],
        account,
    )
    print("Approved")
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token_address"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repaid!")


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

    available_to_borrow, total_debt = get_borrowable_data(lending_pool, account)

    # convert to DAI
    dai_eth_price_feed = config["networks"][network.show_active()]["dai_eth_price_feed"]
    dai_eth_price = get_asset_price(dai_eth_price_feed)

    # safety factor is for Health Factor
    # the lower the safety factor the higher Health Factor
    safety_factor = 0.9
    amount_dai_to_borrow = (1 / dai_eth_price) * (available_to_borrow * safety_factor)
    print(f"We are borrowing {amount_dai_to_borrow} DAI.")

    dai_address = config["networks"][network.show_active()]["dai_token_address"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("Borrowed some DAI")
    print("New borrawable data:", get_borrowable_data(lending_pool, account))

    repay_all(amount, lending_pool, account)
    print(
        "We just deposited, borrowed, and repaid on AAVE all programatically! Thank you AAVE, Brownie, and Chainlink!!"
    )

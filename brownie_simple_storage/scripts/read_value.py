from brownie import SimpleStorage, network, accounts


def read_contract():
    # get the latest contract from ./build/deployments
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())


def main():
    read_contract()

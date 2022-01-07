from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    # grab account from list
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    print("Updated:", simple_storage.retrieve())

    # Other methods to get an account
    # print(account)
    # load the account by name
    # account = accounts.load("first-account")
    # get private key from environment variables
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # get account from config.yaml
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.load("first-account")


def main():
    deploy_simple_storage()

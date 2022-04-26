from unittest.mock import Mock
from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

# this imports from other Py scripts - may need "__init__.py" to initialize
from scripts.helpful_scripts import get_account
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    # pass the price feed address (mock) to our fundme contract

    # If we are on a persistent network like Rinkeby, use the associated address
    # otherwise, deploy mocks if in LOCAL_BLOCKCHAIN ENVIRONMENTS list
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]  # this grabs from brownie-config.yaml file
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        # -1 this means we use the most recently deployed from array

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )  # this gets information from brownie-config.yaml
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()

from algosdk.mnemonic import *
from algosdk.future import transaction
from algosdk.atomic_transaction_composer import *
from algosdk.logic import get_application_address
from constants.constants import ROOT_ACCOUNT_MNEMONIC, ALGOD_HOST, ALGOD_TOKEN
from beaker import *
from contracts.compliance_contract import ComplianceContract

ACCOUNT_ADDRESS = to_public_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SECRET = to_private_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SIGNER = AccountTransactionSigner(ACCOUNT_SECRET)

WAIT_DELAY = 11


class ComplianceClient:
    """
    Compliance client interfacing with the ComplianceContract deployed on the algorand blockchain
    """

    def __init__(self, app_id: int = 0):
        self._algo_client = None
        self._algo_app = None
        self._app_id = app_id
        self._app_address = None

        self.build_client(app_id)

    def build_algo_client(self):
        algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_HOST)
        return algod_client

    def get_algo_app_client(self, app_id: int):
        app_client = client.ApplicationClient(
            self._algo_client,
            ComplianceContract(),
            signer=ACCOUNT_SIGNER,
            app_id=self._app_id,
        )
        if app_id == 0:
            # Create  an app client for our app
            app_id, app_addr, _ = app_client.create()
            print(f"Created Compliance app at {app_id} {app_addr}")
            self._app_id = app_id
            app_client.fund(2 * consts.algo)
            print("Funded app")
            app_client.opt_in()
            print("Opted in")
        else:
            app_addr = get_application_address(app_id)
        self._app_address = app_addr
        return app_client

    def build_client(self, app_id: int):
        self._algo_client = self.build_algo_client()
        self._algo_app = self.get_algo_app_client(app_id)
        assert all(
            [
                self._algo_client,
                self._algo_app,
                self._app_id,
                self._app_address,
            ]
        )

    def get_application_state(self):
        app_state = self._algo_app.get_application_state()
        print(f"Current app state:{app_state}")
        return app_state

    def get_application_address(self):
        app_addr = get_application_address(self._app_id)
        print(f"Current app address:{app_addr}")
        return app_addr

    def get_emissions_rule(self):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.get_emission_rule,
            suggested_params=sp,
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def set_emissions_rule(self):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.set_emission_rule,
            emission_parameter="Co2 Emission Level",
            emission_max=100,
            emission_min=0,
            suggested_params=sp,
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def is_business_compliant(self):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.is_business_compliant,
            emission_parameter="Co2 Emission Level",
            emission_value=80,
            suggested_params=sp,
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def mint_compliance_token(self, business_address: str):
        """
        This functions mints the compliance NFT with the business address as the owner of the NFT,
        for being in compliance with the emission control set by the regulator
        """
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 5000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.issue_compliance_nft,
            business_address=business_address,
            suggested_params=sp,
            accounts=[business_address],
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res


if __name__ == "__main__":
    print("Starting deploy of the Compliance App(SC) on Algorand...")
    # appId: 
    c = ComplianceClient()
    c.get_application_state()
    c.get_application_address()
    c.get_emissions_rule()
    print("================ CHANGE =====================")
    c.set_emissions_rule()
    print("================ CHANGE =====================")
    c.get_emissions_rule()
    print("================ CHANGE =====================")
    try:
        c.is_business_compliant()
    except Exception as e:
        print("============ EXCEPTION: ", e)

    try:
        c.mint_compliance_token("SZ3K22H6MZ3A3ORYIVTAYMQMMBWVFOMJWXR3QCODNMJBQRIKBXN5PXX6AI")
    except Exception as e:
        print("========= EXCEPTION IN MINTING...", e)
        import traceback
        traceback.print_exc()

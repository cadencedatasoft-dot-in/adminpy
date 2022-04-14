from httpcore import ConnectError
from solana.blockhash import Blockhash
from solana.keypair import Keypair 
from solana.rpc.types import TxOpts
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.async_client import AsyncToken
from solana.rpc.async_api import AsyncClient
from consts import NETWORK_URL
from stor import Stor


class SplClient:

    def __init__(self) -> None:
        self.apiclient = None
        self.feepayer = None
        self.feepayerkp = None
        self.owner = None
        self.mint_auth = None
        self.fraction_digits = 9
        self.program_id = TOKEN_PROGRAM_ID
        self.freeze_auth = None
        self.skip_confirm = False
        self.inr_token = None
        self.tok = None

    async def init(self, feepayer, feepayerkeypath, freezeauth, owner):
        try:
            self.apiclient = AsyncClient(NETWORK_URL)
            connected = await self.apiclient.is_connected()
            if connected:
                self.set_feepayer(feepayer, feepayerkeypath)
                self.set_freezeauth(freezeauth)
                self.set_owner(owner)
                return True
        except ConnectError as err:
            raise err


    async def close(self):
        await self.apiclient.close()


    async def get_blockhash(self):
        try:
            bh = await self.apiclient.get_recent_blockhash()
            return Blockhash(bh['result']['value']['blockhash'])
        except ConnectError as err:
            raise err
        except BaseException as err:
            raise err


    async def request_funds(self):
        try:
            airdrop = await self.apiclient.request_airdrop(self.feepayer, 336168000)
            await self.apiclient.confirm_transaction(airdrop['result'])
        except ConnectError as err:
            raise err
        except BaseException as err:
            raise err


    async def create_mint_auth(self, keys, mustsigncount):
        if len(keys) < mustsigncount:
            raise Exception("Error: Verify tha arguments passed")
        else:
            try:
                blockhash = await self.get_blockhash()
                options = TxOpts(False, False)
                self.tok = AsyncToken(self.apiclient, self.owner, TOKEN_PROGRAM_ID, self.feepayerkp)
                self.mint_auth = await self.tok.create_multisig(mustsigncount, keys, options, blockhash)
                return self.mint_auth
            except ConnectError as err:
                raise err                
            except BaseException as err:
                raise err


    def get_mint_auth(self):
        return self.mint_auth


    def set_feepayer(self, pubkeyfeepayer, feepayerpath):
        try:
            pubkey, buff = Stor.get_secret(pubkeyfeepayer, feepayerpath)
            kppayer = Keypair.from_secret_key(buff)
            self.feepayer = pubkeyfeepayer   
            self.feepayerkp = kppayer
        except ConnectError as err:
            raise err
        except BaseException as err:
            raise err        


    def set_freezeauth(self, pubkeyfreezeauth):
        try:
            self.freeze_auth = pubkeyfreezeauth   
        except ConnectError as err:
            raise err
        except BaseException as err:
            raise err


    def set_owner(self, pubkeyowner):
        try:
            self.owner = pubkeyowner   
        except ConnectError as err:
            raise err
        except BaseException as err:
            raise err                 


    async def create_inr_token(self):
        try:
            blockhash = await self.get_blockhash()
            self.inr_token = await self.tok.create_mint(self.apiclient,
                                             self.feepayerkp,
                                             self.mint_auth,
                                             self.fraction_digits,
                                             self.program_id,
                                             self.freeze_auth,
                                             self.skip_confirm,
                                             blockhash)

            acc_pubkey = await self.inr_token.create_account(self.inr_token.pubkey)

            return self.inr_token.pubkey, acc_pubkey
        except ConnectError as err:
            raise err
        except BaseException as err:
            raise err

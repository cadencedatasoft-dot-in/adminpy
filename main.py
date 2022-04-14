import asyncio
from consts import BASE_PATH, BACKUP_FOLDER
from stor import Stor
from keygen import KeyPairGenerator
from splclient import SplClient

async def main():
    try:
        kpobj = KeyPairGenerator()
        minsignercount = 2
        namelist = kpobj.get_names(minsignercount)
        
        keypairlist, pubkeylist = kpobj.gen_key_pairs(namelist)
        keys = list(keypairlist.keys())
        pubkeys = list(pubkeylist.values())
        spl = SplClient()
        if await spl.init(pubkeylist.get(keys[0]), keypairlist.get(keys[0]), pubkeylist.get(keys[0]), pubkeylist.get(keys[0])):
            await spl.request_funds()
            mintauth = await spl.create_mint_auth(pubkeys, minsignercount)
            inr_token, accpub = await spl.create_inr_token()
            newbackuppath = Stor.copy_keys(list(keypairlist.values()), BASE_PATH+BACKUP_FOLDER)
            report_file = Stor.gen_spl_report(newbackuppath, keypairlist, mintauth, inr_token, accpub, pubkeylist.get(keys[0]), pubkeylist.get(keys[0]))
            await spl.close()

        print("Successfully generated multisign mint authority and token, the detail are available at ", report_file)
    except BaseException as err:
        print("Operation Failed\n")
        print(f"Details: {err=}, {type(err)=}")

if __name__=="__main__":
    asyncio.run(main())
from solana.keypair import Keypair 
from consts import BASE_PATH, FILE_EXT


class KeyPairGenerator:
    def __init__(self) -> None:
        self.keyList = {}
        self.pubKeys = {}

    def get_names(self, minsigners):
        input_str = input('Enter names here (min: 2, max: 11): ')
        namelist = input_str.split()
        if len(namelist) < minsigners:
            print("Error: Need more names")
            return None
        return namelist

    def gen_key_pairs(self, names):
        try:
            for name in names:
                path = BASE_PATH + name + "." + FILE_EXT
                kp = Keypair().generate()
                pubkey = kp.public_key
                kpfile = open(path, 'w+')
                keyval = "["
                for b in kp.secret_key:
                    keyval += str(b) + ","
                keyval = keyval[:-1]
                keyval += "]"
                kpfile.write(keyval)
                kpfile.close()
                self.keyList[str(pubkey)] = path
                self.pubKeys[str(pubkey)] = pubkey
            return self.keyList, self.pubKeys
        except OSError as err:
            print("Error while performing file operation {0}", format(err))
            return {}

        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}


    def get_keypairs(self):
        return self.keyList

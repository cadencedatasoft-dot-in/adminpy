import os, datetime
import shutil


class Stor:
    def __init__(self) -> None:
        self.report = None

    @staticmethod
    def get_secret(key, path):
        try:
            file = open(path, 'r')
            data = file.read(1024)
            data = data.strip()
            data1 = data[1:-1]
            secret = data1.split(',')
            b = bytearray()
            for s in secret:
                x = bytes(s, encoding='utf8')
                b.append(int(x))

            return key, bytes(b)
        except OSError as err:
            raise err

        except BaseException as err:
            raise err

    @staticmethod
    def copy_keys(sourcefilelist, backuppath):
        try:
            if not os.path.exists(backuppath):
                os.makedirs(backuppath)
            
            newbackuppath = os.path.join(backuppath, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            os.makedirs(newbackuppath)
            for file in sourcefilelist:
                shutil.copy2(file, newbackuppath)

            return newbackuppath
        except OSError as err:
            raise err

        except BaseException as err:
            raise err

    @staticmethod
    def gen_spl_report(backuppath, pubkey_kppaths, mint_auth, inrtoken, accountpubkey, freezeauth, owner):
        try:
            reportfile = backuppath+  os.path.sep + "report.txt"
            file = open(reportfile, 'w')
            file.write("REPORT \r\n \r\n")
            
            for key in list(pubkey_kppaths.keys()):
                file.write(str(key)+" - ")
                file.write(pubkey_kppaths[key] + "\r\n")
            
            file.write("\r\n \r\n")
            file.write("MINT AUTH: "+ str(mint_auth) + "\r\n")
            file.write("MINT TOKEN: "+ str(inrtoken) + "\r\n")
            file.write("MINT ACCOUNT: "+ str(accountpubkey) + "\r\n")
            file.write("FREEZE AUTH: "+ str(freezeauth) + "\r\n")
            file.write("TOKEN OWNER: "+ str(owner) + "\r\n")            
            file.flush()
            file.close()

            return reportfile
        except OSError as err:
            raise err

        except BaseException as err:
            raise err
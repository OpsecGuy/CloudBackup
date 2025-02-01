from helper import *


cfg = Config()


def main():
    output_file = get_output_file()
    gpg = get_gpg()
    
    create_zip_file()
    encrypt_file(output_file, gpg)
    upload_file_to_mega(output_file)
    
    if cfg.data["do_not_save_file_locally"]:
        os.remove(output_file)

def encrypt_file(output_file, gpg):
    with open(".temp.zip", "rb") as f:
        status = gpg.encrypt_file(
        f,
        recipients=cfg.data["recipments"],
        output=output_file
    )
    if status.ok:
        log.info(f"Encryption successfull <{output_file}>")
    else:
        log.warning("Encrypting zip file has failed!")
        log.error(status.stderr)
        os._exit(5)
    os.remove(".temp.zip")

def create_zip_file():
    with zipfile.ZipFile(".temp.zip", "w") as zf:
        for path_pattern in cfg.data["paths"]:
            if any(ch in path_pattern for ch in ["*"]):
                for file in glob.glob(path_pattern):
                    file_path = pathlib.Path(file)
                    zf.write(file_path, arcname=str(file_path))
            else:
                file_path = pathlib.Path(path_pattern)
                zf.write(file_path, arcname=str(file_path))

def upload_file_to_mega(output_file):
    mega = Mega()
    mg = mega.login(cfg.data["mega_login"], cfg.data["mega_password"])
    mg.upload(output_file)
    log.info("File has been uploaded to cloud storage")

def get_output_file():
    return f"{cfg.data['output_file_name']}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.zip.gpg"

def get_gpg():
    key_data = open(cfg.data["encryption_key_file_name"], "r").read()
    if "win" in sys.platform:
        gpg = gnupg.GPG(gpgbinary=pathlib.Path("gpg.exe"), keyring=key_data)
    elif "linux" == sys.platform:
        gpg = gnupg.GPG(gpgbinary=pathlib.Path("/usr/bin/gpg"))
        gpg.import_keys(key_data)
    return gpg

def run_threaded():
    while True:
        cfg = Config()
        main()
        log.info(f"Waiting {cfg.data['backup_repeat_delay']} seconds for the next backup")
        time.sleep(cfg.data['backup_repeat_delay'])


if __name__ == "__main__":
    if cfg.data['backup_repeat_delay'] > 0:
        threading.Thread(target=run_threaded, daemon=False, name="Loop").start()
    else:
        log.warning("Executing only once due to 'backup_repeat_delay' is set to 0 (seconds)")
        main() # Execute only once
import platform
from datetime import datetime
from pathlib import Path

from smb.SMBConnection import SMBConnection
from dateutil.relativedelta import relativedelta

from server_settings import (
    USER_ID, PASSWORD, SERVER_IP, SERVICE_NAME, REMOTE_PATH
)


class BACKUPNAS_AUTO_REMOVER:
    def __init__(self) -> None:
        """Initialization
        """
        self.DATETIME_NOW = datetime.now()
        self.STORAGE_PERIOD = relativedelta(months=6)

    def main(self) -> None:
        """Main script
        """
        deleted_dirname_list = []
        try:
            conn = SMBConnection(
                username=USER_ID, password=PASSWORD,
                my_name=platform.uname().node, remote_name=SERVER_IP
            )
            conn.connect(SERVER_IP, 139)
            for shared_path in conn.listPath(SERVICE_NAME, REMOTE_PATH):
                shared_filename = shared_path.filename
                if shared_path.filename in [".", ".."]:
                    # ./ と ../ はパスする
                    continue

                if shared_path.isDirectory is False:
                    # ディレクトリでないときは，パスする
                    continue

                print(shared_filename)
                if self.do_delete_directory(shared_filename) is True:
                    print(shared_filename)
                    # shared_path.deleteDirectory(
                    #     SERVICE_NAME, shared_path.filename
                    # )
                    deleted_dirname_list.append(shared_filename)

            LOG_BASENAME = (
                f"removed_directories_{self.DATETIME_NOW:%Y%m%d_%H%M%S}.log"
            )
            PROJ_DIRNAME = Path(__file__).resolve().parent
            LOG_DIRNAME = PROJ_DIRNAME / "log"
            LOG_DIRNAME.mkdir(exist_ok=True, parents=True)
            LOG_FILENAME = LOG_DIRNAME / LOG_BASENAME

            with LOG_FILENAME.open(mode="w", encoding="utf-8") as log_f:
                for deleted_dir in deleted_dirname_list:
                    log_f.write(deleted_dir + "\n")

        finally:
            conn.close()

    def do_delete_directory(self, target_dirname: str) -> bool:
        """削除対象のディレクトリか否かを判定する

        Args:
            target_dirname (str): 判定するディレクトリ名

        Returns:
            bool: 判定する場合はTrue，そうでない場合はFalseを返す
        """
        try:
            backuped_datetime = datetime.strptime(
                target_dirname, "%Y%m%d%H%M%S"
            )
        except ValueError:
            # "%Y%m%d%H%M%S"の形式でエラーが発生する場合
            return False

        print(backuped_datetime)
        return backuped_datetime < (self.DATETIME_NOW - self.STORAGE_PERIOD)


if __name__ == "__main__":
    backupnas_auto_remover = BACKUPNAS_AUTO_REMOVER()
    backupnas_auto_remover.main()

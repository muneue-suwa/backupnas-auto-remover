# Backupnas Auto Remover

SMB経由で接続されたバックアップNASについて，指定された期間以前のフォルダを削除する．

## 環境

### クライアント

- OS: Windows 10
- Python: 3.10.2

### サーバ

SMBサーバ．バックアップフォルダは，バックアップ日時を用いて `%Y%m%d%H%M%S` と保存されている．

## 設定ファイル

`server_settings.py` を作成する．例えば，バックアップフォルダ `20200401010100` が `\\192.168.152.131\smb\public\backup\20200401010100` と保存され，ユーザのID
IDとパスワードが `muneue`, `mypassword` の場合は，以下のように設定する．

```python:server_settings_py
USER_ID = "muneue"  # Your Server User ID
PASSWORD = "mypassowrd"  # Your Server Password
SERVER_IP = "192.168.152.131"  # Server IP Address
SERVICE_NAME = "smb"  # The Shared Folder
REMOTE_PATH = "\\public\\backup\\"  # Backup Location Directory
```


## 実行方法

以下のコマンドを実行する．

```powershll:run
python -m venv .env  # 初回のみ
.env/Script/pip -U pip  # 初回のみ
.env/Script/pip install -r requirements.txt  # 初回のみ
.env/Script/python main.py
```

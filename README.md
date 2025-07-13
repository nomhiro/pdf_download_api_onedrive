# OneDrive PDF ダウンロード API

Microsoft Graph APIを使用してOneDriveからPDFファイルをダウンロードするPythonスクリプトです。

## 機能

- Microsoft Graph APIを通じてOneDriveからファイルをダウンロード
- MSALライブラリを使用した認証
- PDFファイルの取得とローカル保存

## 必要な環境

- Python 3.6以上
- Microsoft Azure アプリケーション登録

## インストール

1. 必要なライブラリをインストール：
```bash
pip install -r requirements.txt
```

## 設定

1. `pdf_download_api_onedrive.py`ファイル内の以下の項目を設定してください：
   - `client_id`: Azure ADアプリケーションのクライアントID
   - `tenant_id`: Azure ADテナントID
   - `YOUR_FILE_ID`: ダウンロードしたいファイルのID

## 使用方法

```python
# ファイルをダウンロード
download_file("YOUR_FILE_ID", "application/pdf")
```

## ファイル構成

- `pdf_download_api_onedrive.py`: メインスクリプト
- `requirements.txt`: 必要なPythonライブラリ一覧

## 注意事項

- Azure ADでアプリケーションを事前に登録する必要があります
- 適切なAPIアクセス許可を設定してください
- 初回実行時は認証画面が表示されます
# OneDriveの特定フォルダ内のファイルを指定形式で一括ダウンロードするツール
# 必要: requests, msal
import os
import requests
from urllib.parse import quote
import webbrowser
import time
import msal

# 設定値（必要に応じて書き換えてください）
# 個人用アカウント専用の最小構成に整理
CLIENT_ID = os.environ.get('ONEDRIVE_CLIENT_ID', 'YOUR_CLIENT_ID')
AUTHORITY = 'https://login.microsoftonline.com/common'
SCOPE = ['Files.Read.All']

# OneDriveのルートからのパスでフォルダ指定
FOLDER_PATH = 'Documents'  # 例: 'Documents/target_folder'
DOWNLOAD_FORMAT = 'pdf'  # 例: 'pdf', 'jpg', 'html' など
DOWNLOAD_DIR = './downloads-from-onedrive'  # ダウンロード先ディレクトリ

# USER_IDを指定（メールアドレスやオブジェクトIDをセットしてください）
USER_ID = os.environ.get('ONEDRIVE_USER_ID', 'YOUR_USER_ID')


def list_files_in_user_drive_folder(user_id, folder_path=None):
    if folder_path:
        url = f'https://graph.microsoft.com/v1.0/users/{user_id}/drive/root:/{quote(folder_path)}:/children'
    else:
        url = f'https://graph.microsoft.com/v1.0/users/{user_id}/drive/root/children'
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get('value', [])


# ファイルを指定形式でダウンロード


def download_file(item, folder_path, file_format, download_dir):
    file_name = item['name']
    item_id = item['id']
    url = f'https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/content?format={file_format}'
    resp = requests.get(url, headers=headers, allow_redirects=False)
    if resp.status_code == 302:
        download_url = resp.headers['Location']
        file_ext = file_format if not file_name.lower().endswith(
            f'.{file_format}') else file_name.split('.')[-1]
        save_name = f"{os.path.splitext(file_name)[0]}.{file_ext}"
        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, save_name)
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {save_name}")
    else:
        print(
            f"Failed to get download URL for {file_name}: {resp.status_code}")


# 認可コードフロー用設定
REDIRECT_URI = 'http://localhost:8080/'  # Azureアプリ登録でリダイレクトURIに追加しておく

# 認可コードフローでアクセストークン取得


def get_token_interactive():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    try:
        flow = app.initiate_device_flow(scopes=SCOPE)
    except Exception as e:
        print(f"Device flow initiation error: {e}")
        print("\n【ヒント】アプリ登録の「サポートされているアカウントの種類」を「個人用 Microsoft アカウントを含む」にしてください。\n")
        raise
    if 'user_code' not in flow:
        print(f"Device flow initiation failed: {flow}")
        raise Exception('Device flow initiation failed')
    print(f"\n{flow['message']}\n")
    try:
        webbrowser.open(flow['verification_uri'])
    except Exception:
        pass
    result = app.acquire_token_by_device_flow(flow)
    if 'access_token' not in result:
        raise Exception(f"認証失敗: {result}")
    return result['access_token']


def main():
    global headers
    access_token = get_token_interactive()
    headers = {'Authorization': f'Bearer {access_token}'}
    # ルート直下の一覧を取得
    files = list_files_in_user_drive_folder('me', FOLDER_PATH)
    print(f"OneDrive '{FOLDER_PATH}' 内のファイル一覧:")
    for item in files:
        if 'file' in item:
            download_file(item, FOLDER_PATH, DOWNLOAD_FORMAT, DOWNLOAD_DIR)
        elif 'folder' in item:
            print(f"[Folder] {item['name']}")


if __name__ == '__main__':
    # USER_IDをセットしたらmain()を有効化してください
    main()

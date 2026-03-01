# subject_4-2-2_1-3

# Google Meet Link Generator (Python)

Google Calendar API を利用して、  
Google Meet付きのイベントを自動生成し、  
Meet参加リンクを出力するPythonスクリプトです。

---

## 📌 概要

本プロジェクトは、Google Calendar APIを使用し、
Google Meetリンク付きのイベントを自動作成するスクリプトです。

Meet単体APIではリンク生成ができないため、
Calendar APIの `conferenceData` を利用して
Meetリンクを発行しています。

---

## 🚀 実装機能

- OAuth認証（初回のみブラウザ認証）
- Google Calendarイベント自動作成
- Google Meetリンク自動生成
- Meet参加URLをターミナルへ出力
- token.jsonによる認証情報の保存

---

## 🛠 使用技術

- Python 3.x
- Google Calendar API
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2

---

## 🔑 セットアップ方法

### 1. 必要ライブラリのインストール

`bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`


### 2. Google Cloud設定

1. Google Cloudで新規プロジェクト作成
2. Google Calendar APIを有効化
3. OAuth同意画面を設定
4. OAuthクライアントID（デスクトップアプリ）を作成
5. credentials.json をダウンロードし、本プロジェクト直下に配置

### 3. 実行

`bash
python create_meet.py`

初回実行時はブラウザでGoogle認証が求められます。

認証完了後、ターミナルに以下のように表示されます.

`https://meet.google.com/xxx-xxxx-xxx`

---

## 📖 処理の流れ

1. OAuth認証
2. Google Calendar APIへ接続
3. 5分後開始・1時間後終了のイベント作成
4. conferenceDataでMeetリンク生成
5. hangoutLinkを取得して出力

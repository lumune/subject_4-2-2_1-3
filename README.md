# subject_4-2-2_1-3

提出用課題

4-2-2 API連携実践課題

1-3. Google ミート



# Google ミート 課題1-3

## 📌 概要

Google Calendar APIを使用し、
Google Meetリンク付きのイベントを自動作成するスクリプトです。

Meet単体APIではリンク生成ができないため、
Calendar APIの `conferenceData` を利用して
Meetリンクを発行しています。

本課題では要件を満たす基本版に加え、
実用性を高めたCLI版も実装しました。

---

## 🚀 実装機能

### 🔹 基本機能（課題要件）

- OAuth認証（初回のみブラウザ認証）
- Google Calendarイベント自動作成
- Google Meetリンク自動生成
- Meet参加URLをターミナルへ出力
- token.jsonによる認証情報の保存

### 🔹 発展機能（CLI版）

- ターミナルからミーティング名を入力可能
- 開始日時・終了日時を自由に指定可能
- 実用的なMeetリンク発行ツールとして利用可能

---

## 🛠 使用技術

- Python 3.x
- Google Calendar API
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2

---

## 📁 プロジェクト構成

```
project/
├── create_meet_event.py   # 固定時間版（課題要件）
├── create_meet_cli.py     # CLI入力版（発展実装）
├── credentials.json       # 認証情報（非公開）
├── token.json             # 認証トークン（自動生成・非公開）
```

※ credentials.json / token.json は GitHub に公開しないでください。

---

## 🔑 セットアップ方法

### 1. 必要ライブラリのインストール

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

### 2. Google Cloud設定

1. Google Cloudで新規プロジェクト作成
2. Google Calendar APIを有効化
3. OAuth同意画面を設定
4. OAuthクライアントID（デスクトップアプリ）を作成
5. credentials.json をダウンロードし、本プロジェクト直下に配置

---

## ▶ 実行方法

### 🔹 基本版（固定時間）

```bash
python create_meet_event.py
```

5分後開始・1時間後終了のイベントが作成され、
Meetリンクが出力されます。

---

### 🔹 CLI版（発展機能）

```bash
python create_meet_cli.py
```

実行後、以下を入力します：

- ミーティング名
- 開始日時（例: 2026-03-05 14:00）
- 終了日時（例: 2026-03-05 15:00）

入力内容に基づいたMeet付きイベントが作成されます。

---

## 📖 処理の流れ（基本版）

1. OAuth認証
2. Google Calendar APIへ接続
3. イベント作成（conferenceData指定）
4. Meetリンク生成
5. hangoutLink取得・出力

---

## 💡 設計意図

まずは課題要件を満たす最小構成を実装し、
その後、実用性を高めるためにCLI版へ拡張しました。

API連携では

「まず動かす → その後拡張する」

という開発プロセスを意識しています。

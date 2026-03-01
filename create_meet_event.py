#!/usr/bin/env python3
"""
Google Calendar API を使用して Google Meet 付きイベントを作成し、
Meet リンクをターミナルに出力するスクリプト
"""

import os
import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# スコープ: カレンダーの読み書き
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# このスクリプトと同じディレクトリを基準にする
SCRIPT_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"
TOKEN_FILE = SCRIPT_DIR / "token.json"


def get_credentials():
    """OAuth 認証を行い、Credentials を返す。初回はブラウザ認証が走る。"""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"credentials.json が見つかりません: {CREDENTIALS_FILE}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def create_meet_event(service):
    """
    「テストミーティング」の Google Meet 付きイベントを作成し、
    作成されたイベント（hangoutLink 含む）を返す。
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now + datetime.timedelta(minutes=5)
    end_time = now + datetime.timedelta(hours=1)

    event_body = {
        "summary": "テストミーティング",
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Tokyo",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Tokyo",
        },
        "conferenceData": {
            "createRequest": {
                "requestId": f"meet-{start_time.timestamp():.0f}",
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        },
    }

    # conferenceData を反映させるため conferenceDataVersion=1 を指定
    created = (
        service.events()
        .insert(
            calendarId="primary",
            body=event_body,
            conferenceDataVersion=1,
        )
        .execute()
    )

    return created


def main():
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    event = create_meet_event(service)
    hangout_link = event.get("conferenceData", {}).get("entryPoints", [{}])
    meet_link = None
    for ep in hangout_link:
        if ep.get("entryPointType") == "video":
            meet_link = ep.get("uri")
            break

    if meet_link:
        print(meet_link)
    else:
        # フォールバック: レスポンスに hangoutLink が含まれる場合（API によってはこちら）
        meet_link = event.get("hangoutLink")
        if meet_link:
            print(meet_link)
        else:
            print("Meet リンクを取得できませんでした。レスポンス:", event)


if __name__ == "__main__":
    main()

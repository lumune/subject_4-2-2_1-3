#!/usr/bin/env python3
"""
Google Calendar API を使用して、
ターミナル入力から Google Meet 付きイベントを作成するスクリプト
"""

import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

SCRIPT_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"
TOKEN_FILE = SCRIPT_DIR / "token.json"


def get_credentials():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def get_user_input():
    summary = input("ミーティング名を入力してください: ")

    start_str = input("開始日時を入力してください（例: 2026-03-05 14:00）: ")
    end_str = input("終了日時を入力してください（例: 2026-03-05 15:00）: ")

    try:
        start_time = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(end_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("日時の形式が正しくありません。例: 2026-03-05 14:00")
        exit(1)

    # JSTタイムゾーン付与
    tz = datetime.timezone(datetime.timedelta(hours=9))
    start_time = start_time.replace(tzinfo=tz)
    end_time = end_time.replace(tzinfo=tz)

    return summary, start_time, end_time


def create_meet_event(service, summary, start_time, end_time):
    event_body = {
        "summary": summary,
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

    summary, start_time, end_time = get_user_input()

    event = create_meet_event(service, summary, start_time, end_time)

    meet_link = event.get("hangoutLink")

    if meet_link:
        print("\n✅ Meetリンク:")
        print(meet_link)
    else:
        print("Meetリンクを取得できませんでした。")
        print(event)


if __name__ == "__main__":
    main()

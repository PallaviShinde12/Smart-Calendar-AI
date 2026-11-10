
import os
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly"]


def connect_calendar():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def get_today_events(service):
    today = datetime.date.today()

    start = datetime.datetime.combine(
        today, datetime.time.min
    ).astimezone()

    end = datetime.datetime.combine(
        today + datetime.timedelta(days=1),
        datetime.time.min
    ).astimezone()

    result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        maxResults=250,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return result.get("items", [])


def get_timed_events(events):
    timed_events = []

    for event in events:
        start_data = event.get("start", {})
        end_data = event.get("end", {})

        # Skip all-day events in time-based calculations
        if "dateTime" not in start_data or "dateTime" not in end_data:
            continue

        start = datetime.datetime.fromisoformat(
            start_data["dateTime"].replace("Z", "+00:00")
        ).astimezone()

        end = datetime.datetime.fromisoformat(
            end_data["dateTime"].replace("Z", "+00:00")
        ).astimezone()

        if start < end:
            timed_events.append({
                "title": event.get("summary", "Untitled Event"),
                "start": start,
                "end": end
            })

    timed_events.sort(key=lambda item: item["start"])
    return timed_events


def detect_conflicts(events):
    timed_events = get_timed_events(events)

    print("\n===== SCHEDULING CONFLICTS =====")
    found_conflict = False

    for i in range(len(timed_events)):
        first = timed_events[i]

        for j in range(i + 1, len(timed_events)):
            second = timed_events[j]

            if second["start"] >= first["end"]:
                break

            overlap_start = max(first["start"], second["start"])
            overlap_end = min(first["end"], second["end"])

            if overlap_start < overlap_end:
                found_conflict = True

                print(
                    f"Conflict: {first['title']} and "
                    f"{second['title']}"
                )
                print(
                    f"Overlapping time: "
                    f"{overlap_start.strftime('%I:%M %p')} - "
                    f"{overlap_end.strftime('%I:%M %p')}"
                )

    if not found_conflict:
        print("No scheduling conflicts found.")


def detect_free_time(events):
    today = datetime.date.today()

    day_start = datetime.datetime.combine(
        today, datetime.time(9, 0)
    ).astimezone()

    day_end = datetime.datetime.combine(
        today, datetime.time(18, 0)
    ).astimezone()

    busy_slots = []

    for event in get_timed_events(events):
        event_start = max(event["start"], day_start)
        event_end = min(event["end"], day_end)

        if event_start < event_end:
            busy_slots.append((event_start, event_end))

    busy_slots.sort(key=lambda slot: slot[0])

    # Merge overlapping or back-to-back busy slots
    merged = []

    for start, end in busy_slots:
        if merged and start <= merged[-1][1]:
            merged[-1] = (
                merged[-1][0],
                max(merged[-1][1], end)
            )
        else:
            merged.append((start, end))

    free_slots = []
    current = day_start

    for start, end in merged:
        if current < start:
            free_slots.append((current, start))

        current = max(current, end)

    if current < day_end:
        free_slots.append((current, day_end))

    return free_slots


def main():
    service = connect_calendar()
    events = get_today_events(service)

    print("\n========== SMART CALENDAR AI ==========")

    detect_conflicts(events)

    print("\n===== TODAY'S EVENTS =====")

    if not events:
        print("No events scheduled for today.")
    else:
        for event in events:
            title = event.get("summary", "Untitled Event")
            start = event.get("start", {})

            event_time = start.get(
                "dateTime", start.get("date", "Unknown time")
            )

            print(f"{title} | {event_time}")

    print("\n===== FREE TIME SLOTS (9 AM - 6 PM) =====")

    free_slots = detect_free_time(events)
    displayed_slots = [
        (start, end)
        for start, end in free_slots
        if (end - start).total_seconds() >= 15 * 60
    ]

    if not displayed_slots:
        print("No free slots of at least 15 minutes.")
    else:
        for start, end in displayed_slots:
            print(
                f"{start.strftime('%I:%M %p')} - "
                f"{end.strftime('%I:%M %p')}"
            )

    print("\nCalendar connected successfully!")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("\nSomething went wrong:")
        print(f"{type(error).__name__}: {error}")

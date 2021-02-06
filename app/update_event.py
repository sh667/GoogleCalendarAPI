from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def update_event(start,end,a):
    # update the event to tomorrow 9 AM IST
    service = get_calendar_service()
    start = "2020-12-20T13:00:00"
    end = "2020-12-20T15:30:00"
    a = 'Upadted Automating calendar'
    event_result = service.events().update(
        calendarId='primary',
        eventId='hci8fcor79e2vnul1qeb6e0no4',
        body={
            "summary": a,
            "start": {"dateTime": start, "timeZone": 'America/New_York'},
            "end": {"dateTime": end, "timeZone": 'America/New_York'},
        },
    ).execute()

    print("updated event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

if __name__ == '__main__':
    main('2020-12-20T13:00:00','2020-12-20T15:30:00','Updated Automating calendar')
import googleapiclient

from cal_setup import get_calendar_service


def main(value):
    # Delete the event
    print(value)
    service = get_calendar_service()
    try:
        service.events().delete(
            calendarId='primary',
            eventId=value,
        ).execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

    print("Event deleted")


if __name__ == '__main__':
    main('iti3h1ifpk96k8tuta6pjtp88c')

import ics

from nanapi.database.calendar.guild_event_select import GuildEventSelectResult
from nanapi.database.calendar.user_calendar_select import UserCalendarSelectResult
from nanapi.utils.clients import get_session


async def ics_from_events(
    events: list[GuildEventSelectResult],
    user_calendar: UserCalendarSelectResult | None = None,
) -> ics.Calendar:
    calendar = ics.Calendar(events=(to_ics_event(e) for e in events))
    if user_calendar:
        ics_url = user_calendar.ics.replace('webcal://', 'https://')
        async with get_session().get(ics_url) as resp:
            resp.raise_for_status()
            ics_str = await resp.text()
        user_cal = ics.Calendar(ics_str)
        calendar.events.update(user_cal.events)
    return calendar


def to_ics_event(event: GuildEventSelectResult) -> ics.Event:
    ics_event = ics.Event(name=event.name, begin=event.start_time, end=event.end_time)
    if event.description:
        ics_event.description = event.description
    if event.location:
        ics_event.location = event.location
    if event.url:
        ics_event.url = event.url
    ics_event.organizer = ics.Organizer(
        common_name=event.organizer.discord_username,
        email=event.organizer.discord_username,
    )
    for participant in event.participants:
        ics_event.add_attendee(
            ics.Attendee(
                common_name=participant.discord_username,
                email=participant.discord_username,
            )
        )
    return ics_event

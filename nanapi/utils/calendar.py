import ics

from nanapi.database.calendar.guild_event_select_participant import (
    GuildEventSelectParticipantResult,
)


def ics_from_events(events: list[GuildEventSelectParticipantResult]) -> ics.Calendar:
    return ics.Calendar(events=(to_ics_event(e) for e in events))


def to_ics_event(event: GuildEventSelectParticipantResult) -> ics.Event:
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

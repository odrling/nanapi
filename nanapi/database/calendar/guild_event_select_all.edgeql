select calendar::GuildEvent {
  *,
  organizer: { * },
  participants: { * },
}
filter .client = global client

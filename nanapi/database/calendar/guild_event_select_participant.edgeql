with
  discord_id := <int64>$discord_id,
select calendar::GuildEvent {
  *,
  organizer: { * },
  participants: { * },
}
filter .client = global client
and .participants.discord_id = discord_id

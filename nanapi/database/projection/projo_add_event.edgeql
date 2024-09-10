with
  id := <uuid>$id,
  event_discord_id := <int64>$event_discord_id,
  event := (
    select calendar::GuildEvent
    filter .client = global client and .discord_id = event_discord_id
  ),
update projection::Projection
filter .id = id
set {
  guild_events += assert_exists(event)
}

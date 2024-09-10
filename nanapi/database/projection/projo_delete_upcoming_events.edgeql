with
  id := <uuid>$id,
update projection::Projection
filter .id = id
set {
  guild_events -= (select .guild_events filter .start_time > datetime_of_transaction())
}

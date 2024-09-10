with
  id := <uuid>$id,
  participant_id := <int64>$participant_id,
update projection::Projection
filter .id = id
set {
  participants -= (select user::User filter .discord_id = participant_id),
};

with
  discord_ids := <array<int64>>$discord_ids,
  _discord_ids := array_unpack(discord_ids),
select user::Profile {
  full_name,
  photo,
  promotion,
  telephone,
  user: {
    discord_id,
    discord_id_str,
  },
}
filter .user.discord_id in _discord_ids
order by .full_name

with
  pattern := <str>$pattern
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
filter .full_name ilike pattern or .promotion ilike pattern or .telephone ilike pattern

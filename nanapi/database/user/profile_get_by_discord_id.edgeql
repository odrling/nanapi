with
  discord_id := <int64>$discord_id,
  profiles := (
    select user::Profile
    filter .user.discord_id = discord_id
  )
select profiles {
  full_name,
  photo,
  promotion,
  telephone,
  user: {
    discord_id,
    discord_id_str,
  },
}

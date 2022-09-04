with
  discord_id := <int64>$discord_id,
  player := (
    select waicolle::Player
    filter .client = global client and .user.discord_id = discord_id
  ),
select player {
  game_mode,
  moecoins,
  blood_shards,
  user: {
    discord_id,
    discord_id_str,
  },
}

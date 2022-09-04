with
  id := <uuid>$id,
select waicolle::Trade {
  id,
  player_a: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
  waifus_a,
  moecoins_a,
  blood_shards_a,
  player_b: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
  waifus_b,
  moecoins_b,
  blood_shards_b,
}
filter .id = id

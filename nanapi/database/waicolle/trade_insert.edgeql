with
  player_a_discord_id := <int64>$player_a_discord_id,
  waifus_a_ids := <array<uuid>>$waifus_a_ids,
  moecoins_a := <optional int32>$moecoins_a ?? 0,
  blood_shards_a := <optional int32>$blood_shards_a ?? 0,
  player_b_discord_id := <int64>$player_b_discord_id,
  waifus_b_ids := <array<uuid>>$waifus_b_ids,
  moecoins_b := <optional int32>$moecoins_b ?? 0,
  blood_shards_b := <optional int32>$blood_shards_b ?? 0,
  player_a := (select waicolle::Player filter .client = global client and .user.discord_id = player_a_discord_id),
  player_b := (select waicolle::Player filter .client = global client and .user.discord_id = player_b_discord_id),
  inserted := (
    insert waicolle::Trade {
      client := global client,
      player_a := player_a,
      waifus_a := (select waicolle::Waifu filter .id in array_unpack(waifus_a_ids)),
      moecoins_a := moecoins_a,
      blood_shards_a := blood_shards_a,
      player_b := player_b,
      waifus_b := (select waicolle::Waifu filter .id in array_unpack(waifus_b_ids)),
      moecoins_b := moecoins_b,
      blood_shards_b := blood_shards_b,
    }
  )
select inserted {
  id,
  player_a: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
  waifus_a: {
    id,
    timestamp,
    level,
    locked,
    trade_locked,
    blooded,
    nanaed,
    custom_image,
    custom_name,
    custom_collage,
    custom_position,
    character: { id_al },
    owner: {
      user: {
        discord_id,
        discord_id_str,
      },
    },
    original_owner: {
      user: {
        discord_id,
        discord_id_str,
      },
    },
    custom_position_waifu: { id },
  },
  moecoins_a,
  blood_shards_a,
  player_b: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
  waifus_b: {
    id,
    timestamp,
    level,
    locked,
    trade_locked,
    blooded,
    nanaed,
    custom_image,
    custom_name,
    custom_collage,
    custom_position,
    character: { id_al },
    owner: {
      user: {
        discord_id,
        discord_id_str,
      },
    },
    original_owner: {
      user: {
        discord_id,
        discord_id_str,
      },
    },
    custom_position_waifu: { id },
  },
  moecoins_b,
  blood_shards_b,
}

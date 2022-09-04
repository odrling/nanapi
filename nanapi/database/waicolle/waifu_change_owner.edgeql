with
  discord_id := <int64>$discord_id,
  ids := <array<uuid>>$ids,
  player := (select waicolle::Player filter .client = global client and .user.discord_id = discord_id),
  updated := (
    update waicolle::Waifu
    filter .id in array_unpack(ids)
    set {
      timestamp := datetime_current(),
      locked := false,
      custom_collage := false,
      custom_position := waicolle::CollagePosition.DEFAULT,
      owner := player,
      custom_position_waifu := {},
    }
  )
select updated {
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
}

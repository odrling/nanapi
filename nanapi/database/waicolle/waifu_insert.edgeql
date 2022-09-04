with
  discord_id := <int64>$discord_id,
  charas_ids := <array<int32>>$charas_ids,
  player := (select waicolle::Player filter .client = global client and .user.discord_id = discord_id),
for id_al in array_unpack(charas_ids) union (
  with
    chara := (select anilist::Character filter .id_al = id_al),
    inserted := (
      insert waicolle::Waifu {
        client := global client,
        character := chara,
        owner := player,
        original_owner := player,
      }
    ),
  select inserted {
    id,
    timestamp,
    level,
    trade_locked,
    locked,
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
)

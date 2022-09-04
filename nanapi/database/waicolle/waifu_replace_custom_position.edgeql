with
  id := <uuid>$id,
  custom_position := <optional waicolle::CollagePosition>$custom_position,
  custom_position_waifu_id := <optional uuid>$other_waifu_id,
  custom_position_waifu := (
    (select waicolle::Waifu filter .id = custom_position_waifu_id)
    if exists custom_position_waifu_id
    else <waicolle::Waifu>{}
  ),
update waicolle::Waifu
filter .id = id
set {
  custom_position := custom_position ?? waicolle::CollagePosition.DEFAULT,
  custom_position_waifu := custom_position_waifu,
}

with
  ids := <array<uuid>>$ids,
delete waicolle::Waifu
filter .id in array_unpack(ids)

with
  id := <uuid>$id,
  id_al := <int32>$id_al,
  media := (select anilist::Media filter .id_al = id_al),
update waicolle::Collection
filter .id = id
set {
  items -= media,
}

with
  id := <uuid>$id,
  id_al := <int32>$id_al,
  staff := (select anilist::Staff filter .id_al = id_al),
update waicolle::Collection
filter .id = id
set {
  items -= staff,
}

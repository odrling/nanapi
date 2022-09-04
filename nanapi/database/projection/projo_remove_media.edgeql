with
  id := <uuid>$id,
  id_al := <int32>$id_al,
update projection::Projection
filter .id = id
set {
  medias -= (select .medias filter .id_al = id_al),
}

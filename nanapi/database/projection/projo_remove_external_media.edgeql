with
  id := <uuid>$id,
  external_media_id := <uuid>$external_media_id,
update projection::Projection
filter .id = id
set {
  external_medias -= (select .external_medias filter .id = external_media_id),
}

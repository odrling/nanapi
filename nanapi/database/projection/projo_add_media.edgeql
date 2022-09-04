with
  id := <uuid>$id,
  id_al := <int32>$id_al,
  _media := ( select anilist::Media filter .id_al = id_al )
update projection::Projection
filter .id = id
set { medias += _media }

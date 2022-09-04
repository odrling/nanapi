with
  id := <uuid>$id,
  id_al := <int32>$id_al,
  media := (select anilist::Media filter .id_al = id_al),
  _update := (
    update waicolle::Collection
    filter .id = id
    set {
      items += media,
    }
  ),
select {
  collection := assert_exists(_update) {
    id,
    name,
  },
  media := assert_exists(media) {
    id_al,
    type,
    title_user_preferred,
  },
}

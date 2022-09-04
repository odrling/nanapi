with
  id := <uuid>$id,
  id_al := <int32>$id_al,
  staff := (select anilist::Staff filter .id_al = id_al),
  _update := (
    update waicolle::Collection
    filter .id = id
    set {
      items += staff,
    }
  ),
select {
  collection := assert_exists(_update) {
    id,
    name,
  },
  staff := assert_exists(staff) {
    id_al,
    name_user_preferred,
    name_native,
  },
}

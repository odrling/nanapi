select anilist::Character {
  id_al,
  name_user_preferred,
  name_alternative,
  name_alternative_spoiler,
  name_native
}
order by .favourites desc

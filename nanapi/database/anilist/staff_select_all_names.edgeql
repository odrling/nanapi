select anilist::Staff {
  id_al,
  name_user_preferred,
  name_alternative,
  name_native,
}
order by .favourites desc

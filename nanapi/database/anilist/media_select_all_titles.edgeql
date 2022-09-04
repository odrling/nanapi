select anilist::Media {
  id_al,
  type,
  title_user_preferred,
  title_native,
  title_english,
  synonyms,
}
order by .favourites desc

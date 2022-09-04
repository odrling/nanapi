select anilist::Media {
  id_al,
}
filter .is_adult
order by .favourites desc
limit 1000

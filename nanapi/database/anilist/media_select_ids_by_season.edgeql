with
  season := <anilist::MediaSeason>$season,
  season_year := <int32>$season_year,
select anilist::Media {
  id_al,
}
filter .season = season and .season_year = season_year

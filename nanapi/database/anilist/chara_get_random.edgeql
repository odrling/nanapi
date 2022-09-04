select anilist::Character {
  id_al,
  favourites,
  site_url,
  name_user_preferred,
  name_alternative,
  name_alternative_spoiler,
  name_native,
  description,
  image_large,
  gender,
  age,
  date_of_birth_year,
  date_of_birth_month,
  date_of_birth_day,
  rank,
  fuzzy_gender,
}
order by random()
limit 1

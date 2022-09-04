with
  ids_al := <array<int32>>$ids_al
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
} filter .id_al in array_unpack(ids_al)

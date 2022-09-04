with
  ids_al := <array<int32>>$ids_al
select anilist::Staff {
  id_al,
  favourites,
  site_url,
  name_user_preferred,
  name_native,
  name_alternative,
  description,
  image_large,
  gender,
  age,
  date_of_birth_year,
  date_of_birth_month,
  date_of_birth_day,
  date_of_death_year,
  date_of_death_month,
  date_of_death_day,
} filter .id_al in array_unpack(ids_al)

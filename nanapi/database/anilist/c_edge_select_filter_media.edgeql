with
  id_al := <int32>$id_al,
select anilist::CharacterEdge {
  character_role,
  character: {
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
  },
  voice_actors: {
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
  } order by .favourites desc
}
filter .media.id_al = id_al
order by .media.popularity desc

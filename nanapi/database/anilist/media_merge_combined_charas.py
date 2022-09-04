from typing import Any

import orjson
from edgedb import AsyncIOExecutor

EDGEQL_QUERY = r"""
with
  media := <json>$media,
  characters := <json>$characters,
  _media := (
    with
      type := <anilist::MediaType>json_get(media, 'type'),
      id_al := <int32>json_get(media, 'id_al'),
      id_mal := <int32>json_get(media, 'id_mal'),
      title_user_preferred := <str>json_get(media, 'title_user_preferred'),
      title_english := <str>json_get(media, 'title_english'),
      title_native := <str>json_get(media, 'title_native'),
      synonyms := <array<str>>json_get(media, 'synonyms'),
      description := <str>json_get(media, 'description'),
      status := <anilist::MediaStatus>json_get(media, 'status'),
      season := <anilist::MediaSeason>json_get(media, 'season'),
      season_year := <int32>json_get(media, 'season_year'),
      episodes := <int32>json_get(media, 'episodes'),
      duration := <int32>json_get(media, 'duration'),
      chapters := <int32>json_get(media, 'chapters'),
      cover_image_extra_large := <str>json_get(media, 'cover_image_extra_large'),
      cover_image_color := <str>json_get(media, 'cover_image_color'),
      popularity := <int32>json_get(media, 'popularity'),
      favourites := <int32>json_get(media, 'favourites'),
      site_url := <str>json_get(media, 'site_url'),
      is_adult := <bool>json_get(media, 'is_adult'),
      genres := <array<str>>json_get(media, 'genres'),
      tags := <json>json_get(media, 'tags'),
    insert anilist::Media {
      type := type,
      id_al := id_al,
      id_mal := id_mal,
      title_user_preferred := title_user_preferred,
      title_english := title_english,
      title_native := title_native,
      synonyms := synonyms,
      description := description,
      status := status,
      season := season,
      season_year := season_year,
      episodes := episodes,
      duration := duration,
      chapters := chapters,
      cover_image_extra_large := cover_image_extra_large,
      cover_image_color := cover_image_color,
      popularity := popularity,
      favourites := favourites,
      site_url := site_url,
      is_adult := is_adult,
      genres := genres,
      tags := distinct (
        for tag in json_array_unpack(tags) union (
          with
            tag_id_al := <int32>json_get(tag, 'id_al'),
            tag_rank := <int32>json_get(tag, 'rank'),
          select anilist::Tag {
            @rank := tag_rank,
          }
          filter .id_al = tag_id_al
        )
      ),
    }
    unless conflict on .id_al
    else (
      update anilist::Media set {
        type := type,
        id_mal := id_mal,
        title_user_preferred := title_user_preferred,
        title_english := title_english,
        title_native := title_native,
        synonyms := synonyms,
        description := description,
        status := status,
        season := season,
        season_year := season_year,
        episodes := episodes,
        duration := duration,
        chapters := chapters,
        cover_image_extra_large := cover_image_extra_large,
        cover_image_color := cover_image_color,
        popularity := popularity,
        favourites := favourites,
        site_url := site_url,
        is_adult := is_adult,
        genres := genres,
        tags := distinct (
          for tag in json_array_unpack(tags) union (
            with
              tag_id_al := <int32>json_get(tag, 'id_al'),
              tag_rank := <int32>json_get(tag, 'rank'),
            select anilist::Tag {
              @rank := tag_rank,
            }
            filter .id_al = tag_id_al
          )
        ),
      }
    )
  ),
  _characters := (
    for character in json_array_unpack(characters) union (
      with
        id_al := <int32>json_get(character, 'id_al'),
        name_user_preferred := <str>json_get(character, 'name_user_preferred'),
        name_alternative := <array<str>>json_get(character, 'name_alternative'),
        name_alternative_spoiler := <array<str>>json_get(character, 'name_alternative_spoiler'),
        name_native := <str>json_get(character, 'name_native'),
        description := <str>json_get(character, 'description'),
        image_large := <str>json_get(character, 'image_large'),
        gender := <str>json_get(character, 'gender'),
        age := <str>json_get(character, 'age'),
        date_of_birth_year := <int32>json_get(character, 'date_of_birth_year'),
        date_of_birth_month := <int32>json_get(character, 'date_of_birth_month'),
        date_of_birth_day := <int32>json_get(character, 'date_of_birth_day'),
        favourites := <int32>json_get(character, 'favourites'),
        site_url := <str>json_get(character, 'site_url'),
      insert anilist::Character {
        id_al := id_al,
        name_user_preferred := name_user_preferred,
        name_alternative := name_alternative,
        name_alternative_spoiler := name_alternative_spoiler,
        name_native := name_native,
        description := description,
        image_large := image_large,
        gender := gender,
        age := age,
        date_of_birth_year := date_of_birth_year,
        date_of_birth_month := date_of_birth_month,
        date_of_birth_day := date_of_birth_day,
        favourites := favourites,
        site_url := site_url,
      }
      unless conflict on .id_al
      else (
        update anilist::Character set {
          name_user_preferred := name_user_preferred,
          name_alternative := name_alternative,
          name_alternative_spoiler := name_alternative_spoiler,
          name_native := name_native,
          description := description,
          image_large := image_large,
          gender := gender,
          age := age,
          date_of_birth_year := date_of_birth_year,
          date_of_birth_month := date_of_birth_month,
          date_of_birth_day := date_of_birth_day,
          favourites := favourites,
          site_url := site_url,
        }
      )
    )
  )
select {
  media := _media,
  characters := _characters,
}
"""


async def media_merge_combined_charas(
    executor: AsyncIOExecutor,
    *,
    media: Any,
    characters: Any,
) -> None:
    await executor.execute(
        EDGEQL_QUERY,
        media=orjson.dumps(media).decode(),
        characters=orjson.dumps(characters).decode(),
    )

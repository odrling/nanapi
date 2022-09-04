from typing import Any

import orjson
from edgedb import AsyncIOExecutor

EDGEQL_QUERY = r"""
with
  character := <json>$character,
  medias := <json>$medias,
  staffs := <json>$staffs,
  edges := <json>$edges,
  _character := (
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
  ),
  _medias := (
    for media in json_array_unpack(medias) union (
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
    )
  ),
  _staffs := (
    for staff in json_array_unpack(staffs) union (
      with
        id_al := <int32>json_get(staff, 'id_al'),
        favourites := <int32>json_get(staff, 'favourites'),
        site_url := <str>json_get(staff, 'site_url'),
        name_user_preferred := <str>json_get(staff, 'name_user_preferred'),
        name_alternative := <array<str>>json_get(staff, 'name_alternative'),
        name_native := <str>json_get(staff, 'name_native'),
        description := <str>json_get(staff, 'description'),
        image_large := <str>json_get(staff, 'image_large'),
        gender := <str>json_get(staff, 'gender'),
        age := <int32>json_get(staff, 'age'),
        date_of_birth_year := <int32>json_get(staff, 'date_of_birth_year'),
        date_of_birth_month := <int32>json_get(staff, 'date_of_birth_month'),
        date_of_birth_day := <int32>json_get(staff, 'date_of_birth_day'),
        date_of_death_year := <int32>json_get(staff, 'date_of_death_year'),
        date_of_death_month := <int32>json_get(staff, 'date_of_death_month'),
        date_of_death_day := <int32>json_get(staff, 'date_of_death_day'),
      insert anilist::Staff {
        id_al := id_al,
        favourites := favourites,
        site_url := site_url,
        name_user_preferred := name_user_preferred,
        name_alternative := name_alternative,
        name_native := name_native,
        description := description,
        image_large := image_large,
        gender := gender,
        age := age,
        date_of_birth_year := date_of_birth_year,
        date_of_birth_month := date_of_birth_month,
        date_of_birth_day := date_of_birth_day,
        date_of_death_year := date_of_death_year,
        date_of_death_month := date_of_death_month,
        date_of_death_day := date_of_death_day,
      }
      unless conflict on .id_al
      else (
        update anilist::Staff set {
          favourites := favourites,
          site_url := site_url,
          name_user_preferred := name_user_preferred,
          name_alternative := name_alternative,
          name_native := name_native,
          description := description,
          image_large := image_large,
          gender := gender,
          age := age,
          date_of_birth_year := date_of_birth_year,
          date_of_birth_month := date_of_birth_month,
          date_of_birth_day := date_of_birth_day,
          date_of_death_year := date_of_death_year,
          date_of_death_month := date_of_death_month,
          date_of_death_day := date_of_death_day,
        }
      )
    )
  ),
for edge in json_array_unpack(edges) union (
  with
    voice_actor_ids := <array<int32>>json_get(edge, 'voice_actor_ids'),
    media_id := <int32>json_get(edge, 'media_id'),
    character_role := <anilist::CharacterRole>json_get(edge, 'character_role'),
    voice_actor := (select _staffs filter .id_al in array_unpack(voice_actor_ids)),
    character := _character,
    media := (select _medias filter .id_al = media_id),
  insert anilist::CharacterEdge {
    character_role := character_role,
    character := character,
    media := media,
    voice_actors := voice_actor,
  }
  unless conflict on ((.character, .media)) else (
    update anilist::CharacterEdge set {
      character_role := character_role,
      voice_actors += voice_actor,
    }
  )
)
"""


async def c_edge_merge_combined_by_chara(
    executor: AsyncIOExecutor,
    *,
    character: Any,
    medias: Any,
    staffs: Any,
    edges: Any,
) -> None:
    await executor.execute(
        EDGEQL_QUERY,
        character=orjson.dumps(character).decode(),
        medias=orjson.dumps(medias).decode(),
        staffs=orjson.dumps(staffs).decode(),
        edges=orjson.dumps(edges).decode(),
    )

select anilist::Media {
  id_al,
}
filter .type = anilist::MediaType.ANIME
and .status = anilist::MediaStatus.NOT_YET_RELEASED

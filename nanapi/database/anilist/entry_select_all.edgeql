with
  media_type := <optional anilist::MediaType>$media_type,
  discord_id := <optional int64>$discord_id,
  entries := (
    (select anilist::Entry filter .account.user.discord_id = discord_id)
    if (exists discord_id) else
    (select anilist::Entry)
  ),
select entries {
  status,
  progress,
  score,
  media: {
    id_al,
  },
  account: {
    user: {
      discord_id,
      discord_id_str,
    },
  }
}
filter .media.type = media_type if exists media_type else true

with
  tag_name := <str>$tag_name,
  min_rank := <int32>$min_rank,
select anilist::Media {
  id_al,
}
filter .tags.name = tag_name and .tags@rank >= min_rank

with
  id := <uuid>$id
select quizz::Quizz {
  id,
  channel_id,
  channel_id_str,
  description,
  url,
  is_image,
  answer,
  answer_source,
  submitted_at,
  hikaried,
  author: {
    discord_id,
    discord_id_str,
  },
}
filter .id = id;

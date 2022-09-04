with
  channel_id := <int64>$channel_id
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
filter .client = global client and not exists .game and .channel_id = channel_id
order by .submitted_at
limit 1

with
  channel_id := <int64>$channel_id,
select quizz::Game {
  id,
  status,
  message_id,
  message_id_str,
  answer_bananed,
  started_at,
  ended_at,
  winner: {
    discord_id,
    discord_id_str,
  },
  quizz: {
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
}
filter .client = global client and .quizz.channel_id = channel_id and .status = quizz::Status.ENDED
order by .ended_at desc
limit 1

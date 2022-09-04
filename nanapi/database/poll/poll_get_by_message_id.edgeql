with
  message_id := <int64>$message_id,
select poll::Poll {
  message_id,
  message_id_str,
  channel_id,
  channel_id_str,
  question,
  options: {
    rank,
    text,
    votes: {
      user: {
        discord_id,
        discord_id_str,
      }
    }
  }
}
filter .message_id = message_id

with
  discord_id := <int64>$discord_id,
  message_id := <int64>$message_id,
  _user := (select user::User filter .discord_id = discord_id),
  _poll := (select poll::Poll { options } filter .message_id = message_id),
delete poll::Vote
filter .poll = _poll and .user = _user

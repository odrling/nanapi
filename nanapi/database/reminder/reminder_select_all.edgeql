select reminder::Reminder {
  id,
  channel_id,
  channel_id_str,
  message,
  timestamp,
  user: {
    discord_id,
    discord_id_str,
  },
}
filter .client = global client

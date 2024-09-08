with
  discord_id := <int64>$discord_id
delete calendar::UserCalendar
filter .user.discord_id = discord_id

with
  discord_id := <int64>$discord_id
select assert_single(calendar::UserCalendar) {
  ics,
  user: { * },
}
filter .user.discord_id = discord_id

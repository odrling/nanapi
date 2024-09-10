with
  discord_id := <int64>$discord_id,
  event := (
    delete calendar::GuildEvent
    filter .client = global client and .discord_id = discord_id
  ),
select event { ** }

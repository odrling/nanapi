with
  discord_id := <int64>$discord_id,
select pot::Pot { amount, count }
filter .client = global client and .user.discord_id = discord_id

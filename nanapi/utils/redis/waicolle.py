from nanapi.utils.redis.base import BooleanValue, StringValue

daily_tag = StringValue('waifu_daily_tag')
user_daily_roll = BooleanValue('waifu_player_daily_roll', default=False)
weekly_season = StringValue('waifu_weekly_season')
user_weekly_roll = BooleanValue('waifu_player_weekly_roll', default=False)

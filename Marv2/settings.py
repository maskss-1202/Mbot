from decouple import config


def get_key():
    return config('OPENAI_API_KEY')

def get_discord_token():
    return config('DISCORD_TOKEN')

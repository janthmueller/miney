import hikari
import lightbulb
import os
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')



default_enabled_guild = eval(os.getenv('DEFAULT_ENABLED_GUILD'))


bot = lightbulb.BotApp(token = discord_token, default_enabled_guilds = default_enabled_guild)

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print(f"Started bot.")
    
bot.load_extensions_from("./extensions")

if __name__ == '__main__':
    bot.run()
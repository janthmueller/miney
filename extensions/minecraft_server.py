import lightbulb
import psutil
import subprocess
import os

plugin = lightbulb.Plugin("minecraft_server")
valid_user_ids = eval(os.getenv('VALID_USER_IDS'))

def valid_user(func):
    async def wrapper(ctx):
        if ctx.author.id in valid_user_ids:
            return func(ctx)
        else:
            await ctx.respond("You are not authorized to use this command.")
    return wrapper

@plugin.command()
@lightbulb.command("start-server", "Starts the Minecraft server.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def start_server(ctx):
    if is_server_running():
        await ctx.respond("Server is already running.")
    else:
        subprocess.run(["sudo", "java", "-Xmx1024M", "-Xms1024M", "-jar", "~/minecraft_server/server.jar", "nogui"])
    

@plugin.command()
@lightbulb.command("server-online", "Checks if the server is online.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
@valid_user
async def server_online(ctx):
    if is_server_running():
        await ctx.respond("Server is online.")
    else:
        await ctx.respond("Server is offline.")
        
def is_server_running():
    for process in psutil.process_iter(['cmdline']):
        if "java" in process.info["cmdline"] and 'server.jar' in process.info["cmdline"]:
            return True
    return False


    

def load(bot):
    bot.add_plugin(plugin)

        

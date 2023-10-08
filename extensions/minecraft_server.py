import lightbulb
import psutil
import subprocess
import os

plugin = lightbulb.Plugin("minecraft_server")
valid_user_ids = eval(os.getenv('VALID_USER_IDS'))

@plugin.command()
@lightbulb.command("start-server", "Starts the Minecraft server.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def start_server(ctx):
    if is_server_running():
        await ctx.respond("Server is already running.")
    else:
        # Use os.path.expanduser to expand the tilde to the home directory
        jar_path = os.path.expanduser("~/minecraft_server/server.jar")
        subprocess.run(["sudo", "java", "-Xmx1024M", "-Xms1024M", "-jar", jar_path, "nogui"])
    

@plugin.command()
@lightbulb.command("server-online", "Checks if the server is online.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
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

        

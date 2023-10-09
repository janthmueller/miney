import lightbulb
import psutil
import asyncio
import os
import ast 

plugin = lightbulb.Plugin("minecraft_server")
valid_user_ids = ast.literal_eval(os.getenv('VALID_USER_IDS'))

process = None

@plugin.command()
@lightbulb.command("stop-server", "Stops the Minecraft server.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def stop_server(ctx):
    global process
    if ctx.interaction.user.id not in valid_user_ids:
        await ctx.respond("You do not have permission to use this command.")
    elif is_server_process_running():
        command = "/stop"
        await ctx.respond("Server stopping...")   
        await process.communicate(command.encode())
    else:
        await ctx.respond("Not able to stop. Server not running.")
    

@plugin.command()
@lightbulb.command("start-server", "Starts the Minecraft server.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def start_server(ctx):
    global process
    if ctx.interaction.user.id not in valid_user_ids:
        await ctx.respond("You do not have permission to use this command.")
    elif is_server_process_running():
        await ctx.respond("Server process is already running.")
    else:
        # Use os.path.expanduser to expand the tilde to the home directory
        jar_path = os.path.expanduser("~/minecraft_server/server.jar")

        # Get the directory of the jar file
        jar_directory = os.path.dirname(jar_path)

        # Change the working directory to the jar file's directory
        os.chdir(jar_directory)

        # Use asyncio.create_subprocess_exec to run the subprocess asynchronously
        process = await asyncio.create_subprocess_exec(
            "sudo", "java", "-Xmx1024M", "-Xms1024M", "-jar", "server.jar", "nogui",
            stdin=asyncio.subprocess.PIPE
        )
        


        # Respond to the Discord message
        await ctx.respond("Server starting...")
    

@plugin.command()
@lightbulb.command("server-process-running", "Checks if the server process is running.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def server_process_running(ctx):
    if is_server_process_running():
        await ctx.respond("Server process is running.")
    else:
        await ctx.respond("Server process is not running.")
        
def is_server_process_running():
    for process in psutil.process_iter(['cmdline']):
        if "java" in process.info["cmdline"] and 'server.jar' in process.info["cmdline"]:
            return True
    return False


def load(bot):
    bot.add_plugin(plugin)

        

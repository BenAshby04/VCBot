import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import os

from keep_alive import keep_alive
import praw
import random
import json

os.chdir("./")

# load_dotenv()
token = os.getenv('TOKEN')
# #Reddit Shiz
# Reddit_ClientID = os.getenv('Reddit_clientID')
# Reddit_clientSecret = os.getenv('Reddit_clientSecret')
# Reddit_Username = os.getenv('Reddit_Username')
# Reddit_Password = os.getenv('Reddit_Password')
# Reddit_userAgent = os.getenv('Reddit_userAgent')

# reddit = praw.Reddit(client_id=Reddit_ClientID,
#                      client_secret=Reddit_clientSecret,
#                      username=Reddit_Username,
#                      password=Reddit_Password,
#                      user_agent=Reddit_userAgent)

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)
GUILD = 'Vibe Central'

help_command = commands.DefaultHelpCommand(no_category='Commands')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='with your mum!'))

    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print(f'{client.user} has connected to {guild.name} (id:{guild.id})')

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members: \n - {members}')
        print("")


#########EveryoneCommands#########
@client.command(name="Ping", aliases=['ping'])
async def _ping(ctx):
    await ctx.send("Pong! {0}ms".format(round(client.latency, 2)))


@client.command()
async def hello(ctx, arg1, arg2):
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)
    await ctx.send("This is arg1 '" + arg1 + "' This is arg2 '" + arg2 + "'!")


@client.command()
async def users(ctx):
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)

    num = len(ctx.guild.members)

    await ctx.send("There are " + str(num) +
                   " members in this discord server!")


@client.command()
async def cum(ctx):
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)

    await ctx.send("💦")
    await ctx.send("💦")
    await ctx.send("💦")


@client.command()
async def oliver(ctx):
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)

    await ctx.send("No situational awareness **wanker**")


@client.command()
async def flipdatable(ctx):
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)

    await ctx.send("(╯°□°）╯︵ ┻━┻")


@client.command()
async def cortana(ctx):
    file1 = open('./quotes/cortana', 'r')
    Lines = file1.readlines()
    line = random.randrange(int(Lines.__len__() + 1))
    em = discord.Embed(title="Here is you quote Cheif",
                       description=Lines[int(line)])
    await ctx.send(embed=em)
    file1.close()


@client.command(name="memes", aliases=['meme'])
async def _reddit(ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []
    top = list(subreddit.hot(limit=100))

    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name, description=url)
    em.set_image(url=url)

    await ctx.send(embed=em)


@client.command()
async def nonce(ctx, user: discord.Member):
    await ctx.send(f"Get pinged {user.mention}")


@client.command()
async def dan(ctx):
    await ctx.send("**weeb**")


#########DNDCommands#########
@client.command(name="Roll", aliases=["roll", "Rolling"])
async def roll(ctx, roll):
    roll = random.randint(1, int(roll))

    print(roll)
    await ctx.send("You rolled a " + str(roll))


@client.command(name="Encounter", aliases=["encounter", "en"])
async def _Encounter(ctx):
    file = open('./dnd/monsterList', 'r')
    Lines = file.readlines()
    line = random.randrange(int(Lines.__len__() + 1))
    await ctx.send("Here is a random monster for you: \n" + Lines[int(line)])


@client.command(name="Location", aliases=["location", "locations", "loc"])
async def _location(ctx):
    file = open('./dnd/locationList', 'r')
    Lines = file.readlines()
    line = random.randrange(int(Lines.__len__() + 1))
    await ctx.send("Here is a random location for you: \n" + Lines[int(line)])


#########NSFWCommands#########


@client.command(name="rule34")
@commands.is_nsfw()
async def _rule34(ctx):
    subreddit = reddit.subreddit("rule34")
    all_subs = []
    top = subreddit.hot(limit=50)

    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name, description=url)
    em.set_image(url=url)

    await ctx.send(embed=em)


@client.command(name="neko")
@commands.is_nsfw()
async def _neko(ctx):
    subreddit = reddit.subreddit("aww")
    all_subs = []
    top = subreddit.hot(limit=50)

    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name, description=url)
    em.set_image(url=url)

    await ctx.send(embed=em)


#########EconomyCommands#########
@client.command(name="balance", aliases=["bal"])
async def balance(ctx):

    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{ctx.author.name}'s balance'",
                       color=discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name="Bank Balance", value=bank_amt)

    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(101)

    await ctx.send(f"Someone gave you {earnings} coins!!")

    users[str(user.id)]["wallet"] = users[str(user.id)]["wallet"] + earnings

    await net_worth_update(user, earnings)

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

@client.command()
async def openBank(ctx):
  await open_account(ctx.author)
  


@client.command()
async def bank(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()

    user = ctx.author

    amount_banked = users[str(user.id)]["wallet"]

    em = discord.Embed(title="Banked",
                       description=f"You have banked {amount_banked}!")
    await ctx.send(embed=em)

    users[str(user.id)]["bank"] += users[str(user.id)]["wallet"]
    users[str(user.id)]["wallet"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@client.command(name="withdraw")
async def withdraw(ctx, arg1):
    await open_account(ctx.author)
    users = await get_bank_data()

    user = ctx.author

    withdraw_amount = int(arg1)

    bank = users[str(user.id)]["bank"]

    if int(withdraw_amount) > int(bank):
        em = discord.Embed(
            title="Withdraw Failed",
            description=
            "Your withdraw has failed, no balance have changed: You dont have enough money in the bank!"
        )
        await ctx.send(embed=em)
        return

    users[str(user.id)]["wallet"] += int(withdraw_amount)
    users[str(user.id)]["bank"] -= int(withdraw_amount)

    bankTotal = users[str(user.id)]["bank"]
    walletTotal = users[str(user.id)]["wallet"]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    em = discord.Embed(
        title="Withdrawed",
        description=
        f"You have withdrawed {withdraw_amount}! You now have {walletTotal} in your wallet and {bankTotal} in your bank account!"
    )
    await ctx.send(embed=em)


@client.command(name="Invest", aliases=["invest", "Investing"])
async def invest(ctx):
    await ctx.send("Investing")


@client.command(name="Coin", aliases=["coin", "coinflip", "flip"])
async def coin(ctx, arg1, arg2):
    await open_account(ctx.author)
    users = await get_bank_data()

    user = ctx.author
    amount_bet = arg2
    choice = arg1
    user_wallet = users[str(user.id)]["wallet"]

    if int(amount_bet) > user_wallet:
        await ctx.send(
            f"You dont have enough in your wallet to bet!\nYou have {user_wallet} in your wallet!"
        )
        return

    chance = random.randrange(12)
    # heads 1-5 tails 6-11
    if chance > 5:
        won = "tail"
    if chance <= 5:
        won = "head"

    if choice != "head" and choice != "tail" and choice != "h" and choice != "t":
        print("reached")
        await ctx.send(
            "Please use head or tail (example command: $coin head 500)")
        return

    if choice == "head" or choice == "h":
        choice2 = "head"

    if choice == "tail" or choice == "t":
        choice2 = "tail"

    if choice2 == won:
        users[str(user.id)]["wallet"] += int(amount_bet)
        user_wallet = users[str(user.id)]["wallet"]

        em = discord.Embed(
            title="You won!",
            description=f"You have {user_wallet} in your wallet")

        await net_worth_update(user, amount_bet)

        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    else:
        users[str(user.id)]["wallet"] -= int(amount_bet)
        user_wallet = users[str(user.id)]["wallet"]

        em = discord.Embed(
            title="You Lost!",
            description=f"You lost {amount_bet}!\nYou now have {user_wallet}!")
        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    await ctx.send(embed=em)

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


async def net_worth_update(user, net):
    users = await get_bank_data()

    users[str(user.id)]["net_worth"] += net

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["net_worth"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users


#########ModeratorCommands#########


@client.command()
@has_permissions(kick_members=True, ban_members=True)
async def mute(ctx):
    await ctx.send("Hello Moderator")


#########AdminCommands#########


@client.command(name="ban")
@has_permissions(kick_members=True, ban_members=True)
async def ban(ctx):
    await ctx.send("your nan has been banned")


#########ErrorHandling#########
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(ctx.author)
        print(ctx.guild)
        print(ctx.message)
        print("Command is invalid")
        await ctx.send("The Command is invalid")

    if isinstance(error, commands.errors.NSFWChannelRequired):
        print(ctx.author)
        print(ctx.guild)
        print(ctx.message)
        print("NSFW Command in a non NSFW channel")
        msg = discord.Embed()
        msg.title = "NSFW Command"
        msg.description = error.args[0]
        return await ctx.send(embed=msg)

    if isinstance(error, commands.errors.CommandOnCooldown):
        print("Command is on cooldown")
        msg = discord.Embed(title="Command on Cooldown",
                            description=error.args[0])
        return await ctx.send(embed=msg)


keep_alive()
client.run(token)

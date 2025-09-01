import discord
from discord.ext import commands
from threading import Thread
from flask import Flask
import random
import os



app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()
    
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

server_settings = {}

welcome_messages = [
    "ยินดีต้อนรับ {member.mention} เข้าสู่บ้านนี้ 💖",
    "โอ้วว มาแล้วๆ {member.mention}! ปูพรมแดงต้อนรับเลย 🎉",
    "หวัดดี {member.mention} ✨ มาร่วมแจมกับพวกเรากันเถอะ!",
    "เย้ๆ {member.mention} มาแล้วว 🥳 สนุกกันเลย",
    "ฮัลโหลล {member.mention} 💕 ดีใจที่นายเข้ามานะ!"
]

goodbye_messages = [
    "ลาก่อน {member.name} 😢 ขอให้โชคดีนะ",
    "{member.name} ออกจากเซิร์ฟแล้ว 💔",
    "再见 {member.name} 👋 ไว้เจอกันใหม่",
    "โอ้ยย {member.name} ทิ้งพวกเราไปแล้ว 🥲",
    "บายยย {member.name} 🚪"
]

@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้ว: {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel):
    guild_id = ctx.guild.id
    if guild_id not in server_settings:
        server_settings[guild_id] = {}
    server_settings[guild_id]["welcome"] = channel.id
    await ctx.send(f"✅ ตั้งค่าห้องต้อนรับเป็น {channel.mention} แล้ว")

@bot.command()
@commands.has_permissions(administrator=True)
async def setgoodbye(ctx, channel: discord.TextChannel):
    guild_id = ctx.guild.id
    if guild_id not in server_settings:
        server_settings[guild_id] = {}
    server_settings[guild_id]["goodbye"] = channel.id
    await ctx.send(f"✅ ตั้งค่าห้องลาออกเป็น {channel.mention} แล้ว")

@bot.event
async def on_member_join(member):
    guild_id = member.guild.id
    if guild_id in server_settings and "welcome" in server_settings[guild_id]:
        channel = bot.get_channel(server_settings[guild_id]["welcome"])
        if channel:
            message = random.choice(welcome_messages).format(member=member)
            await channel.send(message)

@bot.event
async def on_member_remove(member):
    guild_id = member.guild.id
    if guild_id in server_settings and "goodbye" in server_settings[guild_id]:
        channel = bot.get_channel(server_settings[guild_id]["goodbye"])
        if channel:
            message = random.choice(goodbye_messages).format(member=member)
            await channel.send(message)

@bot.command()
async def แนะนำ(ctx):
    await ctx.send("นี่คือคำแนะนำจากบอท ✨: อย่าลืมพักผ่อนด้วยนะคะ!")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="ไม่ระบุเหตุผล"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} ถูกเตะออก (เหตุผล: {reason})")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="ไม่ระบุเหตุผล"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} ถูกแบน (เหตุผล: {reason})")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f"✅ {user.name} ถูกปลดแบนแล้ว")
            return
    await ctx.send("❌ ไม่เจอคนที่จะแบน")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason="ไม่ระบุเหตุผล"):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"🤐 {member} ถูกมิวท์ (เหตุผล: {reason})")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"🔊 {member} ถูกปลดมิวท์แล้ว")
    else:
        await ctx.send("❌ คนนี้ไม่ได้ถูกมิวท์อยู่")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if any(word in message.content for word in ["สวัสดีครับ", "สวัสดีคะ", "สวัสดีคับ"]):
        await message.channel.send("สวัสดีค่ะ 👋")
    await bot.process_commands(message)

keep_alive()
bot.run(os.environ['DISCORD_TOKEN'])


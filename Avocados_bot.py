import discord
from discord.ext import commands
import random

# สร้างบอท
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

welcome_messages = [
    "ยินดีต้อนรับ {member.mention} เข้าสู่บ้านนี้ 💖",
    "โอ้วว มาแล้วๆ {member.mention}! ปูพรมแดงต้อนรับเลย 🎉",
    "หวัดดี {member.mention} ✨ มาร่วมแจมกับพวกเรากันเถอะ!",
    "เย้ๆ {member.mention} มาแล้วว 🥳 สนุกกันเลย",
    "ฮัลโหลล {member.mention} 💕 ดีใจที่นายเข้ามานะ!"
]

# เมื่อบอทออนไลน์
@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้ว: {bot.user}")

# คำสั่งง่ายๆ
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
    if "สวัสดีครับ" in message.content or "สวัสดีคะ" in message.content or "สวัสดีคับ" in message.content:
        await message.channel.send("สวัสดีค่ะ 👋")
    await bot.process_commands(message)


bot.run("MTQxMTk2MzQ3OTg5OTc2Njg3Ng.Gqdcm6.-wZfO8nQmPHZofreAI3mm-eInggySiR3XYTx3I")

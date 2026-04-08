import discord
from discord.ext import commands

from config import TOKEN
from logic import create_db, add_asset, get_assets, save_user, get_user


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

create_db()


@bot.event
async def on_ready():
    print(f"Giris yapildi: {bot.user}")


@bot.command()
async def ekle(ctx, coin: str, amount: float):
    add_asset(ctx.author.id, coin, amount)
    await ctx.send(f"{coin.upper()} icin {amount} eklendi.")


@bot.command()
async def portfoy(ctx):
    rows = get_assets(ctx.author.id)
    if not rows:
        await ctx.send("Portfoy bos.")
        return
    text = "\n".join([f"{coin}: {amt}" for coin, amt in rows])
    await ctx.send(f"Portfoyun:\n{text}")


@bot.command()
async def kayit(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Ad Soyad yaz:")
    ad_soyad = (await bot.wait_for("message", check=check, timeout=120)).content

    await ctx.send("Yasadigin yer yaz:")
    sehir = (await bot.wait_for("message", check=check, timeout=120)).content

    await ctx.send("1 tane projenin adini yaz:")
    proje = (await bot.wait_for("message", check=check, timeout=120)).content

    save_user(ctx.author.id, ad_soyad, sehir, proje)
    await ctx.send(
        f"Kayit tamam.\nAd Soyad: {ad_soyad}\nYer: {sehir}\nProje: {proje}"
    )


@bot.command()
async def bilgim(ctx):
    row = get_user(ctx.author.id)
    if not row:
        await ctx.send("Kayit bulunamadi. Once !kayit yap.")
        return
    full_name, city, project = row
    await ctx.send(
        f"Bilgilerin:\nAd Soyad: {full_name}\nYasadigin Yer: {city}\nProje: {project}"
    )


bot.run(TOKEN)
import aiohttp
import discord
from discord.ext import commands
import os

token = os.environ['TOKEN_DISCORD']
api_KEY = os.environ['NEWS_API']

# Initialisation du bot avec intentions
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} a bien été connecté à Discord!')

async def get_news(query=None, news_type=None, location=None):
    # Liste étendue de termes pour couvrir divers aspects de la cybersécurité
    base_query = (
        "cybersecurity OR information security OR data breach OR hacking OR cyber attack "
        "OR malware OR ransomware OR phishing OR DDoS OR firewall OR cryptography "
        "OR network security OR social engineering OR penetration testing OR CTF "
        "OR bug bounty OR zero-day OR threat hunting OR incident response OR AI security "
        "OR artificial intelligence OR machine learning OR deep learning OR autonomous systems "
        "OR ethical hacking OR cyber forensics OR cybercrime OR dark web"
    )

    if query:
        base_query += f" AND {query}"

    url = f'https://newsapi.org/v2/everything?q={base_query}&apiKey={api_KEY}'

    if news_type:
        url += f'&category={news_type}'
    if location:
        url += f'&domains={location}.news'

    print(f"URL de l'API: {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"Réponse de l'API: {data}")
                articles = data.get('articles', [])
                news_list = [{'title': article['title'], 'url': article['url']} for article in articles[:10]]
                return news_list
            else:
                print(f"Erreur: statut de réponse {resp.status}")
                return []

@bot.command(name='news', help='Recherche des actualités sur la cybersécurité et les technologies connexes')
async def get_cyber_news(ctx, *, query=None):
    news = await get_news(query)
    await send_news_embeds(ctx, news)

@bot.command(name='specific_news', help='Recherche spécifique sur la cybersécurité et les technologies connexes par type et lieu')
async def get_specific_cyber_news(ctx, query=None, news_type=None, location=None):
    news = await get_news(query, news_type, location)
    await send_news_embeds(ctx, news)

async def send_news_embeds(ctx, news):
    if not news:
        await ctx.send("Aucune actualité trouvée.")
        return

    embeds = [discord.Embed(title=item['title'], url=item['url']) for item in news]
    await ctx.send(embeds=embeds)

class NewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_news(self, query=None, news_type=None, location=None):
        # Code similaire à la fonction get_news ci-dessus
        pass

# Ajout du Cog au bot
async def setup(bot):
    await bot.add_cog(NewsCog(bot))

bot.run(token)

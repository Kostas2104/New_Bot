import discord
import requests
import os
import psycopg2
from discord.ext import commands
from get_balances import get_caw_balances
from datetime import datetime

TOKEN = os.getenv("TOKEN")  # Discord Bot Token
CMC_API_KEY = os.getenv("CMC_API_KEY")  # CoinMarketCap API Key
CMC_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)




# Format numbers for display with commas
def format_large_number(value):
    if value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T".replace(",", "")  # Trillions
    elif value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B".replace(",", "")  # Billions
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M".replace(",", "")  # Millions
    else:
        return f"{value:,.2f}"  # Numbers under a million with commas

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')



# 📌 CDC Wallet Titles (excluding Burn)
CDC_WALLET_TITLES = ["wallet_3da3", "wallet_677f", "wallet_825b", "wallet_7fc6"]
MC_TITLE = "Market Cap"
GATE_IO_TITLE = ["Gate.io"]

# 📌 Format number to Trillions (T)
def format_trillions(value):
    return f"{value / 1_000_000_000_000:.2f} T"

# 📌 Format number to Trillions (T)
def format_billions(value):
    return f"{value / 1_000_000_000:.2f} B"

# 📌 Format number to Trillions (T)
def format_millions(value):
    return f"{value / 1_000_000:.2f} M"


async def cdc(ctx):
    cdc_balances, burn_balance, cdc_total, cdc_percentage, gateio_balances = get_caw_balances()
    caw_market_cap = await get_caw_market_cap() # Fetch market cap

    if cdc_balances:
        message = "**📊 CDC Wallet Balances:**\n"

        # Print individual CDC balances
        for title, balance in zip(CDC_WALLET_TITLES, cdc_balances):
            message += f"- **{title}:** {format_trillions(balance)} CAW\n"

        # Print CDC total and percentage
        message += f"\n**⚠️ Total CDC Holdings: {format_trillions(cdc_total)} CAW**"
        message += f"\n**📈 Percentage of Total Supply: {cdc_percentage:.4f}%**"

        # Print individual GATE.IO balance
        for title, balance in zip(GATE_IO_TITLE, gateio_balances):
            message += f"\n\n**{title}:** {format_trillions(balance)} CAW"

        # Add CAW Market Cap
        if caw_market_cap is not None:
            message += f"\n\n**🌐 CAW Market Cap: ${format_large_number(caw_market_cap)} USD**"
        else:
            message += "\n\n**🌐 CAW Market Cap: N/A (Could not fetch)**"



        await ctx.send(message)
    else:
        await ctx.send("❌ Unable to fetch balances!")


import discord, asyncio, pathlib, random, requests
from bs4 import BeautifulSoup as soup
from discord.ext import commands 
from tools import utils, config 
from tools.utils import color, footer, embed, error, usage
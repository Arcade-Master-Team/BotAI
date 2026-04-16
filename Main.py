import discord
import random
from discord.ext import commands
from PIL import Image
import numpy as np
from tensorflow import load_model

model = load_model("keras_model.h5")
with open("labels.txt", "r") as f:
    class_names = f.read().splitlines()

def get_class(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize(224, 224)
    image = np.array(image)
    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image)
    index = np.argnax(prediction)

    class_name = class_names[index]
    confidence = float(prediction[0] [index])

    return class_name, confidence



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def bienvenida(ctx):
    await ctx.send("Bienvenido a mi servidor!")

@bot.command()
async def dircall(ctx):
    await ctx.send(f"Hola{ctx.author.mention}, bienvenido")

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def add(ctx, left: float, right: float):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def operation(ctx, left: float, symbol: str, right: float):
    """Adds two numbers together."""
    if symbol == "+":
        await ctx.send(left + right)
    elif symbol == "-":
        await ctx.send(left - right)
    elif symbol == "*" or symbol == "x":
        await ctx.send(left * right)
    elif symbol == "/":
        await ctx.send(left / right)
    elif symbol == "%":
        await ctx.send(left % right)
    else:
        await ctx.send("Invalid symbol")

@bot.command()
async def imageDetect(ctx):
    if ctx.message.attachments:
        for at in ctx.message.attachments:
            file_name = at.filename
            file_path = f"./Imagenes/{file_name}"
            await at.save(file_path)
            clase, confianza = get_class(file_path)
            await ctx.send(f"Clase: {clase},Confianza: {confianza:.2f}")
    else:
        await ctx.send("no attachments")
bot.run("Enter bot id")

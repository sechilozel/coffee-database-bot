import discord
from discord.ext import commands
import pandas as pd
from thefuzz import process
from logic import DB_Manager
from config import TOKEN, DATABASE

manager = DB_Manager(DATABASE)

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)


df = pd.read_csv("coffeee.csv")
df['keywords'] = df['Kahve Tipi'].str.lower().str.split()  

def guess_coffee(user_input, df, threshold=70):
    user_input = user_input.lower()
    choices = df['Kahve Tipi'].tolist() + [' '.join(k) for k in df['keywords']]
    best_match = process.extractOne(user_input, choices)
    
    if best_match[1] >= threshold:
       
        recipe_row = df[df['Kahve Tipi'] == best_match[0]]
        if not recipe_row.empty:
            return recipe_row.iloc[0].to_dict()
   
        for i, kws in enumerate(df['keywords']):
            if best_match[0] == ' '.join(kws):
                return df.iloc[i].to_dict()
    return None


@bot.command()
async def kahve(ctx, *, message):
    result = guess_coffee(message, df)
    if result:
        # message.lower()
        # await ctx.send(manager.give_coffee)
        # response = "\n".join([f"{k}: {v}" for k, v in result.items()])
        response = "\n".join([f"{k}: {v}" for k, v in result.items() if k != 'keywords'])
    else:
        user_input_lower = message.lower()
        choices = df['Kahve Tipi'].tolist() + [' '.join(k) for k in df['keywords']]
        best_match = process.extractOne(user_input_lower, choices)
        
        if best_match[1] >= 20:
            # Sadece tahmin edilen kahve ismini göster
            await ctx.send(f"İstediğiniz kahve bu olabilir mi? -> {best_match[0]}")
        else:
            await ctx.send("Üzgünüm, bu kahveyi bulamadım.")
        # response = "Üzgünüm, bu kahveyi bulamadım."
    await ctx.send(response)


bot.run(TOKEN)


#YENI VERSIYON CALISIYO
import discord
from discord.ext import commands
import pandas as pd
from thefuzz import process
from config import token
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


df = pd.read_csv("coffeee.csv")
df['keywords'] = df['Kahve Tipi'].str.lower().str.split()

def guess_coffee(user_input, df, threshold=70):
    user_input = user_input.lower()
    choices = df['Kahve Tipi'].tolist() + [' '.join(k) for k in df['keywords']]
    best_match = process.extractOne(user_input, choices)
    
    if best_match[1] >= threshold:
        recipe_row = df[df['Kahve Tipi'] == best_match[0]]
        if not recipe_row.empty:
            return recipe_row.iloc[0].to_dict()
        for i, kws in enumerate(df['keywords']):
            if best_match[0] == ' '.join(kws):
                return df.iloc[i].to_dict()
    return None

@bot.command()
async def kahve(ctx, *, message):
    result = guess_coffee(message, df)
    
    if result:
        
        response = "\n".join([f"{k}: {v}" for k, v in result.items() if k not in ['keywords', 'Resim']])
        image_url = result.get('Resim', None)
        
        
        if image_url and isinstance(image_url, str) and image_url.strip():
            await ctx.send(response)
            await ctx.send(image_url)
        else:
            await ctx.send(response)

    else:
        
        user_input_lower = message.lower()
        choices = df['Kahve Tipi'].tolist() + [' '.join(k) for k in df['keywords']]
        best_match = process.extractOne(user_input_lower, choices)

        if best_match[1] >= 50:
            await ctx.send(f"İstediğiniz kahve bu olabilir mi? -> {best_match[0]}")
        else:
            await ctx.send("Üzgünüm, bu kahveyi bulamadım.")

bot.run(token)




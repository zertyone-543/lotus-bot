import discord
from discord.ext import commands
import os

# --- CONFIG ---
TOKEN = os.getenv('DISCORD_TOKEN') 
PUBLIC_CHANNEL_NAME = "général"  # Ton salon général existant
PRIVATE_CHANNEL_NAME = "candidats-prives"  # Ton salon privé existant

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def add_to_private_channel(member):
    """Ajoute la personne au salon privé existant"""
    try:
        # Trouver ton salon privé existant
        channel = discord.utils.get(member.guild.channels, name=PRIVATE_CHANNEL_NAME)
        
        if channel:
            # Donner l'accès au membre
            await channel.set_permissions(member, read_messages=True, send_messages=True)
            print(f"✅ {member} ajouté au salon {PRIVATE_CHANNEL_NAME}")
            
            # Message de bienvenue dans le salon privé
            welcome_msg = (
                f"🎉 **Bienvenue {member.mention} chez Lotus Capital !**\n\n"
                f"**Félicitations pour ta décision de devenir trader !** 🚀\n\n"
                f"📋 **Prochaines étapes :**\n"
                f"• Tu recevras tes identifiants de compte démo sous 24h\n"
                f"• Consulte les règles de trading épinglées\n"
                f"• Pose tes questions ici librement\n\n"
                f"L'équipe Lotus Capital te souhaite bonne chance ! 📈"
            )
            await channel.send(welcome_msg)
            
        else:
            print(f"❌ Salon privé '{PRIVATE_CHANNEL_NAME}' non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

@bot.event
async def on_message(message):
    # Ignorer les messages du bot
    if message.author == bot.user:
        return

    # Vérifier si le message est dans le salon GÉNÉRAL
    if message.channel.name == PUBLIC_CHANNEL_NAME:
        # Si le message contient "new trader"
        if "new trader" in message.content.lower():
            print(f"👤 Nouveau trader détecté: {message.author}")
            
            # Ajouter au salon privé
            await add_to_private_channel(message.author)
            
            # Répondre dans le général
            await message.channel.send(
                f"✅ **Excellent choix {message.author.mention} !** 🚀\n"
                f"Je t'ai ajouté automatiquement au salon privé des traders.\n"
                f"Tu y recevras toutes les informations importantes !"
            )
    
    # Important pour les commandes
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté: {bot.user}")
    print(f"🎯 Surveillance du salon: #{PUBLIC_CHANNEL_NAME}")
    print("🤖 En attente de 'new trader'...")

@bot.command()
async def test_bot(ctx):
    """Teste si le bot fonctionne"""
    await ctx.send("✅ Bot opérationnel ! Écrivez 'new trader' dans le général.")

# --- LANCEMENT ---
bot.run(TOKEN)
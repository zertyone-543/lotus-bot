import discord
from discord.ext import commands
import os

TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# --- CONFIGURATION ---
COHORT_ROLES = {
    "active": "Trader Actif",
    "waiting": "En Attente", 
    "alumni": "Alumni"
}

CHANNELS = {
    "public": "général",
    "private": "cohorte-privée"
}

# --- SYSTÈME D'ACCUEIL ---
@bot.event
async def on_ready():
    print(f'✅ Bot Lotus Capital connecté: {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="les traders 🌟"))

@bot.event
async def on_member_join(member):
    """Accueil automatique des nouveaux membres"""
    print(f"👤 Nouveau trader: {member}")
    
    # Message de bienvenue en MP
    try:
        await member.send(
            "🎉 **BIENVENUE CHEZ LOTUS CAPITAL !**\n\n"
            "Nous sommes ravis de vous accueillir dans notre communauté de traders.\n\n"
            "**Prochaines étapes:**\n"
            "• Vérification de votre inscription en cours\n"
            "• Attribution de votre cohorte sous 24h\n"
            "• Accès à l'espace privé des traders\n\n"
            "**Commandes utiles:**\n"
            "`!drawdown` - Règles de risque\n"
            "`!assessment` - Phases d'évaluation\n"
            "`!platform` - Plateformes de trading\n"
            "`!help` - Aide complète\n\n"
            "Bonne chance pour votre parcours ! 📈"
        )
    except:
        print(f"❌ Impossible d'envoyer MP à {member}")
    
    # Attribution rôle "En Attente"
    waiting_role = discord.utils.get(member.guild.roles, name=COHORT_ROLES["waiting"])
    if waiting_role:
        await member.add_roles(waiting_role)
        print(f"✅ Rôle '{waiting_role.name}' assigné à {member}")

# --- COMMANDES FAQ ---
@bot.command()
async def drawdown(ctx):
    """Règles de drawdown et risk management"""
    embed = discord.Embed(
        title="📉 RÈGLES DE DRAWDOWN",
        color=0xff0000,
        description="Paramètres de risk management pour tous les traders"
    )
    embed.add_field(name="🎯 Quotidien", value="**3% maximum**", inline=True)
    embed.add_field(name="📊 Total", value="**6% maximum**", inline=True)
    embed.add_field(name="⚡ Conséquence", value="Dépassement = Disqualification immédiate", inline=False)
    embed.add_field(name="💡 Conseil", value="Tradez small pour garder le contrôle !", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def assessment(ctx):
    """Phases du programme d'assessment"""
    embed = discord.Embed(
        title="📊 PHASES D'ASSESSMENT",
        color=0x00ff00,
        description="Progression vers le compte funded"
    )
    embed.add_field(name="1. ÉVALUATION", value="**Target: +8%**\nDurée: 30 jours", inline=True)
    embed.add_field(name="2. CONSISTANCE", value="**Target: +5%**\nDurée: 60 jours", inline=True)
    embed.add_field(name="3. FUNDED", value="**Split: 80/20**\nCompte réel", inline=True)
    embed.add_field(name="📋 Détails", value="[Lien vers le guide complet]", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def platform(ctx):
    """Plateformes de trading supportées"""
    embed = discord.Embed(
        title="💻 PLATEFORMES DE TRADING",
        color=0x0099ff,
        description="Plateformes officiellement supportées"
    )
    embed.add_field(name="🖥️ MT5", value="**Recommandée**\nDémo + Compte réel", inline=True)
    embed.add_field(name="📱 cTrader", value="**Alternative**\nInterface moderne", inline=True)
    embed.add_field(name="🔧 Support", value="Aide à la configuration disponible", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def help_bot(ctx):
    """Affiche toutes les commandes disponibles"""
    embed = discord.Embed(
        title="🆘 AIDE - COMMANDES DISPONIBLES",
        color=0xff9900
    )
    embed.add_field(name="📉 Risk Management", value="`!drawdown` - Règles de drawdown", inline=False)
    embed.add_field(name="📊 Assessment", value="`!assessment` - Phases du programme", inline=False)
    embed.add_field(name="💻 Platforms", value="`!platform` - Plateformes supportées", inline=False)
    embed.add_field(name="👥 Cohorte", value="`!cohort` - Statut de votre cohorte", inline=False)
    embed.add_field(name="ℹ️ Aide", value="`!help` - Ce message", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def cohort(ctx):
    """Vérifie le statut de cohorte"""
    embed = discord.Embed(
        title="👥 STATUT DE COHORTE",
        color=0x9932cc,
        description="Vérification en cours..."
    )
    embed.add_field(name="📊 Votre statut", value="**En traitement**", inline=True)
    embed.add_field(name="⏱️ Délai", value="**24-48 heures**", inline=True)
    embed.add_field(name="📧 Contact", value="Un email vous parviendra pour confirmation", inline=False)
    await ctx.send(embed=embed)

# --- SYSTÈME DE VÉRIFICATION COHORTE ---
@bot.command()
async def verifier(ctx, email: str):
    """Vérifie si un trader est accepté dans une cohorte"""
    
    # LISTE TEST - Simule Google Sheets
    traders_acceptes = {
        "trader1@lotus.com": "Cohorte 1",
        "trader2@lotus.com": "Cohorte 1", 
        "trader3@lotus.com": "Cohorte 2",
        "test@lotus.com": "Cohorte 1"
    }
    
    if email in traders_acceptes:
        cohorte = traders_acceptes[email]
        
        # Donner le rôle de la cohorte
        role_cohorte = discord.utils.get(ctx.guild.roles, name=cohorte)
        if role_cohorte:
            await ctx.author.add_roles(role_cohorte)
        
        # Donner accès au salon privé
        salon_prive = discord.utils.get(ctx.guild.channels, name="cohorte-privée")
        if salon_prive:
            await salon_prive.set_permissions(ctx.author, read_messages=True, send_messages=True)
        
        embed = discord.Embed(
            title="✅ TRADER ACCEPTÉ",
            color=0x00ff00,
            description=f"**Email:** {email}"
        )
        embed.add_field(name="👥 Cohorte", value=cohorte, inline=True)
        embed.add_field(name="🔐 Accès", value="Salon privé activé", inline=True)
        embed.add_field(name="🎯 Statut", value="ACTIF", inline=True)
        await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(
            title="⏳ EN ATTENTE",
            color=0xff9900,
            description=f"**Email:** {email}"
        )
        embed.add_field(name="📊 Statut", value="Liste d'attente", inline=True)
        embed.add_field(name="📧 Contact", value="Vous serez notifié par email", inline=True)
        await ctx.send(embed=embed)

# --- LANCEMENT ---
bot.run(TOKEN)

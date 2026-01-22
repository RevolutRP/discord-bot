import discord
from keep_alive import keep_alive
keep_alive()

from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

questions = [
    {"q": "Sta je FearRP?", "options": {"A": "Plasenje drugih igraca", "B": "Strah za vlastiti zivot", "C": "Izgledati strasno"}, "answer": "B"},
    {"q": "Sta je DM?", "options": {"A": "Ubijanje igraca", "B": "Borba dva igraca", "C": "Ubijanje bez razloga"}, "answer": "C"},
    {"q": "Sta je CB?", "options": {"A": "Prozivanje policije", "B": "Postovanje policije", "C": "Ignorisanje policije"}, "answer": "A"},
    {"q": "Sta je VDM?", "options": {"A": "Voznja u vozilu", "B": "Pucanje iz vozila", "C": "Gazenje igraca"}, "answer": "C"},
    {"q": "Sta je KRP?", "options": {"A": "Ubijanje po RP-u", "B": "Prekidanje RP-a", "C": "Kidnapovanje po RP-u"}, "answer": "B"},
    {"q": "Ti i prijatelj hodate ulicom, neko kaze dizi ruke, prijatelj vadi pištolj i puca. Sta je prekrseno?", "options": {"A": "PG", "B": "RPS", "C": "FearRP"}, "answer": "C"},
    {"q": "Lovi te policija, ti skaces u vodu i zoves prijatelja na radio da dodje. Sta je prekrseno?", "options": {"A": "MG", "B": "PG", "C": "CB"}, "answer": "B"},
    {"q": "Vozis se autom, vidis lika i zabijes se u njega. Sta je prekrseno?", "options": {"A": "VDM", "B": "RDM", "C": "DM"}, "answer": "A"},
    {"q": "Bjezis od policije, sakrijes se u neku ulicu i izadjes iz igre. Sta je prekrseno?", "options": {"A": "DTA", "B": "LTA", "C": "RPS"}, "answer": "B"},
    {"q": "Zaustavlja te policija, ti nemas dokumente, ali preko me/do komandi dajes dokumente. Sta je prekrseno?", "options": {"A": "RPS", "B": "FailRP", "C": "RP2WIN"}, "answer": "C"},
]

class QuizView(discord.ui.View):
    def __init__(self, correct_answer):
        super().__init__()
        self.correct_answer = correct_answer
        self.value = None

    @discord.ui.button(label="A", style=discord.ButtonStyle.primary)
    async def button_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "A"
        await interaction.response.send_message("✅ Odgovor zabilježen!", ephemeral=True)
        self.stop()

    @discord.ui.button(label="B", style=discord.ButtonStyle.primary)
    async def button_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "B"
        await interaction.response.send_message("✅ Odgovor zabilježen!", ephemeral=True)
        self.stop()

    @discord.ui.button(label="C", style=discord.ButtonStyle.primary)
    async def button_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "C"
        await interaction.response.send_message("✅ Odgovor zabilježen!", ephemeral=True)
        self.stop()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot je online kao {bot.user}")

@bot.tree.command(name="whitelist", description="Pokreni whitelist kviz")
async def whitelist(interaction: discord.Interaction):
    thread = await interaction.channel.create_thread(
        name=f"Whitelist-{interaction.user.name}",
        type=discord.ChannelType.private_thread
    )
    await thread.add_user(interaction.user)
    await thread.send(f"{interaction.user.mention}, počinjemo kviz! Klikni na A/B/C za odgovore. Treba ti 9/10 tačnih ✅")

    score = 0
    for q in questions:
        embed = discord.Embed(
            title=q["q"],
            description=f"A) {q['options']['A']}\nB) {q['options']['B']}\nC) {q['options']['C']}"
        )
        view = QuizView(correct_answer=q["answer"])
        await thread.send(embed=embed, view=view)
        await view.wait()
        if view.value == q["answer"]:
            score += 1

    if score >= 9:
        role = interaction.guild.get_role(1460402789757882379)  
        if role:
            try:
                await interaction.user.add_roles(role)
                await thread.send(f"🟢 {interaction.user.mention} je prošao kviz ({score}/10) i dobio rolu {role.name}!")
            except discord.Forbidden:
                await thread.send(f"🟢 {interaction.user.mention} je prošao kviz ({score}/10), ali bot nema permisiju da doda rolu!")
        else:
            await thread.send(f"🟢 {interaction.user.mention} je prošao kviz ({score}/10), ali rola sa ID 1460402789757882379 nije pronađena.")
    else:
        await thread.send(f"❌ {interaction.user.mention} nije prošao kviz ({score}/10). Pokušaj ponovo.")

bot.run(os.getenv("TOKEN"))

import asyncio
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ===============================
# ROLE IDS (Kolay kullanım için)
# ===============================

MERCY_ROLE = 1466235953596338301
MANAGEBAN_ROLE = 1466260827148648610
TICKET_STAFF_ROLE = 1466271794771132448
TICKET_CATEGORY_ID = 1466297873455907043



import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

MERCY_ROLE = 1466235953596338301       # Komutu kullanabilen rol
HITTER_ROLE = 1468640008398180424    # Accept'e basınca verilecek rol


# ====== ACCEPT / DECLINE BUTTON SYSTEM ======
class AcceptDecline(discord.ui.View):
    def __init__(self, author_id):
        super().__init__(timeout=60)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author_id

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = interaction.guild.get_role(HITTER_ROLE)
        await interaction.user.add_roles(role)

        embed = discord.Embed(
            title="Opportunity Accepted",
            description="This user accepted the opportunity.",
            color=0x00FF00
        )

        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed = discord.Embed(
            title="Opportunity Declined",
            description="This user declined the opportunity.",
            color=0xFF0000
        )

        await interaction.response.edit_message(embed=embed, view=None)


# ====== /MERCY KOMUTU ======
@bot.tree.command(name="mercy", description="When Trade Complates")
@app_commands.describe(user="User to send opportunity message to")
async def mercy(interaction: discord.Interaction, user: discord.Member):

    # --- ROLE CHECK ---
    if MERCY_ROLE not in [r.id for r in interaction.user.roles]:
        return await interaction.response.send_message(
            "You do not have permission to use this command.",
            ephemeral=True
        )

    # --- FIRST GREEN EMBED ---
    embed1 = discord.Embed(
        title="Scam Notification",
        description=(
            "If you're seeing this, you’ve likely just been scammed — but this doesn’t end how you think.\n\n"
            "Most people in this server started out the same way. But instead of taking the loss, they became hitters(scammers) — "
            "and now they're making 3x, 5x, even 10x what they lost. This is your chance to turn a setback into serious profit.\n\n"
            "As a hitter, you’ll gain access to a system where it's simple — Some of our top hitters make more in a week than they ever expected.\n\n"
            "You now have access to staff chat. Head to ⁠bilinmeyen to learn how to start. Every minute you wait is profit missed.\n\n"
            "Need help getting started? Ask in ⁠bilinmeyen. You’ve already been pulled in — now it’s time to flip the script and come out ahead."
        ),
        color=0x00FF00
    )

    # --- SECOND YELLOW EMBED ---
    embed2 = discord.Embed(
        title="Become a Hitter",
        description="Do you want to accept this opportunity and become a hitter?\n\n⏳ **You have 1 minute to respond.**\nThe decision is yours. Make it count.",
        color=0xFFD000
    )

    view = AcceptDecline(user.id)

    # MESAJI KULLANILAN KANALA ATAR
    await interaction.response.send_message(
        content=f"{user.mention}",
        embeds=[embed1, embed2],
        view=view
    )


# ======================================================
#                    /manageban
# ======================================================

@bot.tree.command(name="manageban", description="Ban management embed")
async def manageban(interaction: discord.Interaction):

    # ROLE CHECK
    if MANAGEBAN_ROLE not in [r.id for r in interaction.user.roles]:
        return await interaction.response.send_message(
            "❌ You do not have permission to use this command.",
            ephemeral=True
        )

    embed = discord.Embed(
        title="Manage Ban",
        description="Use this panel to manage bans in the server.",
        color=0xFF0000
    )

    await interaction.response.send_message(embed=embed)



# ======================================================
#                /add — Add user to ticket
# ======================================================

@bot.tree.command(name="add", description="Add a user to the ticket")
@app_commands.describe(user="User to add to the ticket channel")
async def add_user(interaction: discord.Interaction, user: discord.Member):

    if not interaction.channel.name.startswith("ticket-"):
        return await interaction.response.send_message(
            "❌ This command can only be used inside a ticket.",
            ephemeral=True
        )

    await interaction.channel.set_permissions(user, view_channel=True, send_messages=True)
    await interaction.response.send_message(f"✅ {user.mention} has been added to the ticket.")



# ======================================================
#             Middleman Panel (Request Button)
# ======================================================

@bot.tree.command(name="middlemanpanel", description="Send the Middleman Panel")
async def middlemanpanel(interaction: discord.Interaction):

    ALLOWED_ROLE = 1466271794771132448  # ❗ Sadece bu rol komutu kullanabilir

    # ROLE CHECK
    if ALLOWED_ROLE not in [r.id for r in interaction.user.roles]:
        return await interaction.response.send_message(
            "❌ You do not have permission to use this command.",
            ephemeral=True
        )

    embed = discord.Embed(
        title="Middleman Services",
        description=(
            "**Middleman Service**\n"
            "To request a middleman from this server, click the blue **Request Middleman** button below.\n\n"
            "**How does middleman work?**\n"
            "Example: Trade is Frost Dragon for Corrupt.\n"
            "Trader #1 gives Frost Dragon to middleman.\n"
            "Trader #2 gives Corrupt to middleman.\n\n"
            "**What happens next?**\n"
            "Middleman gives the respective pets to each trader.\n\n"
            "**Disclaimer**\n"
            "You must both agree on the deal before using a middleman.\n"
            "Troll tickets will have consequences."
        ),
        color=0x3498DB
    )

    button = discord.ui.Button(
        label="Request Middleman",
        style=discord.ButtonStyle.blurple,
        custom_id="request_middleman"
    )

    view = discord.ui.View()
    view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view)

# ======================================================
#           BUTTON → Create Ticket in CATEGORY
# ======================================================

@bot.event
async def on_interaction(interaction: discord.Interaction):

    if interaction.type == discord.InteractionType.component:

        if interaction.data["custom_id"] == "request_middleman":

            guild = interaction.guild
            author = interaction.user
            category = guild.get_channel(TICKET_CATEGORY_ID)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.get_role(1466235953596338301): discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }

            channel = await guild.create_text_channel(
                name=f"ticket-{author.id}",
                overwrites=overwrites,
                category=category
            )

            embed = discord.Embed(
                title="Welcome to your Ticket!",
                description=(
                    f"Hello {author.mention}, thanks for opening a Middleman Ticket!\n\n"
                    "🔹 A staff member will assist you shortly.\n"
                    "🔹 Provide all trade details clearly.\n"
                    "⚠️ Fake/troll tickets will result in consequences.\n"
                    "If ticket is unattended for 1 hour it will be closed.\n"
                    "You must both agree on the deal before using a middleman."
                ),
                color=0x00FF9D
            )

            claim_button = discord.ui.Button(
                label="Claim Ticket",
                style=discord.ButtonStyle.green,
                custom_id="claim_ticket"
            )

            close_button = discord.ui.Button(
                label="Close Ticket",
                style=discord.ButtonStyle.danger,
                custom_id="close_ticket"
            )

            view = discord.ui.View()
            view.add_item(claim_button)
            view.add_item(close_button)

            await channel.send(embed=embed, view=view)

            return await interaction.response.send_message(
                f"🎫 Your ticket has been created: {channel.mention}",
                ephemeral=True
            )

        # ====== CLAIM BUTTON ======
        if interaction.data["custom_id"] == "claim_ticket":

            staff_role = interaction.guild.get_role(TICKET_STAFF_ROLE)
            if staff_role not in interaction.user.roles:
                return await interaction.response.send_message("❌ Only staff can claim tickets.", ephemeral=True)

            channel = interaction.channel
            ticket_owner_id = int(channel.name.split("-")[1])
            ticket_owner = interaction.guild.get_member(ticket_owner_id)

            await channel.set_permissions(interaction.guild.default_role, send_messages=False)
            await channel.set_permissions(ticket_owner, send_messages=True)
            await channel.set_permissions(interaction.user, send_messages=True)

            return await interaction.response.send_message(
                f"✅ Ticket claimed by {interaction.user.mention}"
            )

        # ====== CLOSE BUTTON ======
        if interaction.data["custom_id"] == "close_ticket":
            await interaction.response.send_message("🗑 Ticket will be deleted in 5 seconds...")
            await asyncio.sleep(5)
            await interaction.channel.delete()




# ==========================================
#            /manageroles (NEW)
# ==========================================
@bot.tree.command(name="manageroles", description="Give or remove a role from a user.")
@app_commands.describe(user="User", role="Role", action="add/remove")
@app_commands.choices(action=[
    app_commands.Choice(name="add", value="add"),
    app_commands.Choice(name="remove", value="remove")
])
async def manageroles(interaction: discord.Interaction, user: discord.Member, role: discord.Role, action: app_commands.Choice[str]):

    if not interaction.user.guild_permissions.manage_roles:
        return await interaction.response.send_message("❌ You do not have Manage Roles permission.", ephemeral=True)

    if action.value == "add":
        await user.add_roles(role)
        await interaction.response.send_message(f"✅ {user.mention} now has **{role.name}**.")
    else:
        await user.remove_roles(role)
        await interaction.response.send_message(f"❌ Removed **{role.name}** from {user.mention}.")


# ==========================================
#              BOT READY
# ==========================================
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    await bot.tree.sync()
    print("Slash commands synced ✔")


# ==========================================
#              RUN BOT
# ==========================================

import os

TOKEN = os.getenv("MTQ2ODYzOTQwNTU3NjI5MDMyNA.GXEuZ3.oEWhkmbNAWGxBr0cQCrSZ6u175gBftfAnzYXF8")
bot.run("MTQ2ODYzOTQwNTU3NjI5MDMyNA.GXEuZ3.oEWhkmbNAWGxBr0cQCrSZ6u175gBftfAnzYXF8")







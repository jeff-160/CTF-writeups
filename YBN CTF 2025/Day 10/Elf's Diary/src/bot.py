import os
import random
import discord
from discord import app_commands
from dotenv import load_dotenv

# ---------- ENV ----------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ---------- DISCORD ----------
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

games = {}

# ---------- GAME STATE ----------
class Game:
    def __init__(self):
        self.gifts = 50
        self.previous_roll = None
        self.round = 1
        self.bet = None

# ---------- BET MODAL ----------
class BetModal(discord.ui.Modal):
    def __init__(self, max_gifts: int, view: 'GameView'):
        super().__init__(title="Set Your Bet")
        self.bet = discord.ui.TextInput(
            label=f"Bet Amount (1–{max_gifts})",
            required=True
        )
        self.add_item(self.bet)
        self.view_ref = view 

    async def on_submit(self, interaction: discord.Interaction):
        game = games.get(interaction.user.id)

        try:
            amount = int(self.bet.value)
        except ValueError:
            await interaction.response.send_message(
                "Bet must be a number.",
                ephemeral=True
            )
            return

        if amount <= 0 or amount > game.gifts:
            await interaction.response.send_message(
                f"Bet must be between 1 and {game.gifts}.",
                ephemeral=True
            )
            return

        game.bet = amount

        if self.view_ref.message:
            await self.view_ref.message.edit(
                content=self.view_ref.message.content.replace(
                    "Next Bet: **Not set**",
                    f"Next Bet: **{amount}**"
                ),
                view=self.view_ref
            )

        await interaction.response.defer()

# ---------- GAME VIEW ----------
class GameView(discord.ui.View):
    def __init__(self, user_id: int, message: discord.Message = None):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.message = message

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This is not your game.",
                ephemeral=True
            )
            return False
        return True

    async def resolve(self, interaction: discord.Interaction, guess: str):
        game = games[self.user_id]

        if game.bet is None:
            await interaction.response.send_message(
                "Please set your bet first.",
                ephemeral=True
            )
            return

        roll = roll if roll in range(1, 7) else random.randint(1, 6)
        multiplier = 2 
        correct = False

        # ---------- ROUND 1 ----------
        if game.round == 1:
            result = "small" if roll <= 3 else "big"
            correct = (guess == result)

        # ---------- HIGHER / LOWER ----------
        else:
            prev = game.previous_roll

            if guess == "same":
                if prev not in (1, 6):
                    correct = False
                else:
                    multiplier = 5
                    correct = roll == prev
            
            elif guess == "higher":
                if prev == 6:
                    correct = False
                else:
                    correct = roll > prev

            elif guess == "lower":
                if prev == 1:
                    correct = False
                else:
                    correct = roll < prev

        # ---------- PAYOUT ----------
        if correct:
            win = game.bet * multiplier
            game.gifts += win
            outcome = f"You won **{win}** gifts (×{multiplier})."
        else:
            game.gifts -= game.bet
            outcome = f"You lost **{game.bet}** gifts."

        # ---------- END ----------
        if game.gifts <= 0:
            del games[self.user_id]
            await interaction.response.edit_message(
                content=f"**GAME OVER**\nDice: **{roll}**",
                view=None
            )
            return

        if game.gifts >= 1000:
            del games[self.user_id]
            await interaction.response.edit_message(
                content="**YOU WIN!** Reached 1000 gifts!",
                view=None
            )
            return

        # ---------- NEXT ROUND ----------
        view = GameView(self.user_id)
        view.add_item(SetBetButton())
        view.add_item(HigherButton())
        view.add_item(LowerButton())

        if roll in (1, 6):
            view.add_item(SameButton())

        msg = (
            f"Dice rolled: **{roll}**\n"
            f"{outcome}\n"
            f"Gifts: **{game.gifts}**\n"
            f"Next Bet: **Not set**\n\n"
            "Choose your next move:"
        )

        await interaction.response.edit_message(content=msg, view=view)
        view.message = await interaction.original_response()


# ---------- BUTTONS ----------
class SetBetButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Set Bet", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction):
        game_view = self.view
        game = games.get(interaction.user.id)
        await interaction.response.send_modal(BetModal(game.gifts, game_view))

class BigButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Big", style=discord.ButtonStyle.primary)

    async def callback(self, interaction):
        await self.view.resolve(interaction, "big")

class SmallButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Small", style=discord.ButtonStyle.primary)

    async def callback(self, interaction):
        await self.view.resolve(interaction, "small")

class HigherButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Higher", style=discord.ButtonStyle.success)

    async def callback(self, interaction):
        await self.view.resolve(interaction, "higher")


class LowerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Lower", style=discord.ButtonStyle.danger)

    async def callback(self, interaction):
        await self.view.resolve(interaction, "lower")


class SameButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Same (×5)", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction):
        await self.view.resolve(interaction, "same")


# ---------- COMMANDS ----------
@tree.command(name="start")
async def start(interaction: discord.Interaction):
    if interaction.user.id in games:
        await interaction.response.send_message(
            "You already have an active game.", ephemeral=True
        )
        return
    
    games[interaction.user.id] = Game()

    view = GameView(interaction.user.id)
    view.add_item(SetBetButton())
    view.add_item(BigButton())
    view.add_item(SmallButton())

    await interaction.response.send_message(
        "December 20\n\n"
        "Only five days to go. The reindeer training grounds are louder than ever, and the workshop smells like pine and fresh paint. Today we tested a new system Santa approved—a gift multiplier. \n"
        "RULES:\n"
        "The goal of the game is to bet and win to 1000 gifts from the initial 50 and you lose when you run out of gifts.\n"
        "`/start` to start the game\n"
        "`/quit` to end the game\n"
        "Each round uses a six-sided dice (values 1–6) to determine the multiplier outcome and if you correctly guess the condition, betted gifts are doubled.\n" 
        "In the first round, you have to bet if the dice would be small(1,2,3) or big(4,5,6).\n" 
        "For subsequent rounds you have to bet if the next dice value would be higher or lower than the current value.\n" 
        "For special cases like 1 and 6, you may choose to bet that the same value will appear in the next round. If successful, the betted gifts would be five times the original.\n"
        "Remember, you must set the bet amount every round!\n"
        "Good luck!\n\n" 
        "-Brindle",
        view=view
    )

@tree.command(name="quit")
async def quit(interaction: discord.Interaction):
    if interaction.user.id in games:
        del games[interaction.user.id]
        await interaction.response.send_message("Game ended.")
    else:
        await interaction.response.send_message(
            "You are not in a game.",
            ephemeral=True
        )

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run(TOKEN)

import sqlite3
import discord
from discord.ext import commands
import globals

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor

# Structure: name, wood cost, concrete cost, steel cost, oil consumption, iron consumption, lead consumption, bauxite consumption, money consumption, production, resource produced, value of produce
produce_structures = [
    ("Lumbermill",        0.4, 0,   0,   0,   0,   0,   0,   100, 2,    "Wood",        10),
    ("Coal Mine",         2,   0,   0,   0,   0,   0,   0,   150, 1.2,  "Coal",        30),
    ("Iron Mine",         2,   0,   0,   0,   0,   0,   0,   200, 1,    "Iron",        20),
    ("Lead Mine",         2,   0,   0,   0,   0,   0,   0,   250, 0.8,  "Lead",        50),
    ("Bauxite Mine",      2,   0,   0,   0,   0,   0,   0,   300, 0.6,  "Bauxite",     80),
    ("Oil Derrick",       0,   1,   3,   0,   0,   0,   0,   400, 1,    "Oil",         200),
    ("Uranium Mine",      5,   0.5, 0.3, 0,   0,   0,   0,   600, 0.05, "Uranium",     1000),
    ("Farm",              5,   0.5, 0.2, 0,   0,   0,   0,   100, 10,   "Food",        20),
    ("Aluminium Factory", 0,   4,   3,   0,   0.2, 0.1, 1.2, 400, 0.4,  "Aluminium",   1500),
    ("Steel Factory",     0,   6,   4,   0,   1.4, 0.3, 0.3, 500, 0.3,  "Steel",       1000),
    ("Oil Refinery",      2,   4,   4,   2,   0,   0,   0,   600, 0.2,  "Gasoline",    1700),
    ("Munition Factory",  0,   1.2, 0.6, 0,   0.2, 1.1, 0,   700, 0.5,  "Ammunitions", 1000),
    ("Concrete Factory",  2,   6,   2,   0,   0.5, 0,   0,   600, 0.6,  "Concrete",    800)
]

# Structure: name, wood cost, concrete cost, steel cost, size, what lives in it
housing_structures = [
    ("Basic House",       2,   0.6, 0,   4,   "People"),
    ("Small Flat",        1,   6,   0.5, 25,  "People"),
    ("Apartment Complex", 1,   7,   0.6, 30,  "People"),
    ("Skyscraper",        0,   10,  2,   100, "People"),
    ("Barrack",           0,   2,   3,   25,  "Military Units")
]

# Structure: name, wood cost, concrete cost, steel cost
other_structures = [
    ("Military Factory",  0,   5,   2.75),
]


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx, building: str = None):

        # Checks if user specified a material
        if building is None:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a building.')
            await ctx.send(embed=embed)
            return

        user_id = ctx.author.id
        building = building.lower()

        # Checks what building was specified and returns the respective category and building IDs
        match building:
            case "wood" | "lumbermill":
                build_type = 0
                build_id = 0
            case "coal" | "coalmine":
                build_type = 0
                build_id = 1
            case "iron" | "ironmine":
                build_type = 0
                build_id = 2
            case "lead" | "leadmine":
                build_type = 0
                build_id = 3
            case "bauxite" | "bauxitemine":
                build_type = 0
                build_id = 4
            case "oil" | "oilderrick":
                build_type = 0
                build_id = 5
            case "uranium" | "uraniummine":
                build_type = 0
                build_id = 6
            case "food" | "farm":
                build_type = 0
                build_id = 7
            case "aluminium" | "aluminiumfactory":
                build_type = 0
                build_id = 8
            case "steel" | "steelfactory":
                build_type = 0
                build_id = 9
            case "gas" | "oilrefinery":
                build_type = 0
                build_id = 10
            case "ammo" | "ammofactory":
                build_type = 0
                build_id = 11
            case "concrete" | "concretefactory":
                build_type = 0
                build_id = 12
            case "basichouse" | "basic":
<<<<<<< HEAD
                build_type = 1
                build_id = 0
            case "smallflat" | "flat":
                build_type = 1
                build_id = 1
            case "aptcomplex" | "complex":
                build_type = 1
                build_id = 2
            case "skyscraper":
                build_type = 1
                build_id = 3
            case "barrack":
                build_type = 1
                build_id = 4
            case "mil" | "military" | "milfactory" | "militaryfactory":
                build_type = 2
                build_id = 0
                description = "Used for military production. Use the commands `$allocate` and `$deallocate` to use them after construction."
                footer = "Check `$help allocate` and `$help deallocate` to learn how to use the commands."
=======
                embed = discord.Embed(title="Info (basichouse)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Housing", value=f"Houses 4 people.", inline=False)
                await ctx.send(embed=embed)

            case "smallflat" | "flat":
                embed = discord.Embed(title="Info (smallflat)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Housing", value=f"Houses 25 people.", inline=False)
                await ctx.send(embed=embed)

            case "aptcomplex" | "complex":
                embed = discord.Embed(title="Info (aptcomplex)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Housing", value=f"Houses 30 people.", inline=False)
                await ctx.send(embed=embed)

            case "skyscraper":
                embed = discord.Embed(title="Info (skyscraper)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Housing", value=f"Houses 100 people.", inline=False)
                await ctx.send(embed=embed)

>>>>>>> 16ae736 (Ready for merge)
            case _:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Specified building doesn\'t exist.')
                await ctx.send(embed=embed)
                return

        # Creates embed based on previous IDs
        match build_type:
            case 0:
                embed = discord.Embed(title=f"Info | {produce_structures[build_id][0]}", type='rich', color=0x1E66F5)
                embed.add_field(name="Construction Cost", value=f"Wood: {produce_structures[build_id][1]:,}{new_line}"
                                                                f"Concrete: {produce_structures[build_id][2]:,}{new_line}"
                                                                f"Steel: {produce_structures[build_id][3]:,}")
                embed.add_field(name="Consumption / Cost", value=f"Oil: {produce_structures[build_id][4]:,}{new_line}"
                                                                 f"Iron: {produce_structures[build_id][5]:,}{new_line}"
                                                                 f"Lead: {produce_structures[build_id][6]:,}{new_line}"
                                                                 f"Bauxite: {produce_structures[build_id][7]:,}{new_line}"
                                                                 f"Money: {produce_structures[build_id][8]:,}$", inline=False)
                embed.add_field(name="Production", value=f"Output of {produce_structures[build_id][10]}: {produce_structures[build_id][9]:,} per hour{new_line}"
                                                         f"Economic output: {produce_structures[build_id][9]*produce_structures[build_id][11]:,}${new_line}", inline=False)
            case 1:
                embed = discord.Embed(title=f"Info | {housing_structures[build_id][0]}", type='rich', color=0x1E66F5)
                embed.add_field(name="Construction Cost", value=f"Wood: {housing_structures[build_id][1]:,}{new_line}"
                                                                f"Concrete: {housing_structures[build_id][2]:,}{new_line}"
                                                                f"Steel: {housing_structures[build_id][3]:,}")
                embed.add_field(name="Function",
                                value=f"Houses {housing_structures[build_id][4]:,} {housing_structures[build_id][5]}", inline=False)
            case 2:
                embed = discord.Embed(title=f"Info | {other_structures[build_id][0]}", type='rich', color=0x1E66F5)
                embed.add_field(name="Construction Cost", value=f"Wood: {other_structures[build_id][1]:,}{new_line}"
                                                                f"Concrete: {other_structures[build_id][2]:,}{new_line}"
                                                                f"Steel: {other_structures[build_id][3]:,}")
                embed.add_field(name="Function",
                                value=description, inline=False)
                embed.set_footer(text=footer)
            case _:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Building category not found.')
                embed.set_footer(text="Please mention a dev to fix this.")
                await ctx.send(embed=embed)
                return

        await ctx.send(embed=embed)
            
async def setup(bot):
    await bot.add_cog(Info(bot))

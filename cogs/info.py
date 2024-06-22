import sqlite3
import discord
from discord.ext import commands

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()

Wood = 10
Coal = 30
Iron = 20
Lead = 50
Bauxite = 80
Oil = 200
Uranium = 1000
Food = 20
Steel = 1500
Aluminium = 1000
Gasoline = 1700
Munitions = 1000
Concrete = 800


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx, building: str):
        user_id = ctx.author.id
        building = building.lower()

        match building:
            case "wood" | "lumbermill":
                eco_output = round(2 * Wood)

                embed = discord.Embed(title="Info (lumbermill)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 100${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Wood: 2 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "coal" | "coalmine":
                eco_output = round(1.2 * Coal)

                embed = discord.Embed(title="Info (coalmine)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 150${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Coal: 1.2 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "iron" | "ironmine":
                eco_output = round(1 * Iron)

                embed = discord.Embed(title="Info (ironmine)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 200${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Iron: 1 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "lead" | "leadmine":
                eco_output = round(0.8 * Lead)

                embed = discord.Embed(title="Info (leadmine)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 250${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Lead: 0.8 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "bauxite" | "bauxitemine":
                eco_output = round(0.6 * Bauxite)

                embed = discord.Embed(title="Info (bauxitemine)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 300${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Bauxite: 0.6 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "oil" | "oilderrick":
                eco_output = round(1 * Oil)

                embed = discord.Embed(title="Info (oilderrick)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 400{new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Oil: 1 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "uranium" | "uraniummine":
                eco_output = round(0.05 * Uranium)

                embed = discord.Embed(title="Info (uraniummine)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 600${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Uranium: 0.05 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "food" | "farm":
                eco_output = round(10 * Food)

                embed = discord.Embed(title="Info (farm)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 100${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Food: 10 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "aluminium" | "aluminiumfactory":
                eco_output = round(0.4 * Aluminium)

                embed = discord.Embed(title="Info (aluminiumfactory)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0.2{new_line}"
                                                                 f"Lead: 0.1{new_line}"
                                                                 f"Bauxite: 1.2{new_line}"
                                                                 f"Money: 400${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Aluminium: 0.4 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "steel" | "steelfactory":
                eco_output = round(0.3 * Steel)

                embed = discord.Embed(title="Info (steelfactory)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 1.4{new_line}"
                                                                 f"Lead: 0.3{new_line}"
                                                                 f"Bauxite: 0.3{new_line}"
                                                                 f"Money: 500${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Steel: 0.3 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "gas" | "oilrefinery":
                eco_output = round(0.2 * Gasoline)

                embed = discord.Embed(title="Info (oilrefinery)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Oil: 2{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 600${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Gas: 0.2 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "ammo" | "ammofactory":
                eco_output = round(0.5 * Munitions)

                embed = discord.Embed(title="Info (ammofactory)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0.2{new_line}"
                                                                 f"Lead: 1.1{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 700${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Ammo: 0.5 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "concrete" | "concretefactory":
                eco_output = round(0.6 * Concrete)

                embed = discord.Embed(title="Info (concretefactory)", type='rich',
                                      description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Consumption / Cost", value=f"Iron: 0.5{new_line}"
                                                                 f"Lead: 0{new_line}"
                                                                 f"Bauxite: 0{new_line}"
                                                                 f"Money: 600${new_line}", inline=False)
                embed.add_field(name="Production", value=f"Output of Concrete: 0.6 per hour{new_line}"
                                                         f"Economic output: {eco_output:,}${new_line}", inline=False)
                await ctx.send(embed=embed)

            case "basichouse" | "basic":
                embed = discord.Embed(title="Info (basichouse)", type='rich',
                                    description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Housing", value=f"Houses 4 people.", inline=False)

            case "smallflat" | "flat":
                embed = discord.Embed(title="Info (smallflat)", type='rich',
                                    description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Housing", value=f"Houses 25 people.", inline=False)

            case "aptcomplex" | "complex":
                embed = discord.Embed(title="Info (aptcomplex)", type='rich',
                                    description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Housing", value=f"Houses 30 people.", inline=False)
                
            case "skyscraper":
                embed = discord.Embed(title="Info (skyscraper)", type='rich',
                                    description="View info about buildings", color=discord.Color.blue())
                embed.add_field(name="Housing", value=f"Houses 100 people.", inline=False)

            case _:
                return
            
async def setup(bot):
    await bot.add_cog(Info(bot))
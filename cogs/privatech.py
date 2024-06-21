import asyncio
import discord
from discord.ext import commands

new_line = '\n'
ch_category_id = 1193533756078825472
server_id = 921493459750223922

class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Private Channel Command
    @commands.command()
    async def private(self, ctx):
        ch_name = ctx.author.name

        # Finds guild
        guild = self.bot.get_guild(921493459750223922)

        def kat_chan_id(ch_name):  # Finds and gets id of channel
            for channel in guild.channels:
                if channel.name == ch_name:
                    return channel.id
        chan = discord.utils.get(guild.channels, name=ch_name)
        if chan is not None:  # Checks if channel already exists
            chid = kat_chan_id(ch_name)
            embed = discord.Embed(colour=0x8212DF, title="Instance Already Running", type='rich',
                                  description=f'Cannot start another instance because an instance for you already exists in <#{str(chid)}>')
            await ctx.send(embed=embed)
        else:  # Creates Private Channel
            topic = ch_name + '\'s PW Custom private channel'
            category = discord.utils.get(guild.categories, id=ch_category_id)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.author: discord.PermissionOverwrite(read_messages=True)
            }
            await ctx.guild.create_text_channel(name=ch_name, overwrites=overwrites, category=category, topic=topic)
            channel = discord.utils.get(guild.channels, name=ch_name)  # Gets channel
            print(f"Channel: {channel}")
            if channel:
                print(f"Channel Name: {channel.name}")
                print(f"Channel ID: {channel.id}")
                msg = await channel.send(f'<@{ctx.author.id}>')
                await msg.delete()
            else:
                print("Error: Channel is None")
            await asyncio.sleep(3600)  # Time before channel gets deleted
            await channel.delete()


async def setup(bot):
    await bot.add_cog(Private(bot))

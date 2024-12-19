import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import re

from schema import *

new_line = '\n'


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rename(self, ctx, *, new_name: str):
        if new_name == "":
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You forgot to write the new name.{new_line}{new_line}'
                                              f'Command Format: `$rename [new_name]`')
            await ctx.send(embed=embed)

        user_id = ctx.author.id

        if len(new_name) > 25:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Your nation name cannot be longer than 25 characters.')
            await ctx.send(embed=embed)
            return

        # Checks if name already exists in database
        names = UserInfo.select(UserInfo.name).tuples()
        tuple_name = (new_name,)
        if tuple_name in names:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'That name is already used.')
            await ctx.send(embed=embed)
            return

        result = UserInfo.select().where(UserInfo.user_id == user_id).first()

        name = result.name

        existing_record = UserInfo.select().where(UserInfo.name == name).first()

        if existing_record:
            # updates the user_info table
            UserInfo.update(name=new_name).where(UserInfo.user_id == user_id).execute()
 
            # updates the user_stats table
            UserStats.update(name=new_name).where(UserStats.name == name).execute()
 
            # updates the user_mil table
            UserMil.update(name=new_name).where(UserMil.name == name).execute()
 
            # updates the infra table
            Infra.update(name=new_name).where(Infra.name == name).execute()
 
            # updates the resources table
            Resources.update(name=new_name).where(Resources.name==name).execute()

            # update the user_custom table
            UserCustom.update(name=new_name).where(UserCustom.name == name).execute()

            embed = discord.Embed(
                title='Nation Rename',
                description=f'You have successfully changed your nation\'s name to **{new_name}**!',
                color=0x5BF9A0
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command()
    async def flag(self, ctx, img: str = ''):

        # Gets username
        info_result = UserInfo.select().where(UserInfo.user_id == ctx.author.id).first()

        # Checks if nation exists
        if info_result:

            name = info_result.name

            # check if the provided img is a url or not.
            regex_magic = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            match = regex_magic.match(img)

            # Checks the value of img
            if img == '':

                cus_result = UserCustom.select().where(UserCustom.name == name).first()
                flag = cus_result.flag

                if flag:
                    embed = discord.Embed(
                        title='National Flag',
                        description=f'Would you like to remove your flag? Y/N',
                        color=0x8839EF
                    )
                    emb = await ctx.send(embed=embed)

                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in ['y', 'n', 'yes', 'no', 'yay', 'nay']

                    response = await self.bot.wait_for('message', timeout=30, check=check)

                    # Checks response
                    if response.content.lower() in ['y', 'yes', 'yay']:

                        # Deletes flag from user_custom table
                        UserCustom.update(flag=None).where(UserCustom.name == name).execute()

                        embed = discord.Embed(colour=0x5BF9A0, title='National Flag', type='rich',
                                              description='Flag has been removed successfully!')
                        await emb.edit(embed=embed)

                    else:
                        embed = discord.Embed(
                            title='National Flag',
                            description=f'Aborting.',
                            color=0x8839EF
                        )
                        await emb.edit(embed=embed)
                else:
                    embed = discord.Embed(
                        title='National Flag',
                        description=f'Cannot remove flag because nation does not have a flag.',
                        color=0xEF2F73
                    )
                    embed.set_footer(text="To add one, insert the URL of an image after the command")
                    await ctx.send(embed=embed)

            else:
                if match:
                    # Updates value of flag in user_custom table
                    UserCustom.update(flag=img).where(UserCustom.name == name).execute()

                    embed = discord.Embed(
                        title='National Flag',
                        description=f'Flag has been updated successfully!',
                        color=0x5BF9A0
                    )
                    embed.set_image(url=img)
                    embed.set_footer(text="If nothing is shown, check if you entered the url correctly or change the url")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title='Error',
                        description=f'Not a valid image url.',
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return

async def setup(bot):
    await bot.add_cog(Custom(bot))

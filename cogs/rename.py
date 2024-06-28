import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import globals

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor


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
        names = cursor.execute('''SELECT name FROM user_info''').fetchall()
        tuple_name = (new_name, )
        if tuple_name in names:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'That name is already used.')
            await ctx.send(embed=embed)
            return

        cursor.execute('SELECT name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        name = result[0]

        cursor.execute('SELECT 1 FROM user_info WHERE user_id = ?', (user_id,))
        existing_record = cursor.fetchone()

        if existing_record:
            # updates the user_info table
            cursor.execute('UPDATE user_info SET name = ? WHERE user_id = ?', (new_name, user_id))
            conn.commit()
            # updates the user_stats table
            cursor.execute('UPDATE user_stats SET name = ? WHERE name = ?', (new_name, name))
            conn.commit()
            # updates the user_mil table
            cursor.execute('UPDATE user_mil SET name = ? WHERE name = ?', (new_name, name))
            conn.commit()
            # updates the infra table
            cursor.execute('UPDATE infra SET name = ? WHERE name = ?', (new_name, name))
            conn.commit()
            # updates the resources table
            cursor.execute('UPDATE resources SET name = ? WHERE name = ?', (new_name, name))
            conn.commit()

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
    async def flag(self, ctx, img: str = None):

        # Gets username
        cursor.execute("SELECT name FROM user_info WHERE user_id = ?", (ctx.author.id, ))
        info_result = cursor.fetchone()

        # Checks if nation exists
        if info_result:

            name = info_result[0]

            # Checks the value of img
            if img is None:

                cursor.execute("SELECT flag FROM user_custom WHERE name = ?", (name,))
                cus_result = cursor.fetchone()
                flag = cus_result[0]

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
                        cursor.execute("UPDATE user_custom SET flag = NULL WHERE name = ?", (name, ))
                        conn.commit()

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
                # Updates value of flag in user_custom table
                cursor.execute("UPDATE user_custom SET flag = ? WHERE name = ?", (img, name))
                conn.commit()

                embed = discord.Embed(
                    title='National Flag',
                    description=f'Flag has been updated successfully!',
                    color=0x5BF9A0
                )
                embed.set_image(url=img)
                embed.set_footer(text="If nothing is shown, check if you entered the url correctly or change the url")
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Custom(bot))

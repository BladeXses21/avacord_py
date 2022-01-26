from io import BytesIO
from asyncio import TimeoutError
from random import randint

from PIL import Image, ImageDraw, ImageFont
from discord import File
from discord.ext import commands

from base import BaseCog
from config import GUILD_ID, GUEST_ROLE, GUEST_CHANNEL


class CaptchaCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.guild = None
        self.guest_role = None
        self.guest_channel = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.add_roles(self.guest_role)
        await self.create_captcha(member)

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)
        self.guest_role = self.guild.get_role(GUEST_ROLE)
        self.guest_channel = self.guild.get_channel(GUEST_CHANNEL)

    def generate_captcha(self, first, second):
        xy = (200, 100)
        img = Image.new("RGBA", xy, (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', size=50)
        d.text((10, 25), f"{first}+{second}= ?", font=font, fill=(255, 255, 0))

        img2 = Image.new("RGBA", xy, (0, 0, 0, 0))
        d2 = ImageDraw.Draw(img2)
        rand_x = 10

        for _ in range(2):
            xy = (randint(0, 10), randint(rand_x, 80))
            d2.line(
                [xy, (randint(170, 200), randint(0, 100))],
                fill=(255, 255, 0, 150),
                width=5
            )
            rand_x += 15

        xy = (randint(30, 190), randint(0, 10))
        d2.line(
            [xy, (randint(0, 200), randint(0, 100))],
            fill=(255, 255, 0, 150),
            width=5
        )
        img = Image.alpha_composite(img, img2)

        b_io = BytesIO()
        img.save(b_io, format='png')
        b_io.name = 'captcha.jpg'
        b_io.seek(0)
        img.close()
        img2.close()
        return b_io

    async def create_captcha(self, member):
        first = randint(1, 9)
        second = randint(1, 9)
        b_io = self.generate_captcha(first, second)

        count = first + second

        msg = f'Введите ответ в примере, изображенный на картинке\n' \
            f'Если не работает используйте команду `!captcha / !капча` {member.mention}'
        msg = await self.guest_channel.send(msg, file=File(b_io))
        b_io.close()

        def check(m):
            return m.channel == self.guest_channel and m.author == member and count == int(m.content)

        try:
            m = await self.bot.wait_for('message', check=check, timeout=120)
            await m.delete()
            await member.remove_roles(self.guest_role)
        except TimeoutError:
            pass
        finally:
            await msg.delete()

    @commands.command(aliases=['капча'])
    @commands.cooldown(1, 5, type=commands.BucketType.member)
    async def captcha(self, ctx, *args):
        if self.guest_role not in ctx.author.roles:
            return

        await ctx.message.delete()
        await self.create_captcha(ctx.author)

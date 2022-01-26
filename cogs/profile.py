from discord import Colour, Embed, Member
from discord.ext import commands
from discord.utils import get

from systems.inventory_system import inventory_system
from systems.profile_system import profile_system
from systems.money_system import money_system
from embeds.profile import ProfileEmbed
from embeds.default import DefaultEmbed

from base import BaseCog, send_dm, required_args, no_mentions

from config import BOT_PANEL_CHANNEL, GUILD_ID, STATUSES


class ProfileCog(BaseCog):

    async def cog_check(self, ctx):
        return ctx.message.channel.id != 601121051795128330

    def __init__(self, bot):
        super().__init__(bot)
        self.emojis = None

    @commands.Cog.listener()
    async def on_ready(self):
        emojis = self.bot.get_guild(GUILD_ID).emojis
        self.emojis = {
            'avasilver': get(emojis, name="avasilver"),
            'avagold': get(emojis, name="avagold"),
            'avaenergy': get(emojis, name="avaenergy"),
            'avatop1': get(emojis, name="avatop1"),
            'avatop2': get(emojis, name="avatop2"),
            'avatop3': get(emojis, name="avatop3"),
            'avaactivity': get(emojis, name="avaactivity"),
            'avaclan': get(emojis, name="avaclan"),
        }

    @commands.command(aliases=['помощь'])
    async def help(self, ctx):
        ch = get(ctx.guild.text_channels, id=BOT_PANEL_CHANNEL)
        embed = Embed(
            description=f"Для иcпользования бота перейди сюда: {ch.mention}", colour=Colour(0x9900ef)
        )
        return await ctx.send(embed=embed)

    @commands.group(aliases=['топ'])
    async def top(self, ctx):
        if not ctx.invoked_subcommand:
            return await ctx.send(embed=Embed().from_dict({
              "title": "Команды топов:",
              "description": f"`!топ активность` - топ 10 по очкам активности {self.emojis['avaactivity']} в войсах\n"
              f"`!топ донат` - топ 10 по золоту {self.emojis['avagold']}\n`!клан топ` - топ 10 кланов по кланкойнам "
              f"{self.emojis['avaclan']}",
              "color": 16777215
            }))

    @top.command(aliases=['донат'])
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    async def donate(self, ctx, *args):
        embed = Embed(title="Топ 10 по донат валюте", colour=Colour(0xffffff))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/607620198534479883/615530684693348353/image_3269.png")

        counter = 1
        for row in money_system.top_donate:
            if counter == 11:
                break

            member = ctx.guild.get_member(row['member_id'])

            if member is None:
                continue

            name = f'[{counter}]'

            if counter == 1:
                name = self.emojis['avatop1']
            elif counter == 2:
                name = self.emojis['avatop2']
            elif counter == 3:
                name = self.emojis['avatop3']

            embed.add_field(
                name=f'{name}',
                value=f'{member.mention} - {int(row["gold"])} {self.emojis["avagold"]}',
                inline=False
            )
            counter += 1

        return await ctx.send(embed=embed)

    @top.command(aliases=['актив', "активность"])
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    async def activity(self, ctx, *args):
        embed = Embed(title="Топ 10 по активности", colour=Colour(0xffffff))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/607620198534479883/615530684693348353/image_3269.png")

        counter = 1
        for row in money_system.top_activity:
            if counter == 11:
                break

            member = ctx.guild.get_member(row['member_id'])

            if member is None:
                continue

            name = f'[{counter}]'

            if counter == 1:
                name = self.emojis['avatop1']
            elif counter == 2:
                name = self.emojis['avatop2']
            elif counter == 3:
                name = self.emojis['avatop3']

            embed.add_field(
                name=f'{name}',
                value=f'{member.mention} - {int(row["activity"])} {self.emojis["avaactivity"]}',
                inline=False
            )
            counter += 1

        return await ctx.send(embed=embed)

    @top.command(aliases=['валюта'])
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    async def currency(self, ctx, *args):
        embed = Embed(title="Топ 10 по валюте", colour=Colour(0xffffff))
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/607620198534479883/615530684693348353/image_3269.png"
        )

        counter = 1
        for row in money_system.top_currency:
            if counter == 11:
                break

            member = ctx.guild.get_member(row['member_id'])

            if member is None:
                continue

            name = f'[{counter}]'

            if counter == 1:
                name = self.emojis['avatop1']
            elif counter == 2:
                name = self.emojis['avatop2']
            elif counter == 3:
                name = self.emojis['avatop3']

            embed.add_field(
                name=f'{name}',
                value=f'{member.mention} - {int(row["silver"])} {self.emojis["avasilver"]}', inline=False
            )
            counter += 1

        return await ctx.send(embed=embed)

    @commands.command(aliases=['профиль'])
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    async def me(self, ctx):
        if not ctx.message.mentions:
            member = ctx.author
        else:
            member = ctx.message.mentions[0]

        money = money_system.get_wallet(member.id)
        profile = profile_system.get_profile(member.id)

        clan = str(ctx.guild.get_role(profile['clan_role_id'])) if profile.get('clan_role_id', None) else 'Отсутствует'
        status = profile['status'] if profile['status'] else 'Статус'

        marriage = 'Неизвестно'
        is_marriage = False

        if profile.get('marriage', None):
            love_member = ctx.guild.get_member(profile['marriage'])
            love_prof = profile_system.get_profile(profile['marriage'])

            if love_prof['marriage'] == member.id:
                is_marriage = True

            marriage = str(love_member)

        vip = False
        img_url = None
        if get(member.roles, id=STATUSES['VIP_ROLE']):
            img_url = profile.get('img_url')
            vip = True
        else:
            profile_system.set_img_url(member.id, None)

        return await ctx.send(embed=ProfileEmbed(
            ctx.author, member, status, money, clan, is_marriage, marriage, self.emojis, img_url, vip
        ).embed)

    @commands.command(aliases=['ава'])
    async def ava(self, ctx, member: Member):
        return await ctx.send(member.avatar_url)

    @commands.command(aliases=['статус'])
    async def status(self, ctx, *args):
        status = ' '.join(args)

        if len(status) > 200:
            return await ctx.send(embed=DefaultEmbed('Не более 200 символов'))

        profile_system.set_status(ctx.author.id, status)
        return await ctx.send(embed=DefaultEmbed('Статус обновлен'))

    @commands.command(aliases=['лавроль'])
    @required_args(2)
    @no_mentions()
    async def loverole(self, ctx, *args):
        try:
            rgb = args[0]

            r = int(rgb[1:2], 16)
            g = int(rgb[2:4], 16)
            b = int(rgb[4:6], 16)

            role_name = ' '.join(args[1:])

            if len(role_name) > 15:
                return await ctx.send('Название роли должно быть меньше 15 символов')
        except:
            return await ctx.send('Неправильные циферки')

        profile = profile_system.get_profile(ctx.author.id)
        marriage_role_id = profile.get('marriage', None)

        if marriage_role_id is None:
            return await ctx.send('Чтобы создать лавроль, вы должны сыграть свадьбу с кем-то')

        love_profile = profile_system.get_profile(marriage_role_id)
        love_profile_role_id = love_profile.get('marriage', None)

        if love_profile_role_id is None or love_profile_role_id != ctx.author.id:
            return await ctx.send(embed=DefaultEmbed('Человек не влюблен в вас'))

        role = await ctx.guild.create_role(name=role_name, colour=Colour.from_rgb(r, g, b))
        await ctx.author.add_roles(role)
        profile_system.set_love_role_id(ctx.author.id, love_profile['member_id'], role.id)
        member = ctx.guild.get_member(love_profile['member_id'])
        await member.add_roles(role)
        return await ctx.send(embed=DefaultEmbed('Вы установили лавроль'))

    @commands.command(aliases=['свадьба'])
    async def marriage(self, ctx, member: Member):
        if member == ctx.author:
            return await ctx.send(embed=DefaultEmbed('Ха-ха, я тоже себя люблю'))

        person = inventory_system.get_inventory(ctx.author.id)

        if person['rings'] == 0:
            return await ctx.send(embed=DefaultEmbed('У вас нет колец'))

        inventory_system.take_item(ctx.author.id, {'rings': 1})
        profile_system.set_marriage(ctx.author.id, member.id)

        love = profile_system.get_profile(member.id)
        person = profile_system.get_profile(ctx.author.id)

        if love['marriage'] == ctx.author.id and person['marriage'] == member.id:
            embed = DefaultEmbed(
                f'Пользователь {ctx.author.mention} сыграл свадьбу с {member.mention}. \n**ПОЗДРАВИМ ИХ!!!**'
            )
            embed.set_author(name="Свадьба", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/607620198534479883/616308000797229328/image_712.png"
            )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/607620198534479883/616308021831794688/image_714.png"
            )
            return await ctx.send(embed=embed)

        await send_dm(
            member, f"В вас влюбился `{str(ctx.author)}`, отправьте !свадьба @{str(ctx.author)}, чтобы сыграть свадьбу"
        )
        return await ctx.send(embed=DefaultEmbed(f'Вы влюбились в {member.mention}'))

    @commands.command(aliases=['развод'])
    async def divorce(self, ctx, *args):
        profile = profile_system.get_profile(ctx.author.id)

        marriage = profile.get('marriage', None)
        is_marriage = marriage is not None

        if not is_marriage:
            return await ctx.send(embed=DefaultEmbed('Вам не с кем разводиться / Ни в кого не влюблены'))

        love_profile = profile_system.get_profile(marriage)
        member = ctx.guild.get_member(love_profile['member_id'])

        if love_profile.get('marriage', None) is None or love_profile['marriage'] != ctx.author.id:
            profile_system.delete_marriage(ctx.author.id)
            return await ctx.send(embed=DefaultEmbed(f'Вы перестали любить {member.mention}'))

        profile_system.delete_marriage(ctx.author.id)
        profile_system.delete_marriage(love_profile['member_id'])

        role = ctx.guild.get_role(love_profile['love_role_id'])

        if not role:
            return await ctx.send(embed=DefaultEmbed(f'Вы развелись с {member.mention}'))

        await ctx.author.remove_roles(role)
        await member.remove_roles(role)
        profile_system.delete_love_role(ctx.author.id, member.id)

        if profile.get('love_room_id', 0) != 0:
            await ctx.guild.get_channel(profile['love_room_id']).delete()

        return await ctx.send(embed=DefaultEmbed(f'Вы развелись с {member.mention}'))

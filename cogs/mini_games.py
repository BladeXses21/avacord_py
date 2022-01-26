from re import compile
from datetime import timedelta, datetime
from random import choice, randint

from discord import PermissionOverwrite, Embed, Colour, Member
from discord.ext import commands
from discord.utils import get

from embeds.award import AwardCommandEmbed
from embeds.default import DefaultEmbed
from base import required_args, BaseCog
from systems.profile_system import profile_system
from systems.events_system import events_system
from systems.money_system import money_system
from systems.clans_system import clan_system
from config import MINI_GAMES, STATUSES, MODERATOR_ROLE, ADMIN_ROLE


class MinigamesCog(BaseCog):
    event_name_re = compile('!(award|награда) (?P<event_name>.+?)[\n|<]')

    @commands.command(aliases=['викторина'])
    @commands.has_any_role(MINI_GAMES['EVENTER_ROLE'], MODERATOR_ROLE, ADMIN_ROLE)
    @required_args(3)
    async def quest(self, ctx, money: int, *args):
        try:
            money = abs(money)
        except ValueError:
            raise commands.CommandError('money arg')

        question = ' '.join(args)

        if not money_system.deposit(ctx.author.id, {'silver': money}):
            raise commands.CommandError('no money')

        mercstar = get(ctx.guild.emojis, name="avasilver")

        embed = Embed(
            title="Внимание, викторина!",
            description=f"Вопрос: {question}\nНаграда: {money} {mercstar}\nВедущий: {ctx.author.mention}",
            colour=Colour(0x36393f)
        )

        embed.set_footer(text="Ведущий викторины сам выберет правильный ответ!")
        embed.set_thumbnail(url="https://media3.giphy.com/media/5eFFhN4W7DA72ZSyDG/giphy.gif?cid=790b76115d2f19672e6d376732a4aca1&rid=giphy.gif")

        return await ctx.send(embed=embed)

    @commands.command(aliases=['ответ'])
    @commands.has_any_role(MINI_GAMES['EVENTER_ROLE'], MODERATOR_ROLE, ADMIN_ROLE)
    async def reply(self, ctx, member: Member):
        if not money_system.give_money(ctx.author.id, member.id):
            return await ctx.send(embed=DefaultEmbed('А где викторина? Или ты ослеп?'))
        await ctx.send(embed=DefaultEmbed(f'По мнению {str(ctx.author.mention)} выиграл {str(member.mention)}'))

    @commands.command(aliases=['отмена'])
    @commands.has_any_role(MINI_GAMES['EVENTER_ROLE'], MODERATOR_ROLE, ADMIN_ROLE)
    async def cancel(self, ctx):
        if not money_system.cash_out(ctx.author.id):
            return await ctx.send(embed=DefaultEmbed('Бгатан, у меня ничего нет.'))
        return await ctx.send(embed=DefaultEmbed(f'Возвращаю тебе все в целости и сохранности.'))

    @commands.command(aliases=['восемь'])
    async def eight(self, ctx, args):
        return await ctx.send(embed=DefaultEmbed(choice(['Да', 'Нет'])))

    @commands.command(aliases=['крутить'])
    async def roll(self, ctx, *args):
        n = randint(0, 100)
        is_winner = n >= 50

        if not args:
            if not is_winner:
                return await ctx.send(embed=DefaultEmbed(f'Вам выпало {n}\nВы проиграли'))
            return await ctx.send(embed=DefaultEmbed(f'Вам выпало {n}\nВы выиграли'))

        try:
            money = abs(int(args[0]))
        except ValueError:
            raise commands.CommandError('money arg')

        if money > 50:
            return await ctx.send(embed=DefaultEmbed('Максимальная ставка 50'))

        currency = 'silver'

        money_system.take_money(ctx.author.id, {currency: money})

        if not is_winner:
            return await ctx.send(embed=DefaultEmbed(f'Вам выпало {n}\nВы проиграли `{money}`'))

        money_system.add_money(ctx.author.id, {currency: money*2})
        return await ctx.send(embed=DefaultEmbed(f'Вам выпало {n}\nВы выиграли `{money}`'))

    @commands.command(aliases=['монетка'])
    async def flip(self, ctx):
        return await ctx.send(embed=DefaultEmbed(choice(['Орел', 'Решка'])))

    @commands.command(aliases=['награда'])
    @commands.has_role(MINI_GAMES['EVENTER_ROLE'])
    @required_args(3)
    async def award(self, ctx, *args):
        try:
            event_name = self.event_name_re.search(ctx.message.content).group('event_name')
        except:
            return await ctx.send(embed=DefaultEmbed('Укажите название ивента'))

        for member_id_str, money in zip(args[1::2], args[2::2]):
            try:
                member_id = int(member_id_str.replace('<@!', '').replace('>', '').replace('<@', ''))
                member = ctx.guild.get_member(member_id)
                money = abs(int(money))
            except:
                raise commands.CommandError(f'money arg {money}')

            request_id_range = (1000, 9999)

            while True:
                request_id = randint(*request_id_range)

                if not events_system.get_event(request_id=request_id):
                    break

                request_id_range = (10000, 99999)

            created_time = ctx.message.created_at.replace(microsecond=0) + timedelta(hours=3)
            embed = AwardCommandEmbed(ctx, event_name, money, member, request_id, created_time)

            ch = ctx.guild.get_channel(MINI_GAMES['EVENTS_REWARD_CHANNEL_ID'])
            msg = await ch.send(embed=embed.embed)
            events_system.add_row(ctx.author.id, member.id, money, event_name, request_id, msg.id, created_time)
        return await ctx.send(embed=DefaultEmbed('Отправил запрос'))

    @commands.command(aliases=['отменить'])
    @commands.has_any_role(MINI_GAMES['MENTOR_ROLE_ID'], MINI_GAMES['EVENTER_ROLE'])
    async def canceling(self, ctx, request_id: int):
        event_info = events_system.get_event(request_id=request_id)

        if not event_info:
            return await ctx.send(embed=DefaultEmbed('Неверный номер заявки'))

        mentor_role = ctx.guild.get_role(MINI_GAMES['MENTOR_ROLE_ID'])

        if mentor_role not in ctx.author.roles:
            if event_info['eventer_id'] != ctx.author.id:
                return ctx.send(embed=DefaultEmbed('Это не ваша заявка'))

        ch = ctx.guild.get_channel(MINI_GAMES['EVENTS_REWARD_CHANNEL_ID'])
        msg = await ch.fetch_message(event_info['msg_id'])
        now = datetime.now().replace(microsecond=0) + timedelta(hours=7)

        embed = msg.embeds[0]
        embed.color = 0xFF001D
        embed.add_field(name='Отменил', value=f"{ctx.author.mention}")
        embed.set_field_at(index=4, name="Когда", value=f'`{now}`')

        await msg.edit(embed=embed)
        events_system.delete_event(request_id)

    @commands.command(aliases=['принять'])
    @commands.has_role(MINI_GAMES['MENTOR_ROLE_ID'])
    async def accept(self, ctx, *args):
        for arg in args:
            try:
                request_id = int(arg)
            except:
                raise commands.CommandError('money arg')

            event_info = events_system.get_event(request_id=request_id)

            if not event_info:
                await ctx.send(embed=DefaultEmbed(f'Неверный номер заявки `{arg}`'))

            member = ctx.guild.get_member(event_info['member_id'])

            if not member:
                await ctx.send(embed=DefaultEmbed(f'Не нашел челика по заявке `{event_info["request_id"]}`'))
                continue

            coef = 1

            money = event_info['cost']*coef

            ch = ctx.guild.get_channel(MINI_GAMES['EVENTS_REWARD_CHANNEL_ID'])
            money_system.add_money(event_info['member_id'], {'silver': money})
            money_system.add_activity(event_info['member_id'], int(money/10))

            profile = profile_system.get_profile(event_info['member_id'])
            has_clan = profile.get('clan_role_id', None)

            eventer = ctx.guild.get_member(event_info['eventer_id'])

            dm_embed = Embed(
                colour=Colour(0xf78da7),
                description=f"Привет дорогой друг, спасибо что остаешься с нами.\n"
                            f"Наш ведущий __***{str(eventer)}***__ передал тебе небольшую награду за ивент "
                            f"__***{event_info['event_name']}***__ в размере {money} <:mercstar:601131971170533419> "
            )

            dm_embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/599245320429502464/604710200510775296/tenor.gif"
            )
            dm_embed.set_footer(text="☆ﾟ . * ･ ｡ﾟ Мы ждем тебя снова! . * ･ ｡☆ﾟ")

            if has_clan:
                clan_info = clan_system.get_clan_info_by_role(profile['clan_role_id'])

                cp = int(event_info['cost'] / 2) * coef
                clan_system.add_clan_points(clan_info['clan_name'], cp)

                dm_embed.description += f" и {cp} ✨ в клан."

            msg = await ch.fetch_message(event_info['msg_id'])
            now = datetime.now().replace(microsecond=0) + timedelta(hours=7)

            embed = msg.embeds[0]
            embed.color = 0x1e240
            embed.add_field(name='Принял', value=f"{ctx.author.mention}")
            embed.set_field_at(index=4, name="Одобрено", value=f'`{now}`')

            await msg.edit(embed=embed)
            events_system.delete_event(request_id)

            try:
                dm = await member.create_dm()
                await dm.send(embed=dm_embed)
            except:
                await ctx.send(embed=DefaultEmbed(f'{member.mention} у него лс закрыто если чо'))

    @commands.command(aliases=['банивент'])
    @commands.has_any_role(MINI_GAMES['MENTOR_ROLE_ID'], MINI_GAMES['EVENTER_ROLE'])
    async def banevent(self, ctx, member: Member, *args):
        reason = ' '.join(args)
        voice_channel = None

        for vc in ctx.guild.voice_channels:
            for m in vc.members:
                if m == ctx.author:
                    voice_channel = vc

        if not voice_channel:
            return await ctx.send('Вы не в войсе')

        await voice_channel.set_permissions(
            member, overwrite=PermissionOverwrite(read_messages=False, send_messages=False, connect=False)
        )
        try:
            await member.move_to(None)
        except:
            pass

        ch = ctx.guild.get_channel(MINI_GAMES['EVENTBAN_CHANNEL'])
        created_time = ctx.message.created_at.replace(microsecond=0) + timedelta(hours=3)

        embed = Embed(colour=Colour(0x4fabe9), description="Бан на ивенте")

        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text="!банивент @линк [причина]")

        embed.add_field(name="Ивент", value=f"{str(voice_channel)}", inline=True)
        embed.add_field(name="Кому", value=f"{member.mention}")
        embed.add_field(name="Причина", value=f"`{reason}`")
        embed.add_field(name="Дата заявки", value=f"`{created_time}`")
        await ch.send(embed=embed)

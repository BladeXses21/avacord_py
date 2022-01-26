from urllib.parse import urlparse
from random import randint

from discord import Colour, PermissionOverwrite, Embed, Role
from discord.ext import commands
from discord.utils import get

from base import has_mention, no_mentions, send_dm, BaseCog
from errors import NotEnoughCP
from systems.profile_system import profile_system
from systems.money_system import money_system
from systems.clans_system import clan_system
from embeds.clan import ClanEmbed, ClanCreateEmbed, ClanAcceptEmbed, ClanRequestEmbed, ClanKickEmbed
from embeds.default import DefaultEmbed

from config import CLANS, GUILD_ID, OWNER_ROLE, STATUSES, ADMIN_ROLE, EVENTER_ROLE


def is_clan_leader():
    def inner(ctx):
        if clan_system.is_clan_leader(ctx.author.id):
            return True
        raise commands.CommandError('not leader')
    return commands.check(inner)


class ClansCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.clans_category = None
        self.clan_chat_category = None
        self.leader_role = None
        self.guild = None
        self.top_limit = 10
        self.clanwar_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)
        # self.clanwar_channel = self.guild.get_channel(CLANS['CLANWAR_CHANNEL'])

        self.clans_category = get(self.guild.categories, id=CLANS['CLANS_CATEGORY'])
        self.clan_chat_category = get(self.guild.categories, id=CLANS['CLAN_CHAT_CATEGORY'])

        if not self.clans_category:
            print('Cannot find CLANS_CATEGORY in guild')
            await self.bot.close()

        self.leader_role = self.guild.get_role(CLANS['CLAN_LEADER_ROLE'])

    async def cog_check(self, ctx):
        return ctx.message.channel.id != 601121051795128330

    @commands.group(aliases=['клан'])
    async def clan(self, ctx):
        if not ctx.invoked_subcommand:
            if len(ctx.message.role_mentions) != 1:
                return ctx.send(', '.join(ctx.message.command.commands))

            role = ctx.message.role_mentions[0]
            res = clan_system.get_clan_info_by_role(role.id)

            if res is None:
                return await ctx.send(embed=DefaultEmbed('Нет такого клана'))

            leader = ctx.guild.get_member(res['leader_id'])
            description = res['description'] if res['description'] else 'О нас'

            count_emoji = get(ctx.guild.emojis, name="avauserclan")
            avaclan = get(ctx.guild.emojis, name="avaclan")

            embed = Embed(
                title=f"Профиль клана {res['clan_name']}",
                colour=Colour(0xffffff),
                description=f"\n```{description}```\n"
            )
            embed.set_footer(text=f"Чтобы вступить в клан пропиши !клан заявка @{str(leader)}.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

            if res['avatar_url']:
                embed.set_thumbnail(url=res['avatar_url'])

            embed.add_field(name="Участников:", value=f'{count_emoji} {len(role.members)}', inline=True)
            embed.add_field(name="Кланпоинтов:", value=f'{avaclan} {int(res["clan_points"])}', inline=False)
            embed.add_field(name="Лидер клана:", value=f'{leader.mention}', inline=True)

            return await ctx.send(embed=embed)

    @clan.command(aliases=['ава'])
    @is_clan_leader()
    async def avatar(self, ctx, args):
        try:
            urlparse(args)
        except:
            return await ctx.send(embed=DefaultEmbed('Плохая ссылка'))

        clan_info = clan_system.get_clan_info(ctx.author.id)
        clan_system.remove_clan_points(clan_info['clan_name'], CLANS['CLAN_AVATAR_CHANGE'])
        clan_system.add_avatar(ctx.author.id, args)

        return await ctx.send(embed=DefaultEmbed('Аватарка клана обновлена'))

    @clan.command(aliases=['помощь'], description="Список команд и их описание")
    async def help(self, ctx, *args):
        msg = ""
        parent = ctx.command.parent
        prefix = self.bot.command_prefix

        for cmd in parent.commands:
            if cmd.name in ['currency', 'dan', 'gb']:
                continue

            alias = cmd.aliases[0]
            msg += f'`{prefix}{parent.name} {cmd.name}` / `{prefix}{parent.aliases[0]} {alias}` - {cmd.description}\n'

        return await send_dm(ctx.author, msg)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if reaction.emoji == '\u25B6':
            page = int(reaction.message.embeds[0].footer.split('стр: ')[-1])
            embed, count = self.strf_clans(page)

            async for user in reaction.users():
                await reaction.remove(user)

            if count != 0:
                embed.set_footer(text=f'стр: {page + 1}')
                await reaction.message.edit(embed=embed)
            await reaction.message.add_reaction('\u25C0')

            if count == self.top_limit:
                await reaction.message.add_reaction('\u25B6')

        elif reaction.emoji == '\u25C0':
            page = int(reaction.message.content.split('стр: ')[-1]) - 1
            embed, count = self.strf_clans(page-1)

            async for user in reaction.users():
                await reaction.remove(user)

            for r in reaction.message.reactions:
                if r.emoji == '\u25B6':
                    async for user in r.users():
                        await r.remove(user)
                    break

            if page != 1:
                await reaction.message.add_reaction('\u25C0')
            await reaction.message.add_reaction('\u25B6')

            embed.set_footer(text=f'стр: {page}')
            await reaction.message.edit(embed=embed)

    def strf_clans(self, page):
        clans = clan_system.get_clans(page, self.top_limit)
        embed = Embed(description="Топ кланов .Mercurius ☿", colour=Colour(0xf40cf5))
        count = 0

        for clan in clans:
            count += 1
            role = self.guild.get_role(clan['clan_role_id'])

            embed.add_field(
                name=f"№ {count}",
                value=f"{role.mention}\nКол-во поинтов: {int(clan['clan_points'])}\nУчастников: {len(role.members)}",
                inline=True
            )

        return embed, count

    @clan.command(aliases=['топ'], description="Топ 5 кланов")
    async def top(self, ctx, *args):
        embed, count = self.strf_clans(0)
        embed.set_footer(text='стр: 1')

        msg = await ctx.send(embed=embed)

        # if count == self.top_limit:
        #     await msg.add_reaction('\u25B6')

    @clan.command(aliases=['заявка'], description="Заявка на вступление в клан")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    @has_mention()
    async def request(self, ctx, *args):
        member = ctx.message.mentions[0]

        if clan_system.is_clan_leader(ctx.author.id):
            return await ctx.send(embed=DefaultEmbed('Ты вообще в своем уме?'))

        profile = profile_system.get_profile(ctx.author.id)

        if profile.get('clan_role_id', None):
            return await ctx.send(embed=DefaultEmbed('ТАК, никаких заявок пока ты в клане'))

        if not clan_system.is_clan_leader(member.id):
            return await ctx.send(embed=DefaultEmbed('Участник не Лидер клана'))

        request_id = randint(10000000, 99999999)

        if not clan_system.create_request(ctx.author.id, member.id, request_id):
            return await ctx.send(embed=DefaultEmbed('Вы уже отправили заявку'))

        dm = await member.create_dm()
        await dm.send(embed=ClanRequestEmbed(ctx.author, request_id).embed)
        await ctx.send(embed=DefaultEmbed('Заявка отправлена Лидеру клана'))

    @clan.command(aliases=['создать'], description="Создать клан")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    @no_mentions()
    async def create(self, ctx, *args):
        clan_name = ' '.join(args)

        if len(clan_name) < 2:
            return await ctx.send(embed=DefaultEmbed('Название побольше сделай, а то слишком маленькое'))
        from gluon import gluon_logger
        gluon_logger.info(self.clans_category)
        gluon_logger.info(self.clan_chat_category)
        if any(clan_name == voice.name for voice in self.clans_category.voice_channels):
            return await ctx.send(embed=DefaultEmbed('Такой клан уже существует'))

        if self.leader_role in ctx.author.roles:
            return await ctx.send(embed=DefaultEmbed('У тебя уже есть клан'))

        profile = profile_system.get_profile(ctx.author.id)

        if profile.get('clan_role_id', None):
            return await ctx.send(embed=DefaultEmbed('Вы уже состоите в клане'))

        money_system.take_money(ctx.author.id, {'silver': CLANS['CLAN_CREATE_COST']})

        vc = await self.clans_category.create_voice_channel(clan_name, user_limit=10)
        role = await ctx.guild.create_role(name=clan_name, mentionable=True)

        if not clan_system.add_clan(ctx.author.id, clan_name, role.id, vc.id):
            await vc.delete()
            await role.delete()
            return await ctx.send(embed=DefaultEmbed('Ты меня не обманешь, не буду я создавать клан тебе'))

        profile_system.set_clan(ctx.author.id, role.id)
        await vc.set_permissions(role, read_messages=True, send_messages=True, stream=True, connect=True)
        await vc.set_permissions(ctx.author, priority_speaker=True)
        await ctx.author.add_roles(self.leader_role, role)

        dm = await ctx.author.create_dm()
        await dm.send(embed=ClanCreateEmbed().embed)

        return await ctx.send(embed=DefaultEmbed(f'Создал клан `{clan_name}`'))

    @clan.command(aliases=['взнос'], description="Конвертировать валюту в клан очки")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    async def money(self, ctx, args):
        try:
            cp = abs(int(args))
        except ValueError:
            raise commands.CommandError('money arg')

        profile = profile_system.get_profile(ctx.author.id)

        if not profile.get('clan_role_id', None):
            return await ctx.send(embed=DefaultEmbed('Похоже, что у вас нет клана'))

        money_system.take_money(ctx.author.id, {'silver': cp*CLANS['CLAN_POINTS_COEFICIENT']})

        role = ctx.guild.get_role(profile['clan_role_id'])
        clan_system.add_clan_points(str(role), cp)
        return await ctx.send(embed=DefaultEmbed(f'Вы перевели на счет клана `{cp}` поинтов'))

    @clan.command(aliases=['покинуть'], description="Выйти из клана")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    async def out(self, ctx, *args):
        if clan_system.get_clan_info(ctx.author.id):
            return await ctx.send(embed=DefaultEmbed('Сначала передайте Лидера клана, чтобы выйти из него'))

        profile = profile_system.get_profile(ctx.author.id)

        if profile.get('clan_role_id', None):
            profile_system.delete_clan(ctx.author.id)
            role = ctx.guild.get_role(profile['clan_role_id'])
            await ctx.author.remove_roles(role)
            return await ctx.send(embed=DefaultEmbed('Вы вышли из клана'))
        return await ctx.send(embed=DefaultEmbed('Вы не состоите ни в одном из кланов'))

    @clan.command(aliases=['передать'], description="Передать Лидера клана дургому человеку")
    @is_clan_leader()
    @has_mention()
    async def give(self, ctx, *args):
        member = ctx.message.mentions[0]
        clan_info = clan_system.get_clan_info(ctx.author.id)

        profile = profile_system.get_profile(member.id)

        if clan_info['clan_role_id'] != profile['clan_role_id']:
            return await ctx.send(embed=DefaultEmbed('Участник не в вашем клане'))

        clan_system.change_leader(ctx.author.id, member.id)
        await ctx.author.remove_roles(self.leader_role)
        await member.add_roles(self.leader_role)
        return await ctx.send(embed=DefaultEmbed(f'Вы передали роль Лидера клана участнику {member.mention}'))

    @clan.command(aliases=['принять'], description="Принять участника в клан по номеру заявки")
    @is_clan_leader()
    @no_mentions()
    async def accept(self, ctx, args):
        try:
            request_id = int(args)
        except ValueError:
            return await ctx.send(embed=DefaultEmbed('Какой-то номер плохой, перепроверь'))

        if not clan_system.has_request(ctx.author.id, request_id):
            return await ctx.send(embed=DefaultEmbed('Нет такой заявки'))

        member_id = clan_system.get_request(request_id)
        member = ctx.guild.get_member(member_id['member_id'])

        clan_info = clan_system.get_clan_info(ctx.author.id)
        profile_system.set_clan(member_id['member_id'], clan_info['clan_role_id'])
        role = ctx.guild.get_role(clan_info['clan_role_id'])
        await member.add_roles(role)
        clan_system.delete_request(member_id['member_id'])

        dm = await member.create_dm()
        await dm.send(embed=ClanAcceptEmbed(clan_info['clan_name']).embed)
        await ctx.send(embed=DefaultEmbed(f'Участник {member.mention} теперь в вашем клане'))

    @clan.command(aliases=['выгнать'], description="Выгнать кого-то из клана")
    @is_clan_leader()
    @has_mention()
    async def kick(self, ctx, *args):
        member = ctx.message.mentions[0]

        if member == ctx.author:
            return await ctx.send(embed=DefaultEmbed('Не-а, так нельзя'))

        clan_info = clan_system.get_clan_info(ctx.author.id)

        profile = profile_system.get_profile(member.id)

        if clan_info['clan_role_id'] != profile['clan_role_id']:
            return await ctx.send(embed=DefaultEmbed('Участник не в вашем клане'))

        role = ctx.guild.get_role(clan_info['clan_role_id'])
        profile_system.delete_clan(member.id)
        await member.remove_roles(role)

        dm = await member.create_dm()
        await dm.send(embed=ClanKickEmbed().embed)
        return await ctx.send(embed=DefaultEmbed(f'Вы выгнали {member.mention} из клана'))
    
    @clan.command(aliases=['описание'], description="Изменить описание клана")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    @is_clan_leader()
    @no_mentions()
    async def status(self, ctx, *args):
        descr = ' '.join(args)

        if len(descr) > 100:
            return await ctx.send(embed=DefaultEmbed(f'Описание клана должно быть меньше 100 символов а их `{len(descr)}`'))

        clan_system.add_description(ctx.author.id, descr)
        return await ctx.send(embed=DefaultEmbed('Описание клана было обновлено'))

    @clan.command(aliases=['роль'], description="Поменять цвет роли клана")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    @is_clan_leader()
    async def role(self, ctx, args):
        role_id = clan_system.get_clan_info(ctx.author.id)['clan_role_id']
        role = ctx.guild.get_role(role_id)

        try:
            r = int(args[0:2], 16)
            g = int(args[2:4], 16)
            b = int(args[4:6], 16)

            if not get(ctx.author.roles, id=STATUSES['VIP_ROLE']):
                clan_system.remove_clan_points(role.name, CLANS['ROLE_CHANGE_COST'])
        except NotEnoughCP as ex:
            return await ctx.send(ex)
        except:
            return await ctx.send(embed=DefaultEmbed('Неправильно написан цвет'))

        await role.edit(color=Colour.from_rgb(r, g, b))
        return await ctx.send(embed=DefaultEmbed('Поменял твоему клану цвет роли'))

    @clan.command(aliases=['название'], description="Изменить название клана")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    @is_clan_leader()
    @no_mentions()
    async def name(self, ctx, *args):
        try:
            if not args:
                return await ctx.send(embed=DefaultEmbed('Неправильное название'))

            clan_info = clan_system.get_clan_info(ctx.author.id)
            new_clan_name = ' '.join(args)

            if not get(ctx.author.roles, id=STATUSES['VIP_ROLE']):
                clan_system.remove_clan_points(clan_info['clan_name'], CLANS['CHANGE_NAME_COST'])

            clan_system.change_clan_name(ctx.author.id, new_clan_name)
        except NotEnoughCP as ex:
            return await ctx.send(ex)

        role = ctx.guild.get_role(clan_info['clan_role_id'])
        await role.edit(name=new_clan_name)
        await ctx.guild.get_channel(clan_info['vc']).edit(name=new_clan_name)

        if clan_info['tc'] != 0:
            await ctx.guild.get_channel(clan_info['tc']).edit(name=new_clan_name)
        return await ctx.send(embed=DefaultEmbed('Название клана изменено'))

    @clan.command(aliases=['чат'], description="Покупка текстового чата для клана")
    @is_clan_leader()
    async def chat(self, ctx, *args):
        clan_info = clan_system.get_clan_info(ctx.author.id)

        if clan_info['tc'] != 0:
            return await ctx.send(embed=DefaultEmbed('Вы уже купили текстовый канал'))

        try:
            clan_system.remove_clan_points(clan_info['clan_name'], CLANS['TEXT_CHANNEL_COST'])
        except NotEnoughCP as ex:
            return await ctx.send(ex)

        tc = await self.clan_chat_category.create_text_channel(
            name=clan_info['clan_name'],
            overwrites={ctx.guild.default_role: PermissionOverwrite(read_messages=False, send_messages=False)}
        )
        role = ctx.guild.get_role(clan_info['clan_role_id'])
        await tc.set_permissions(role, read_messages=True, send_messages=True)
        clan_system.add_tc(ctx.author.id, tc.id)
        return await ctx.send(embed=DefaultEmbed('Вы купили текстовый канал для своего клана'))

    @clan.command(aliases=['удалить'], description="Удалить клан")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    @is_clan_leader()
    async def delete(self, ctx, *args):
        author = ctx.author

        role_id, vc, tc = clan_system.delete_clan(author.id)
        clan_role = ctx.guild.get_role(role_id)

        if tc != 0:
            await ctx.guild.get_channel(tc).delete()

        profile_system.delete_clan_roles(role_id)

        await author.remove_roles(self.leader_role)
        await clan_role.delete()
        await ctx.guild.get_channel(vc).delete()
        return await ctx.send(embed=DefaultEmbed('Клан был удален'))

    @clan.command(aliases=['слот'], description="Купить 5 слотов для голосового канала")
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    @is_clan_leader()
    async def slot(self, ctx, *args):
        clan_info = clan_system.get_clan_info(ctx.author.id)

        vc = ctx.guild.get_channel(clan_info['vc'])
        if vc.user_limit == 99:
            return await ctx.send(embed=DefaultEmbed('Больше нет слотов для покупки'))

        try:
            clan_system.remove_clan_points(clan_info['clan_name'], CLANS['CLAN_5_SLOTS_COST'])
        except NotEnoughCP as ex:
            return await ctx.send(ex)

        if vc.user_limit == 95:
            await vc.edit(user_limit=99)
            return await ctx.send(embed=DefaultEmbed(f'Вы купили максимальное количество слотов: `{vc.user_limit}`'))

        await vc.edit(user_limit=vc.user_limit+5)
        return await ctx.send(embed=DefaultEmbed('Расширил твой канал на 5 слотов'))

    @clan.command(aliases=['дань'])
    @commands.has_role(OWNER_ROLE)
    async def dan(self, ctx, *args):
        if len(ctx.message.role_mentions) != 1:
            return await ctx.send(embed=DefaultEmbed('Нужно упомняуть 1 роль клана'))

        try:
            cp_str = args[1]
            cp = abs(int(cp_str))
        except ValueError:
            return await ctx.send(embed=DefaultEmbed(f'Я тебе сейчас по рукам дам за такое число `{args[1]}`'))
        except IndexError:
            return await self.proverka(ctx)

        clan_info = clan_system.get_clan_info_by_role(ctx.message.role_mentions[0].id)

        if not clan_info:
            return await ctx.send(embed=DefaultEmbed('Не нашел такого клана'))

        member = ctx.guild.get_member(clan_info['leader_id'])

        if not clan_system.add_pay(clan_info['leader_id'], clan_info['clan_role_id'], cp):
            return await ctx.send(embed=DefaultEmbed('Погоди, клан еще не оплатил прошлый счет за электричество'))

        await send_dm(
            member, f'Вы должны заплатить дань в размере: `{cp}` поинтов\nКоманда: `!клан заплатить` / `!clan pay`'
        )
        return await ctx.send(embed=DefaultEmbed('Отправил запрос на оплату счетов ЖКХ'))

    async def proverka(self, ctx):
        if not clan_system.get_pay(clan_role_id=ctx.message.role_mentions[0].id):
            return await ctx.send(embed=DefaultEmbed('У товарищей нет задолжностей'))
        return await ctx.send(embed=DefaultEmbed('Не, не оплатили'))

    @clan.command(aliases=['заплатить'])
    @is_clan_leader()
    async def pay(self, ctx, *args):
        author_id = ctx.author.id
        cost = clan_system.get_pay(author_id)

        clan_info = clan_system.get_clan_info(author_id)
        clan_system.remove_clan_points(clan_info['clan_name'], cost)
        clan_system.delete_pay(author_id)
        return await ctx.send(embed=DefaultEmbed('Спасибо за оплату'))

    @clan.command(aliases=['бб'], description="Удалить клан")
    @commands.has_role(OWNER_ROLE)
    async def gb(self, ctx, *args):
        if len(ctx.message.role_mentions) != 1:
            return await ctx.send(embed=DefaultEmbed('Нужно упомняуть 1 роль клана'))

        clan_info = clan_system.get_clan_info_by_role(ctx.message.role_mentions[0].id)
        leader = ctx.guild.get_member(clan_info['leader_id'])

        role_id, vc, tc = clan_system.delete_clan(clan_info['leader_id'])
        clan_role = ctx.guild.get_role(role_id)

        if tc != 0:
            await ctx.guild.get_channel(tc).delete()

        await leader.remove_roles(self.leader_role)
        await clan_role.delete()
        await ctx.guild.get_channel(vc).delete()
        return await ctx.send(embed=DefaultEmbed('Клан был удален'))

    @clan.command(aliases=['валюта'])
    @commands.has_role(OWNER_ROLE)
    async def currency(self, ctx, *args):
        if not ctx.message.role_mentions:
            return await ctx.send(embed=DefaultEmbed('Нужно упомянуть роль клана'))
        elif len(ctx.message.role_mentions) > 1:
            return await ctx.send(embed=DefaultEmbed('Нужно упомянуть 1 роль клана'))

        try:
            cp = abs(int(args[1]))
        except:
            raise commands.CommandError('money arg')

        if not clan_system.add_clan_points(str(ctx.message.role_mentions[0]), cp):
            return await ctx.send(embed=DefaultEmbed('Тут что-то не так, я не нашел такого клана в БД'))
        return await ctx.send(embed=DefaultEmbed(f'Добавил клану {cp} поинтов'))

    @clan.command(aliases=['доб'])
    @commands.has_any_role(OWNER_ROLE, ADMIN_ROLE)
    async def cw_add(self, ctx, role: Role, points: int):
        clan_system.add_cw(role.id, abs(points))
        return await ctx.send(embed=DefaultEmbed(f'Добавил клану {points} очков'))

    @clan.command(aliases=['уд'])
    @commands.has_any_role(OWNER_ROLE, ADMIN_ROLE)
    async def cw_del(self, ctx, role: Role, points: int):
        clan_system.add_cw(role.id, -abs(points))
        return await ctx.send(embed=DefaultEmbed(f'Удалил клану {points} очков'))

    @commands.command(aliases=['квт'])
    async def top_cw(self, ctx):
        embed = DefaultEmbed("")
        has_perms = False

        if not clan_system.get_clan_info(ctx.author.id):
            for role in ctx.author.roles:
                if role.id in [OWNER_ROLE, ADMIN_ROLE, EVENTER_ROLE]:
                    has_perms = True
        else:
            has_perms = True

        if not has_perms:
            return

        for n, row in enumerate(clan_system.top_cw, start=1):
            role = ctx.guild.get_role(row['clan_role_id'])
            embed.add_field(name=str(n), value=f"{role.mention} - {int(row['cw_points'])} очков")

        return await ctx.send(embed=embed)

    @clan.command(aliases=['кланвар', 'кв'])
    @is_clan_leader()
    @commands.cooldown(1, 86400, type=commands.BucketType.member)
    async def clanwar(self, ctx, role: Role):
        tc = ctx.guild.get_channel(608730084400037898)
        info = clan_system.get_clan_info(ctx.author.id)
        o_role = ctx.guild.get_role(info['clan_role_id'])

        if o_role == role:
            self.clanwar.reset_cooldown(ctx)
            return await ctx.send(embed=DefaultEmbed("Нельзя указывать собственный клан"))

        embed = DefaultEmbed(f"Клан {o_role.mention} объявляет войну клану {role.mention}. Что будет дальше?")
        embed.set_author(name="Намечается война между 2-мя кланами!")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/607620198534479883/616386780018769922/image_563.png"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607620198534479883/616386508601032704/image_3193.png"
        )
        await ctx.send(embed=DefaultEmbed(f"Вы объявили войну клану {role.mention}"))
        return await tc.send(embed=embed)

    @clan.command(aliases=['победа'])
    @commands.has_any_role(OWNER_ROLE, ADMIN_ROLE)
    async def win(self, ctx, role: Role):
        tc = ctx.guild.get_channel(608730084400037898)
        embed = DefaultEmbed(f"Клан {role.mention} побеждает в войне.")
        embed.set_author(name="Победитель")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/607620198534479883/616387439258370051/image_1802.png"
        )
        await ctx.send(embed=DefaultEmbed(f'Вы выбрали клан {role.mention}'))
        return await tc.send(embed=embed)

    # @commands.command()
    # @commands.has_role(OWNER_ROLE)
    # async def clanwar(self, ctx, *args):
    #     games = list(args)
    #
    #     data = {
    #         'status': 'open',
    #         'games': games,
    #         'clans': []
    #     }
    #
    #     with open('clanwars.pkl', 'wb') as f:
    #         dump(data, f)
    #
    #     await self.clanwar_channel.send('Началась регистрация на войны кланов')
    #
    #     for member in self.leader_role.members:
    #         await send_dm(member, 'Началась регистрация на войны кланов\nИгры: {0}'.format(', '.join(games)))
    #
    # @commands.command()
    # @is_clan_leader()
    # async def war(self, ctx, args):
    #     with open('clanwars.pkl', 'rb') as f:
    #         data = load(f)
    #
    #     if not data or data['status'] == 'closed':
    #         return await ctx.send(embed=DefaultEmbed('Регистрация на войны кланов закрыта'))
    #
    #     if args not in data['games']:
    #         return await ctx.send(embed=DefaultEmbed('Нет такой игры'))
    #
    #     author_id = ctx.author.id
    #
    #     if not data['clans']:
    #         data['clans'].append({'leader_id': author_id, 'games': [args]})
    #     else:
    #         for clan in data['clans']:
    #             if clan['leader_id'] == author_id:
    #                 clan['games'].append(args)
    #
    #     with open('clanwars.pkl', 'wb') as f:
    #         dump(data, f)
    #
    #     role = ctx.guild.get_role(clan_system.get_clan_info(author_id)['clan_role_id'])
    #
    #     await self.clanwar_channel.send(f'Лидер клана {role.mention} выбрал игру: {args}')
    #     return await ctx.send(embed=DefaultEmbed(f'Вы зарегистрировались на войны кланов с игрой: `{args}`'))
    #
    # @commands.command()
    # @commands.has_role(OWNER_ROLE)
    # async def warstart(self, ctx, *args):
    #     with open('clanwars.pkl', 'rb') as f:
    #         data = load(f)
    #
    #     if not data or data['status'] == 'closed':
    #         return await ctx.send(embed=DefaultEmbed('Сначала открой регистрацию на войны кланов'))
    #
    #     data['status'] = 'closed'
    #
    #     with open('clanwars.pkl', 'wb') as f:
    #         dump(data, f)
    #
    #     msg_text = ''
    #
    #     # shuffle кланов НЕ РАБОТАЕТ
    #
    #     for clan in data['clans']:
    #         clan_info = clan_system.get_clan_info(clan['leader_id'])
    #         role = ctx.guild.get_role(clan_info['clan_role_id'])
    #
    #         games = ', '.join(clan["games"])
    #
    #         msg_text += f'{role.mention} - игры: f{games}\n'
    #
    #     return await ctx.send(msg_text)
    #

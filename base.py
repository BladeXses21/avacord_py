from datetime import timedelta

from discord.ext.commands import check, CommandError, Cog, Bot, CommandOnCooldown

from embeds.default import DefaultEmbed


def strfdelta(tdelta: timedelta):
    d = {}
    d["ч"], rem = divmod(tdelta.seconds, 3600)
    d["м"], d["с"] = divmod(rem, 60)

    msg = ''
    for k, v in d.items():
        if v == 0:
            continue
        msg += f'{v}{k} '

    return msg.strip()


def on_cmd_error(ctx, error):
    if str(error) == 'args len':
        return 'Нехватает аргументов'
    elif str(error) == 'not leader':
        return 'Вы не лидер клана'
    elif str(error) == 'mentions':
        return 'Ты в своем уме? Быстро исправь название'
    elif str(error) == 'no mention':
        return 'Вы должны упомянуть кого-то'
    elif str(error) == 'money arg':
        return 'По-моему это не число, перепроверь'
    elif 'no money' in str(error):
        currency = str(error).split(':')[-1]
        s = 'средств'

        if currency == 'energy':
            s = 'энергии'
        elif currency == 'activity':
            s = 'очков активности'
        elif currency == 'silver':
            s = 'серебра'
        elif currency == 'gold':
            s = 'золота'
        elif currency == 'pvp':
            s = 'PVP очков'
        elif currency == 'cc':
            s = ''

        return f'Недостаточно {s}'
    elif 'Недостаточно клан очков' in str(error):
        return 'Недостаточно клан очков'
    elif str(error) == 'no coupons':
        return 'Недостаточно купонов'
    elif type(error) == CommandOnCooldown:
        return f'Подожди {int(error.retry_after)}c'


def required_args(count: int):
    def inner(ctx, *args):
        if len(ctx.message.content.split()) - 1 < count:
            raise CommandError('args len')
        return True
    return check(inner)


def has_mention(*args, **kwargs):
    def inner(ctx):
        if len(ctx.message.mentions) == 1:
            return True
        raise CommandError('no mention')
    return check(inner)


def no_mentions():
    def inner(ctx):
        if ctx.message.mentions:
            raise CommandError('mentions')
        return True
    return check(inner)


def has_mentions(count: int):
    def inner(ctx, *args):
        if len(ctx.message.mentions) == count:
            return True
    return check(inner)


async def send_dm(member, msg: str):
    try:
        dm = await member.create_dm()
        await dm.send(embed=DefaultEmbed(msg))
    except:
        pass


class BaseCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

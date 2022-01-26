from cogs.admin import *
from cogs.emotions import EmotionsCog
from cogs.inventory import InventoryCog
from statuses import StatusesCog
from cogs.economy import EconomyCog
from cogs.activity import ActivityCog
# from donate import DonateCog
from cogs.clans import ClansCog
from cogs.private import PrivatesCog
from cogs.gaynigger import GayNiggerClient
from cogs.owners import OwnersCog
from cogs.roles import RolesCog
from cogs.profile import ProfileCog
from rooms_events import EventCog
from cogs.mini_games import MinigamesCog

from embeds.default import ErrorEmbed
from base import on_cmd_error
from bot_logger import gluon_logger


gluon_bot = commands.Bot(command_prefix='!', help_command=None)


@gluon_bot.event
async def on_ready():
    gluon_logger.info('READY')


@gluon_bot.command()
@commands.has_role(OWNER_ROLE)
async def cmds(ctx):
    msg = ""
    for name, cog in gluon_bot.cogs.items():
        for cmd in cog.get_commands():
            if isinstance(cmd, commands.Group):
                for subcmd in cmd.commands:
                    msg += cmd.name + " " + subcmd.name + '\n'
            else:
                aliases = " - " + str(cmd.aliases) if cmd.aliases else ""
                msg += cmd.name + aliases + '\n'

    return await ctx.send(msg)


@gluon_bot.event
async def on_command_error(ctx, error):
    if type(error) == commands.CommandNotFound:
        return

    msg = on_cmd_error(ctx, error)

    if msg:
        return await ctx.send(embed=ErrorEmbed(msg))

    gluon_logger.error(f'{str(ctx.author)} - {ctx.message.content}')
    gluon_logger.error(error)

gluon_bot.add_cog(ClansCog(gluon_bot))
gluon_bot.add_cog(ProfileCog(gluon_bot))
gluon_bot.add_cog(StatusesCog(gluon_bot))
gluon_bot.add_cog(MinigamesCog(gluon_bot))
gluon_bot.add_cog(InventoryCog(gluon_bot))
gluon_bot.add_cog(EconomyCog(gluon_bot))
gluon_bot.add_cog(PrivatesCog(gluon_bot))
gluon_bot.add_cog(GayNiggerClient(gluon_bot))
gluon_bot.add_cog(ActivityCog(gluon_bot))
gluon_bot.add_cog(MutesCog(gluon_bot))
gluon_bot.add_cog(EmotionsCog(gluon_bot))
gluon_bot.add_cog(AdminCog(gluon_bot))
gluon_bot.add_cog(OwnersCog(gluon_bot))
gluon_bot.add_cog(RolesCog(gluon_bot))
gluon_bot.add_cog(EventCog(gluon_bot))

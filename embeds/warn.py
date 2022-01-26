from discord import Embed, Colour


class WarnEmbed(object):

    def __init__(self, ctx, member, reason, warn_date):
        self._embed = Embed(colour=Colour(0x4fabe9), description="Варн")

        self._embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        self._embed.set_footer(text="!warn / !варн @линк [причина]")

        self._embed.add_field(name="Кому", value=f"{member.mention}")
        self._embed.add_field(name="Причина", value=f"{reason}")
        self._embed.add_field(name="Дата варна", value=f"`{warn_date}`")

    @property
    def embed(self):
        return self._embed


class WarnDMEmbed(object):

    def __init__(self, ctx, reason):
        self._embed = Embed(
            colour=Colour(0x36393f), description="Варн",
            title="Тебе выдали предупреждение! В случае повторного нарушения правил сервера, ты попадешь в мут."
        )
        self._embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607620198534479883/615451004556673024/image_3166.png"
        )

        self._embed.add_field(name="Кто выдал:", value=f"{str(ctx.author)}", inline=True)
        self._embed.add_field(name="Причина:", value=f"{reason}", inline=True)

    @property
    def embed(self):
        return self._embed

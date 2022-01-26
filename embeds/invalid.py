from discord import Embed, Colour


class InvalidEmbed(object):

    def __init__(self, ctx, member, reason, invalid_date):
        self._embed = Embed(colour=Colour(0x4fabe9), description="Инвалид")

        self._embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        self._embed.set_footer(text="!invalid / !инвалид @линк [причина]")

        self._embed.add_field(name="Кому", value=f"{member.mention}")
        self._embed.add_field(name="Причина", value=f"{reason}")
        self._embed.add_field(name="Дата инвалида", value=f"`{invalid_date}`")

    @property
    def embed(self):
        return self._embed

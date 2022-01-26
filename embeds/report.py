from discord import Embed, Colour


class ReportEmbed(object):
    
    def __init__(self, ctx, member, reason, request_id, created_time):
        self._embed = Embed(colour=Colour(0x4fabe9), description="Репорт на участника :poop: ")

        self._embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        self._embed.set_footer(
            text=f"!report / !репорт @линк [причина], !report / !репорт [номер заявки] - принять репорт"
        )
        self._embed.add_field(name="На кого", value=f"{member.mention}")
        self._embed.add_field(name="Причина", value=f"{reason}")
        self._embed.add_field(name="Номер заявки", value=f"`{request_id}`")
        self._embed.add_field(name="Дата заявки", value=f"`{created_time}`")
        
    @property
    def embed(self):
        return self._embed

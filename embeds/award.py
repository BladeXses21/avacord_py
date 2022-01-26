from discord import Embed, Colour


class AwardCommandEmbed(object):
    
    def __init__(self, ctx, event_name, money, member, request_id, created_time):
        self._embed = Embed(colour=Colour(0xffe200), description="Заявка на выдачу награды за ивент")
        
        self._embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        self._embed.set_footer(text="!награда @линк [кол-во] [название ивента] / !принять [номер заявки]")

        self._embed.add_field(name="Ивент", value=f"{event_name}", inline=True)
        self._embed.add_field(name="Сумма", value=f"{money}", inline=True)
        self._embed.add_field(name="Кому", value=f"{member.mention}")
        self._embed.add_field(name="Номер заявки", value=f"`{request_id}`")
        self._embed.add_field(name="Дата заявки", value=f"`{created_time}`")

    @property
    def embed(self):
        return self._embed

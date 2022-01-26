from discord import Embed, Colour


class MuteDMEmbed(object):

    def __init__(self, ctx, reason, mute_date):
        self._embed = Embed(title="Тебе выдали мут на сервере AVACORD", colour=Colour(0x36393f))

        self._embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607620198534479883/615451004556673024/image_3166.png"
        )
        self._embed.set_author(name="THIS IS MUTEEEEEEEEEEEEEEEEEEEEEE!")

        self._embed.add_field(name="Кто выдал:", value=f"{str(ctx.author)}", inline=True)
        self._embed.add_field(name="Причина:", value=f"{reason}", inline=True)
        self._embed.add_field(name="Дата размута:", value=f"{mute_date}", inline=True)

    @property
    def embed(self):
        return self._embed


class MuteEmbed(object):

    def __init__(self, ctx, member, reason, mute_date, unmute_date):
        self._embed = Embed(colour=Colour(0x4fabe9), description="Мут")

        self._embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        self._embed.set_footer(text="!mute / !мут @линк [мин] [причина]")

        self._embed.add_field(name="Кому", value=f"{member.mention}")
        self._embed.add_field(name="Причина", value=f"{reason}")
        self._embed.add_field(name="Дата мута", value=f"`{mute_date}`")
        self._embed.add_field(name="Дата размута", value=f"`{unmute_date}`")

    @property
    def embed(self):
        return self._embed

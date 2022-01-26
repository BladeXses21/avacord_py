from discord import Embed, Colour


class BanEmbed(object):

    def __init__(self, ctx, reason):
        self._embed = Embed(
            title="Ты забанен на сервере AVACORD", colour=Colour(0x36393f),
            description="[ПОДАЧА ЗАЯВКИ НА РАЗБАН](https://docs.google.com/forms/d/1TK4Mn1lb6BSgFCPnovyFgoIHNE8jZmClrk0BYOf96EM/edit)"
        )

        self._embed.set_image(
            url="https://media1.tenor.com/images/4c906e41166d0d154317eda78cae957a/tenor.gif?itemid=12646581"
        )
        self._embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607620198534479883/615451004556673024/image_3166.png"
        )
        self._embed.set_author(name="THIS IS BAAAAAAAAAAAAAAAAAAAAAAN!")

        self._embed.add_field(name="Кто выдал:", value=f"{str(ctx.author)}", inline=True)
        self._embed.add_field(name="Причина:", value=f"{reason}", inline=True)

    @property
    def embed(self):
        return self._embed

from discord import Embed, Colour


class EverydayBonus(object):

    def __init__(self, money, mercstar):
        self._embed = Embed(
            title="Ежедневный бонус", colour=Colour(0xffffff), description=f"Ты получил {money} {mercstar}"
        )
        self._embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/610456153503301632/615261118520360962/image_3840.png"
        )

    @property
    def embed(self):
        return self._embed

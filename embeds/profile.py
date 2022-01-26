from discord import Embed, Colour


class ProfileEmbed(object):

    def __init__(self, author, member, status, money, clan, is_marriage, marriage, emojis, img_url, vip=False):
        self._embed = Embed(
            title=f"Профиль {str(member)}", colour=Colour(0xffffff), description=f"\n```{status}```\n"
        )
        self._embed.set_thumbnail(url=member.avatar_url)

        self._embed.add_field(name="Баланс:", value=f"{int(money['silver'])} {emojis['avasilver']}", inline=True)
        self._embed.add_field(name="Донат:", value=f"{int(money['gold'])} {emojis['avagold']}", inline=True)
        self._embed.add_field(name="Энергия:", value=f"{int(money['energy'])} {emojis['avaenergy']} ", inline=True)
        self._embed.add_field(name="Клан:", value=f"{clan} ", inline=True)
        self._embed.add_field(name="Активность:", value=f"{int(money['activity'])} {emojis['avaactivity']} ", inline=True)

        self._embed.add_field(
            name="Семейное положение:" if is_marriage else "Влюблен(а) в:", value=f"{marriage}", inline=True
        )
        self._embed.set_footer(text=str(author), icon_url=author.avatar_url)
        self._embed.set_author(
            name="VIP" if vip else "",
            icon_url="https://media.discordapp.net/attachments/607620198534479883/616003038016176138/image_75.png" if vip else ""
        )
        self._embed.set_image(url=img_url if img_url else "")

    @property
    def embed(self):
        return self._embed

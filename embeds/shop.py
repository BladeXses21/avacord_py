from discord import Embed, Colour


class DonateShop(object):
    
    def __init__(self, owners, emojis):
        self._embed = Embed(
            description=f"Для покупки {emojis['mercdonat']} обращайтесь к {owners}\n\n"
            f"Вы можете конвертировать 1 {emojis['mercdonat']} → 10 {emojis['mercstar']}\n"
            f"Команда: `!перевод / !transfer [кол-во желаемых звезд]`",
            color=Colour(0x9900ef)
        )
        self._embed.set_author(name='Донат магазин "Gold Comets"')
        self._embed.set_thumbnail(
            url='https://media2.giphy.com/media/Qze6gDuxZt48U/giphy.gif?cid=790b76115d35ef6d5a514a30599a9c14&rid=giphy.gif'
        )

        self._embed.set_footer(text="Чтобы купить одну из привилегий пропиши !donate buy [id]")

        self._embed.add_field(name=f"#1 На месяц = 399 {emojis['mercdonat']}", value="<@&601120959549931521>", inline=True)
        self._embed.add_field(name=f"#2 На неделю = 150 {emojis['mercdonat']}", value="<@&601120959549931521>", inline=True)
        self._embed.add_field(name=f"#3 На месяц = 299 {emojis['mercdonat']}", value="<@&601120960531267614>", inline=True)
        self._embed.add_field(name=f"#4 На неделю = 100 {emojis['mercdonat']}", value="<@&601120960531267614>", inline=True)
        self._embed.add_field(name=f"#5 На месяц = 199 {emojis['mercdonat']}", value="<@&601120961202225180>", inline=True)
        self._embed.add_field(name=f"#6 На неделю = 75 {emojis['mercdonat']}", value="<@&601120961202225180>", inline=True)
        self._embed.add_field(name=f"#7 На месяц = 199 {emojis['mercdonat']}", value="💒 - Love Room", inline=True)
        self._embed.add_field(name=f"#8 На неделю = 99 {emojis['mercdonat']}", value="💒 - Love Room", inline=True)
        self._embed.add_field(name=f"#9 На месяц = 199 {emojis['mercdonat']}", value="🔥 - Личная Роль", inline=True)
        self._embed.add_field(name=f"#10 На неделю = 99 {emojis['mercdonat']}", value="🔥 - Личная Роль", inline=True)
    
    @property
    def embed(self):
        return self._embed
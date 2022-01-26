from discord import Colour, Embed


class TextChannelEmbed(object):

    def __init__(self):
        self._embed = Embed(
            description="Хей-хей, этот чат доступен только тебе и видишь его только ты", colour=Colour(0x9900ef)
        )
        self._embed.add_field(
            name='!demo / !демо', value='Отправляет ссылку на видео демонстрацию твоего войса'
        )
        self._embed.add_field(
            name='!invite / !позвать @линк', value='Разрешает доступ к текстовому каналу пользователю'
        )
        self._embed.add_field(
            name='!pban / !пбан @линк', value='Блокирует доступ пользователю к чату и войсу'
        )

    @property
    def embed(self):
        return self._embed

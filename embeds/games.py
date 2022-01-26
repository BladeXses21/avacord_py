from discord import Embed, Colour


class BaseGameEmbed(object):
    title = ''

    def __init__(self, **kwargs):
        self.description = f"\n\n**Время проведения ивента: {kwargs['event_date']} по МСК** \n" \
            f"**Ведущий: {kwargs['event_maker']}**\n" \
            f"**Комната ивента:** {kwargs['event_link']}\n"
        self.mercstar = kwargs['emojis']['avasilver']
        self._embed = Embed(title=f"A V A C O R D {self.title}")

    @property
    def embed(self):
        return self._embed


class CrocodileEmbed(BaseGameEmbed):
    title = "КРОКОДИЛ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xf9eded)
        self._embed.description = self.description + "**Ссылка на сайт:** https://gartic.io/\n\n**Призы**"
        self._embed.set_image(url="https://cdn.discordapp.com/attachments/581758024805253121/600682510883618829/VtlP.gif")

        self._embed.add_field(name="🥇 место ", value=f"30 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥈 место", value=f"25 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥉 место", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 место", value=f"10 {self.mercstar}", inline=True)


class TalkAboutEmbed(BaseGameEmbed):
    title = "ПОГОВОРИМ О"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xe6ffff)
        self._embed.description = self.description + "**Ссылка на сайт:** https://gartic.io/\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601714603914821643/Gifius.ru.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"15 {self.mercstar}", inline=True)


class ChessEmbed(BaseGameEmbed):
    title = "ШАХМАТЫ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xec0d0c)
        self._embed.description = self.description + "**Ссылка на сайт:** https://lichess.org/\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601729796145414163/111333.gif"
        )

        self._embed.add_field(name="🏆 победа", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"5 {self.mercstar}", inline=True)


class ShashkiEmbed(BaseGameEmbed):
    title = "Шашки"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xff6900)
        self._embed.description = self.description
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/607970620533112832/7CGo.gif"
        )

        self._embed.add_field(name="🏆 победа", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"5 {self.mercstar}", inline=True)


class DominoEmbed(BaseGameEmbed):
    title = "Домино"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xabb8c3)
        self._embed.description = self.description
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/607971140769677322/Dominoessrcmyneighborsekikun_4fe98d_4966601.gif"
        )

        self._embed.add_field(name="🏆 победа", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"5 {self.mercstar}", inline=True)


class CardsToAllEmbed(BaseGameEmbed):
    title = "КАРТЫ ПРОТИВ ВСЕХ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xd4e8f2)
        self._embed.description = self.description + "**Ссылка на сайт:** http://cardsvs.ru/\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601731742126309386/image_862907151404511829727.gif"
        )

        self._embed.add_field(name="🏆 победа", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"10 {self.mercstar}", inline=True)


class WhoAmIEmbed(BaseGameEmbed):
    title = "КТО-Я?"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xafbfd7)
        self._embed.description = self.description + "\n**Призы**\n"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601734386760810526/UCmk.gif"
        )

        self._embed.add_field(name="🏆 победа", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"10 {self.mercstar}", inline=True)


class MonopolyEmbed(BaseGameEmbed):
    title = "МОНОПОЛИЯ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xafbfd9)
        self._embed.description = self.description + "**Ссылка на сайт:** https://monopoly-one.com\n\n**Призы**\n"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601739163414429696/orig.gif"
        )

        self._embed.add_field(name="🥇место", value=f"35 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥈место", value=f"30 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥉место", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽участие", value=f"15 {self.mercstar}", inline=True)


class CodenamesEmbed(BaseGameEmbed):
    title = "КОДНЕЙМС"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xee3535)
        self._embed.description = self.description + "**Ссылка на сайт:** https://meme-police.ru/bg/codenames\n\n**Призы**\n"
        self._embed.set_image(url="https://i.gifer.com/o3F.gif")

        self._embed.add_field(name="🏆 место", value=f"35 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"15 {self.mercstar}", inline=True)


class TriviadorEmbed(BaseGameEmbed):
    title = "ТРИВИАДОР"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xafdfd9)
        self._embed.description = self.description + "**Ссылка на сайт:** https://russia.triviador.net/\n\n**Призы**\n"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601781261320847370/image_861304161346558888743.gif"
        )

        self._embed.add_field(name="🏆 место", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"10 {self.mercstar}", inline=True)


class SoloEmbed(BaseGameEmbed):
    title = "СОЛО"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xa8eae5)
        self._embed.description = self.description + "**Ссылка на сайт:** https://boardgamearena.com\n\n**Призы**\n"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601782770100076556/72P.gif"
        )

        self._embed.add_field(name="🥇место", value=f"25 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥈место", value=f"15 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥉место", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"5 {self.mercstar}", inline=True)


class WithoutStopEmbed(BaseGameEmbed):
    title = "БЕЗ ОСТАНОВКИ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x9fc7ec)
        self._embed.description = self.description + "**Ссылка на игру:** https://boardgamearena.com\n\n**Призы**\n"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601789291332370471/5f7a60591286779152c35443d3b44014.gif"
        )

        self._embed.add_field(name="🏆 место", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"10 {self.mercstar}", inline=True)


class PokerEmbed(BaseGameEmbed):
    title = "ПОКЕР"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x9fc7ec)
        self._embed.description = self.description + "**Ссылка на игру:** https://worldpokerclub.com/\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601792295158808650/1401700952_1970100794.gif"
        )

        self._embed.add_field(name="🏆 место", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"5 {self.mercstar}", inline=True)


class SudokuEmbed(BaseGameEmbed):
    title = "СУДОКУ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xe6b8f2)
        self._embed.description = self.description + "**Ссылка на игру:** http://sudoku.org.ua/rus/\n"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601802761251586059/image_860308171619518584436.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"15 {self.mercstar}", inline=True)


class FoolEmbed(BaseGameEmbed):
    title = "ДУРАК"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xeff2be)
        self._embed.description = self.description + "\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601792295158808650/1401700952_1970100794.gif"
        )

        self._embed.add_field(name="🏆 место", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"5 {self.mercstar}", inline=True)


class IOGaemsEmbed(BaseGameEmbed):
    title = "ИГРЫ СЕРИИ IO"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x693e3)
        self._embed.description = self.description + "\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601804894302765056/tumblr_mposgyzarc1s5lf2ro1_500.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"15 {self.mercstar}", inline=True)


class GnomsEmbed(BaseGameEmbed):
    title = "ГНОМЫ И ВРЕДИТЕЛИ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x474556)
        self._embed.description = self.description + "**Ссылка на игру:** https://boardgamearena.com\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/601121089845985280/601806956709281811/image_861304160646429883270.gif"
        )

        self._embed.add_field(name="🏆 место", value=f"35 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"15 {self.mercstar}", inline=True)


class CowEmbed(BaseGameEmbed):
    title = "КОРОВА006"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xcc3654)
        self._embed.description = self.description + "**Ссылка на сайт:** https://meme-police.ru/bg/memexit#\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601809258014703636/images.jpg"
        )

        self._embed.add_field(name="🥇место", value=f"25 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥈место", value=f"15 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥉место", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"5 {self.mercstar}", inline=True)


class ImaginariumEmbed(BaseGameEmbed):
    title = "ИМАДЖИНАРИУМ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xeb144c)
        self._embed.description = self.description + "**Ссылка на сайт:** https://boardgamearena.com\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/601810683759165451/K1uU.gif"
        )

        self._embed.add_field(name="🥇место", value=f"25 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥈место", value=f"15 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥉место", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"5 {self.mercstar}", inline=True)


class MinecraftEmbed(BaseGameEmbed):
    title = "МАИНКРАФТ"

    def __init__(self, ip, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xe09a75)
        self._embed.description = self.description + f"**IP: {ip}**\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602157711433400321/e0de1a902ef2459d8f5867fb854aeb73.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"40 {self.mercstar}", inline=True)


class Dota2PublicEmbed(BaseGameEmbed):
    title = "DOTA2 ПАБЛИК"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x5a9466)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602158581986623498/32ac5cb57429afede678aeca28abe130c2ceca64.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"40 {self.mercstar} (за час игры)", inline=True)


class LolPublicEmbed(BaseGameEmbed):
    title = "LOL ПАБЛИК"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x5a9466)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602159274587586570/Br4y.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"40 {self.mercstar} (за час игры)", inline=True)


class Brawhalla1x1Embed(BaseGameEmbed):
    title = "Brawlhalla1x1"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x8ed1fc)
        self._embed.description = self.description
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/607968736250429464/mlPz0yF.png"
        )

        self._embed.add_field(name="🏆 победа", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"10 {self.mercstar}", inline=True)


class YgadaikaEmbed(BaseGameEmbed):
    title = "Угадайка"

    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x7bdcb5)
        self._embed.description = self.description + f"\n**Тематика: {theme}**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/607970132332904479/b95bf2ca645c.gif"
        )

        self._embed.add_field(name="🏆 победа", value=f"30 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"15 {self.mercstar}", inline=True)


class DontStarveEmbed(BaseGameEmbed):
    title = "Don't Starve Together"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x5a5c5a)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602159688502738953/AngelicAgonizingFlatcoatretriever-size_restricted.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"35 {self.mercstar} (за час игры)", inline=True)


class OSUEmbed(BaseGameEmbed):
    title = "ОСУ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x6a898f)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602160313055576065/Js6x.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"40 {self.mercstar} (за час игры)", inline=True)


class HearthstoneEmbed(BaseGameEmbed):
    title = "Hearthstone"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xe8d0a9)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602160899716808704/79DN.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"35 {self.mercstar} (за час игры)", inline=True)


class OverwatchEmbed(BaseGameEmbed):
    title = "Overwatch"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xa3583c)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602162333808066581/14154309068336.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"35 {self.mercstar} (за час игры)", inline=True)


class Puzzles300Embed(BaseGameEmbed):
    title = "300"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xd6b6a7)
        self._embed.title = f'A V A C O R D ПАЗЛЫ 300'
        self._embed.description = self.description + f"**Ссылка на сайт:** https://www.jigsawplanet.com/\n\n**Призы**"
        self._embed.set_image(url="https://cdn.discordapp.com/attachments/599245320429502464/602167915218731019/10.gif")

        self._embed.add_field(name="🎽 участие", value=f"20 {self.mercstar}", inline=True)


class StoriesEmbed(BaseGameEmbed):
    title = "СКАЗКИ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x53a1e0)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602168787608797187/gifki-spokojnoj-nochi-2.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"20 {self.mercstar}", inline=True)


class YesNoEmbed(BaseGameEmbed):
    title = "ДАНЕТКИ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xab8771)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602169954212642826/EmbellishedDismalIchidna-size_restricted.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"10 {self.mercstar}", inline=True)


class TrueOrActionEmbed(BaseGameEmbed):
    title = "ПРАВДА ИЛИ ДЕЙСТВИЕ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xab7771)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602172003772006401/BG9X.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"15 {self.mercstar}", inline=True)


class RabbitEmbed(BaseGameEmbed):
    title = "RABBIT"

    def __init__(self, name, category, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x7bdcb5)
        self._embed.description = self.description + f"\n**Название: {name.replace('_', ' ')}**\n" \
            f"**Жанр**: {category}\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602173747302105109/171129_7822.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"40 {self.mercstar} (за 120 минут просмотра)", inline=True)


class SpyEmbed(BaseGameEmbed):
    title = "ШПИОН"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xf78da7)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602176283497070603/1423155091_file.gif"
        )

        self._embed.add_field(name="⚫ Шпион", value=f"30 {self.mercstar}", inline=True)
        self._embed.add_field(name="⚪ Жители", value=f"15 {self.mercstar}", inline=True)


class HentaiMangaEmbed(BaseGameEmbed):
    title = "ХЕНТАЙ МАНГА"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xf78da7)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602486744365006858/1500276292_1493319692_tumblr_op2c48NF0V1urooiqo1_500_1.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"50 {self.mercstar}", inline=True)


class DeceitEmbed(BaseGameEmbed):
    title = "DECEIT"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x397d58)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602501676188041247/8fcf9b433ad91f5abe779fff46c6d3e6.gif"
        )

        self._embed.add_field(name="🎽 участие", value=f"35 {self.mercstar} (за час игры)", inline=True)


class WordByWordEmbed(BaseGameEmbed):
    title = "СЛОВА ИЗ СЛОВ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x5ccca7)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602502213239046146/hiyori-iki-anime-D0B3D0B8D184D0BAD0B8-D091D0B5D0B7D0B4D0BED0BCD0BDD18BD0B9-D0B1D0BED0B3-1084905.gif"
        )

        self._embed.add_field(name="🏆победа", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽участие", value=f"10 {self.mercstar}", inline=True)


class SeaWarEmbed(BaseGameEmbed):
    title = "МОРСКОЙ БОЙ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x1bc2d1)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602502759069122582/image_861106160912089952768.gif"
        )

        self._embed.add_field(name="🏆победа", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽участие", value=f"5 {self.mercstar}", inline=True)


class Dota2CloseEmbed(BaseGameEmbed):
    title = "DOTA2 КЛОЗ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x67c981)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602503316014104586/image_86071017163656425000.gif"
        )

        self._embed.add_field(name="🏆 победа", value=f"30 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"20 {self.mercstar}", inline=True)


class CitadelsEmbed(BaseGameEmbed):
    title = "ЦИТАДЕЛИ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xc9c667)
        self._embed.description = self.description + f"**Ссылка на игру:** http://citadeli.ru/\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602504074256056351/igroved_citadels_08.png"
        )

        self._embed.add_field(name="🏆 победа", value=f"30 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"20 {self.mercstar}", inline=True)


class TreasureAndDoorsEmbed(BaseGameEmbed):
    title = "ДВЕРИ И СОКРОВИЩА"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xc96767)
        self._embed.description = self.description + f"**Ссылка на игру:** https://www.doors-treasures.ru/\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602504237192052746/mainN.png"
        )

        self._embed.add_field(name="🏆 победа", value=f"30 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"20 {self.mercstar}", inline=True)


class SigameEmbed(BaseGameEmbed):
    title = "СВОЯ ИГРА"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x2c2391)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602506587894185984/004.png"
        )

        self._embed.add_field(name="🏆 победа", value=f"35 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"20 {self.mercstar}", inline=True)


class MarriageEmbed(BaseGameEmbed):
    title = "СВАДЬБА"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xed8ad3)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602508683955535912/Love-8.gif"
        )

        self._embed.add_field(name="💕 Паре", value=f"лав рума (на месяц) или парная роль (на месяц) или 2 кольца +50 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"30 {self.mercstar}", inline=True)


class MafiaEmbed(BaseGameEmbed):
    title = "МАФИЯ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0x185cab)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602509480336424989/1523663921_1493177890_tumblr_nzd8qmzjZ31s5wiico1_500.gif"
        )

        self._embed.add_field(name="⚫ Мафия", value=f"40 {self.mercstar}", inline=True)
        self._embed.add_field(name="🔴 Жители", value=f"30 {self.mercstar}", inline=True)
        self._embed.add_field(name="⚪ Маньяк", value=f"50 {self.mercstar}", inline=True)


class PuzzlesEmbed(BaseGameEmbed):
    title = "ПАЗЛЫ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xfcb900)
        self._embed.description = self.description + f"**Ссылка на игру:** https://www.jigsawplanet.com/\n\n**Призы**"
        self._embed.set_image(url="https://cdn.discordapp.com/attachments/599245320429502464/602167915218731019/10.gif")

        self._embed.add_field(name="1 пазл", value=f"10 {self.mercstar}", inline=True)
        self._embed.add_field(name="2 пазл", value=f"15 {self.mercstar}", inline=True)
        self._embed.add_field(name="3 пазл", value=f"20 {self.mercstar}", inline=True)
        self._embed.add_field(name="участие ", value=f"5 {self.mercstar}", inline=True)


class HatEmbed(BaseGameEmbed):
    title = "ШЛЯПА"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xde1b1b)
        self._embed.description = self.description + f"**Ссылка на игру:** https://meme-police.ru/bg/alias#\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602512246232449024/f7946a5b13d16e83b0617df2b9dd87674e92cdb1_hq.gif"
        )

        self._embed.add_field(name="🥇 место", value=f"35 {self.mercstar} (каждому) ", inline=True)
        self._embed.add_field(name="🥈 место", value=f"25 {self.mercstar} (каждому) ", inline=True)
        self._embed.add_field(name="🥉 место", value=f"15 {self.mercstar} (каждому) ", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"10 {self.mercstar} (каждому) ", inline=True)


class AsylumEmbed(BaseGameEmbed):
    title = "ПСИХУШКА"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xabb8c3)
        self._embed.description = self.description + f"**Ссылка на игру:** https://meme-police.ru/bg/alias#\n\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602513355831508992/1483200551162427516.gif"
        )

        self._embed.add_field(name="🥇 место", value=f"35 {self.mercstar} (каждому) ", inline=True)
        self._embed.add_field(name="🥈 место", value=f"25 {self.mercstar} (каждому) ", inline=True)
        self._embed.add_field(name="🥉 место", value=f"15 {self.mercstar} (каждому) ", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"10 {self.mercstar} (каждому) ", inline=True)


class TalentsShowEmbed(BaseGameEmbed):
    title = "ШОУ ТАЛАНТОВ"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xe3d666)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602513998742683670/8khi.gif"
        )

        self._embed.add_field(name="🥇 место", value=f"150 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥈 место", value=f"100 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥉 место", value=f"80 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"50 {self.mercstar}", inline=True)


class LiteratureEveningEmbed(BaseGameEmbed):
    title = "ЛИТЕРАТУРНЫЙ ВЕЧЕР"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._embed.colour = Colour(0xe39e66)
        self._embed.description = self.description + f"\n**Призы**"
        self._embed.set_image(
            url="https://cdn.discordapp.com/attachments/599245320429502464/602514004350337044/1EjJ.gif"
        )

        self._embed.add_field(name="🥇 место", value=f"150 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥈 место", value=f"100 {self.mercstar}", inline=True)
        self._embed.add_field(name="🥉 место", value=f"80 {self.mercstar}", inline=True)
        self._embed.add_field(name="🎽 участие", value=f"50 {self.mercstar}", inline=True)

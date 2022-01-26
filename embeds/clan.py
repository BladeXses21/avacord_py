from discord import Embed, Colour


class ClanEmbed(object):

    def __init__(self, leader, clan_name, colour, description, members_cnt, clan_points, avatar_url):
        self._embed = Embed(
                title=f"Профиль клана {clan_name}",
                colour=Colour(colour),
                description=f"\n```{description}```\n"
            )
        self._embed.set_footer(text=f"Чтобы вступить в клан пропиши !клан заявка @{str(leader)}.")

        if avatar_url:
            self._embed.set_thumbnail(url=avatar_url)

        self._embed.add_field(name="Всего участников:", value=f'😊 __{members_cnt}__', inline=True)
        self._embed.add_field(name="Баланс клана:", value=f'💸 __{clan_points}__', inline=False)
        self._embed.add_field(name="Лидер:", value=f'👑 __{leader.mention}__', inline=False)

    @property
    def embed(self):
        return self._embed


class ClanCreateEmbed(object):

    def __init__(self):
        self._embed = Embed(
            color=Colour(0xffffff),
            description="Хэй! Создание клана - ответственный шаг. Скорее ознакомься с правилами, "
                        "чтобы в дальнейшем у тебя не возникало проблем.\n\n1. Запрещено устраивать "
                        "рейды на сервер.\n```md\n#Удаление клана```\n2. Вы должны удалять сообщения своего клана "
                        "в канале <#608730084400037898>, в случае того, если они оскорбляют другой клан. Если после "
                        "предупреждения они не удалены, то\n```md\n#Запрет писать в чат на 2 дня```\n3. Запрещено "
                        "выдавать доступ к каналам посторонним без согласия администрации.\n```md\n#Закрытие доступа "
                        "к правам каналов```\n4. Обязательно оплачивайте налог. Если вы отнесетесь пренебрежительно к "
                        "этому 2 раза, то\n```md\n#Удаление клана```\n5. Нельзя устраивать и игнорировать травлю "
                        "участников сервера и клана, если большинство людей твоего клана будут травить одного и это "
                        "будет выходит за рамки, то ты должен это прекратить в противном случае\n```md\n#Удаление "
                        "клана```\n6. Нельзя оскорблять в названии клана, ставить на аватарку клана запрещенный "
                        "контент и т.д.\n```md\n#Удаление клана```\n7. Нельзя вызывать 2 и более клана сразу. "
                        "(Исключение: массовые клановые забивы)\n```md\n#На усмотрение админа```"
        )
        self._embed.set_author(name="Клановые правила")
        self._embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607620198534479883/616353157265489941/image_3193.png"
        )

    @property
    def embed(self):
        return self._embed


class ClanKickEmbed(object):

    def __init__(self):
        self._embed = Embed(
            description="Тебя выгнали с клана!",
            color=Colour(0x36393f)
        )
        self._embed.set_image(url='https://rockstarsupport.zendesk.com/hc/user_images/8fNJeG4ve36KFOhS2XP7fA.gif')

    @property
    def embed(self):
        return self._embed


class ClanRequestEmbed(object):

    def __init__(self, member, request_id):
        self._embed = Embed(
            description=f'В твой клан хочет вступить новый участник, прими наконец его.', color=Colour(0x36393f)
        )
        self._embed.set_author(name="Заявка")
        self._embed.set_footer(text=f"Чтобы принять введи команду !клан принять {request_id}")
        self._embed.add_field(name="Кто подал заявку:", value=f"`{str(member)}`", inline=True)
        self._embed.add_field(name="Номер заявки:", value=f"{request_id}", inline=True)

    @property
    def embed(self):
        return self._embed


class ClanAcceptEmbed(object):

    def __init__(self, clan_name: str):
        self._embed = Embed(description=f'Поздравляем! Тебя приняли в клан {clan_name}', color=Colour(0x36393f))
        self._embed.set_image(url='https://i.gifer.com/Be.gif')

    @property
    def embed(self):
        return self._embed

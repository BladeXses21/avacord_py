from discord import Embed, Colour


class DefaultEmbed(Embed):

    def __init__(self, description, **kwargs):
        kwargs['description'] = description
        super().__init__(**kwargs)
        self.color = Colour(0xffffff)


class ErrorEmbed(DefaultEmbed):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = Colour(0xff0000)

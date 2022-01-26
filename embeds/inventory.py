from discord import Colour, Embed


class InventoryEmbed(object):
    
    def __init__(self, member, ctx, inventory, emojis):
        self._embed = Embed(colour=Colour(0x9900ef), description=f"Инвентарь {member}")
        self._embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607555730458804224/616319898322337809/image_3177.png"
        )
        self._embed.set_author(
            name=f"Инвентарь {str(member)}",
            icon_url=ctx.author.avatar_url
        )
        self._embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)

        role_coupons = f"{emojis['avarole6']} x{int(inventory['role_6'])} "
        role_coupons += f'{emojis["avarole3"]} x{int(inventory["role_3"])} '
        role_coupons += f'{emojis["avarole2"]} x{int(inventory["role_2"])}'

        self._embed.add_field(name="Купоны на роль:", value=role_coupons, inline=True)
        self._embed.add_field(name="Торты:", value=f"{emojis['avacake']} x{int(inventory['cakes'])}", inline=True)
        self._embed.add_field(name="Фишки:", value=f"{emojis['avafishki']} x{int(inventory['sgift'])}", inline=True)
        self._embed.add_field(name="Подарок:", value=f"{emojis['avagift']} x{int(inventory['bgift'])}", inline=True)
        self._embed.add_field(name="Кольца:", value=f"{emojis['avaring']} x{int(inventory['rings'])}", inline=True)
        self._embed.add_field(name="Кофе:", value=f"{emojis['avacoffe']} x{int(inventory['batteries'])}", inline=True)

    @property
    def embed(self):
        return self._embed

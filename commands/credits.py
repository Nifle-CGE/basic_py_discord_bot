class credits():
    name = "credits"
    description = "Pour voirr les credits du bot."
    aliases = ["credit", "cékikafé"]
    authorisation = "everyone"

    async def execute(client, message, args):
        await message.channel.send("Vos crédits")
        return "Les crédits ont étés envoyés."
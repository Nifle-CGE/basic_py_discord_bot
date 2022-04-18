import discord

class logs():
    name = "logs"
    description = "Pour avoir les logs du bot."
    authorisation = "admin"

    async def execute(client, message, args):
        with open("./logs.log", "rb") as fp:
            await message.channel.send(file=discord.File(fp, "logs.log"))

        return "Les logs ont étés envoyés avec succès."
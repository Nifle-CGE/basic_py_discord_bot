class test():
    name = "test"
    description = "Pour savoir si le bot marche. To know if the bot works."
    arguments = "[optionnel : pour tester le systeme d'argument]"
    cooldown = 3
    aliases = ["tests", "ping", "tst"]
    authorisation = "everyone"

    async def execute(client, message, args):
        msg = []
        msg.append("Merci je vais bien.\nThanks, I'm ok.")
        if args:
            if len(args) > 1:
                msg.append("Tes arguments sont : " + ", ".join(args) + ".\nYour arguments are : " + ", ".join(args) + ".")
            elif len(args) > 0:
                msg.append("Ton argument est : " + args[0] + ".\nYour argument is : " + args[0] + ".")

        await message.reply("\n".join(msg))
        return "Le bot a été testé avec succès."
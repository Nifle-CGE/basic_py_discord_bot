import commands, discord
from os import listdir
from os.path import isfile, join

class help():
    name = "help"
    description = "Pour voir toutes les commandes. To see every existing command."
    arguments = "[optionnel : commande sur laquelle vous voulez avoir des informations]"
    cooldown = 5
    aliases = ["aide", "halp", "hlp"]
    authorisation = "everyone"

    async def execute(client, message, args):
        cmds = [filename for filename in listdir("commands") if isfile(join("commands", filename)) and not filename.startswith("_")]
        for val_index, cmd_filenem in enumerate(cmds):
            comd = cmd_filenem[:-3]
            cmds[val_index] = comd

        msg = []
        if not args:
            embed_title = "Help"

            msg.append("Voila une liste de toutes mes commandes : " + ", ".join(cmds))
            msg.append("Vous pouvez utiliser la commande help avec comme argument le nom d'une commande pour avoir des informations sur cette commande.")

            end_msg = "Commande aide générale executée avec succès."
        elif args[0] in cmds:
            curr_cmd = getattr(commands, args[0])
            embed_title = curr_cmd.name

            msg.append(f"Nom : **{curr_cmd.name}**")
            msg.append(f"Description : **{curr_cmd.description}**")
            try:
                msg.append(f"Argument(s) : **{curr_cmd.arguments}**")
            except AttributeError:
                msg.append("Cette commande n'a pas d'arguments.")
            try:
                msg.append(f"Cooldown : **{curr_cmd.cooldown}**")
            except AttributeError:
                msg.append("Cette commande n'a pas de cooldown.")
            try:
                msg.append(f"Aliases : **{'**, **'.join(curr_cmd.aliases)}**")
            except AttributeError:
                msg.append("Cette commande n'a pas d'aliases.")
            msg.append(f"Authorisation : **{curr_cmd.authorisation}**")

            end_msg = f"Commande aide spécifique sur la commande {args[0]} executée avec succès."
        else:
            await message.reply("Your argument is invalid, use the help command without arguments to have a list of commands.")
            return "L'argument procuré ne corresponds à aucune commande."

        embed = discord.Embed(title=embed_title, description="\n".join(msg))

        await message.reply(embed=embed)
        return end_msg
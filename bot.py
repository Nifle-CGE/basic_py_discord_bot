import discord, commands, logging, sys, time
from commands import _stuffimporter
from os import listdir
from os.path import isfile, join

class MyBot(discord.Client):
    async def on_ready(self):
        with open("./logs.log", "r", encoding="utf-8") as log_file:
            log_file = log_file.read()
        if log_file.endswith("|INFO => Ready.\n"):
            with open("./logs.log", "w", encoding="utf-8") as log_wfile:
                log_wfile.write("\n".join(log_file.split("\n")[:-3]) + "\n")
                
        global log
        log = logging.getLogger("logger")
        log.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s|%(levelname)s => %(message)s")

        fh = logging.FileHandler("logs.log", encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        log.addHandler(ch)

        log.info("I'm ready to be ready.")
        
        comds = [filename[:-3] for filename in listdir("commands") if isfile(join("commands", filename)) and not filename.startswith("_")]
        
        global cmds
        cmds = {}
        for item in comds:
            try:
                cmds[getattr(commands, item).name] = [item] + getattr(commands, item).aliases
            except:
                cmds[getattr(commands, item).name] = [item]

        game = discord.Game(_stuffimporter.get_config()["prefix"] + "help")
        await self.change_presence(status=discord.Status.online, activity=game)

        # Mise en place du système de cooldown
        global cooldowns
        cooldowns = cmds.copy()
        for item in cooldowns:
            cooldowns[item] = {}

        log.info("Ready.")

    async def on_message(self, message):
        if message.author.bot: return

        config = _stuffimporter.get_config()

        if message.content.startswith(config["prefix"]): # detection des commandes
            splitted = message.content.split(" ")
            cmd_or_alias = splitted[0][len(config["prefix"]):]
            args = splitted[1:] # séparation des arguments de la commande

            cmd = None
            for glob_comd in cmds.keys(): # trouver les aliases
                for alias in cmds[glob_comd]:
                    if cmd_or_alias == alias:
                        cmd = glob_comd

            if cmd: # si nom cmd utilisée existe
                user_id = message.author.id
                cmd_auth = getattr(commands, cmd).authorisation
                if cmd_auth != "everyone" and user_id != config[cmd_auth]:
                    return await message.channel.send("Vous n'avez pas le niveau d'accréditation nécéssaire pour executer cette commande.")

                # Système de cooldown
                global cooldowns
                if str(user_id) in cooldowns[cmd].keys(): # Vérification pour savoir si l'utilisateur est sur un cooldown ou pas
                    time_diff = cooldowns[cmd][str(user_id)] - time.time()
                    if time_diff > 0:
                        await message.reply(f"Vous êtes en cooldown, vous pourrez réutiliser cette commande dans **{round(time_diff, 2)}** secondes.")
                        return log.info(f"L'utilisateur {message.author} a essayé d'utiliser la commande {cmd} alors qu'il était en cooldown, il pourra réutiliser cette commande dans {time_diff} secondes.")
                
                temp = {}
                for curr_cmd, val in cooldowns.items(): # Check de tout les cooldowns pour voir si il y en a qui sont "périmés" (TODO : opti)
                    temp[curr_cmd] = {}
                    for us_id, cooldown in val.items():
                        if cooldown > time.time():
                            temp[curr_cmd][us_id] = cooldown
                cooldowns = temp.copy()

                try:
                    end_msg = await getattr(commands, cmd).execute(self, message, args)
                    wut_happ = f"le message de fin \"{end_msg}\""
                    log_levl = "info"
                except Exception as e:
                    await message.channel.send(f"Une erreur est survenue, voici le message d'erreur : {e}")
                    wut_happ = f"l'erreur {e}"
                    log_levl = "warn"

                # Ajout du cooldown
                try:
                    cooldowns[cmd][str(user_id)] = time.time() + getattr(commands, cmd).cooldown
                except AttributeError:
                    pass

                if args:
                    getattr(log, log_levl)(f"Commande \"{cmd}\" avec argument(s) \"{', '.join(args)}\" executée avec {wut_happ} par {message.author}.")
                else:
                    getattr(log, log_levl)(f"Commande \"{cmd}\" executée avec {wut_happ} par {message.author}.")

            else:
                await message.channel.send(f"Je ne reconnais pas cette commande, utilisez la commande help pour de l'aide.\nI don't know this command, please use the help command.")

bot = MyBot()
bot.run(_stuffimporter.get_config()["token"])

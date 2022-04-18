import json, discord

def get_config():
    with open("./config.json", "r", encoding="utf-8") as config_file:
        return json.load(config_file)

def set_config(config):
    with open("./config.json", "w", encoding="utf-8") as config_file:
        json.dump(config, config_file)
    return

def get_users():
    with open("./users.json", "r", encoding="utf-8") as users_file:
        temp = json.load(users_file)

    users = {}
    for item in temp:
        if type(temp[item]) == list:
            users[item] = set(temp[item])
        else:
            users[item] = temp[item]
    return users

def set_users(users):
    json_users = {}
    for item in users:
        if type(users[item]) == set:
            json_users[item] = list(users[item])
        else:
            json_users[item] = users[item]

    with open("./users.json", "w", encoding="utf-8") as users_file:
        json.dump(json_users, users_file)
    return

def get_all():
    return get_config(), get_users()

def set_all(config, users):
    set_config(config)
    set_users(users)
    return

async def get_discord_user(client, id):
    user = client.get_user(id)
    if user is None:
        user = await client.fetch_user(id)
    return user

async def get_dm_channel(user):
    channel = user.dm_channel
    if channel is None:
        channel = await user.create_dm()
    return user
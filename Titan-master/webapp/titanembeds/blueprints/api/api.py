from titanembeds.database import db, Guilds, UnauthenticatedUsers, UnauthenticatedBans, AuthenticatedUsers, get_administrators_list, get_badges, DiscordBotsOrgTransactions
from titanembeds.decorators import valid_session_required, discord_users_only, abort_if_guild_disabled
from titanembeds.utils import serializer, check_guild_existance, guild_accepts_visitors, guild_query_unauth_users_bool, get_client_ipaddr, discord_api, rate_limiter, channel_ratelimit_key, guild_ratelimit_key, user_unauthenticated, checkUserRevoke, checkUserBanned, update_user_status, check_user_in_guild, get_guild_channels, guild_webhooks_enabled, guild_unauthcaptcha_enabled, get_member_roles, get_online_embed_user_keys, redis_store, redisqueue, get_forced_role
from titanembeds.oauth import user_has_permission, generate_avatar_url, check_user_can_administrate_guild
import titanembeds.constants as constants
from flask import Blueprint, abort, jsonify, session, request, url_for
from flask import current_app as app
from flask_socketio import emit
from sqlalchemy import and_
from urllib.parse import urlparse, parse_qsl, urlsplit
import random
import json
import datetime
import re
import requests
from config import config
import copy

api = Blueprint("api", __name__)

@api.after_request
def after_request(response):
    if response.is_json:
        session_copy = copy.deepcopy(dict(session))
        data = response.get_json()
        data["session"] = serializer.dumps(session_copy)
        response.set_data(json.dumps(data))
    return response

@api.before_request
def before_request():
    authorization = request.headers.get("authorization", None)
    if authorization:
        try:
            data = serializer.loads(authorization)
            session.update(data)
        except:
            pass

def parse_emoji(textToParse, guild_id):
    guild_emojis = get_guild_emojis(guild_id)
    for gemoji in guild_emojis:
        emoji_name = gemoji["name"]
        emoji_id = gemoji["id"]
        emoji_animated = gemoji.get("animated", False)
        if emoji_animated:
            textToParse = textToParse.replace(":{}:".format(emoji_name), "<a:{}:{}>".format(emoji_name, emoji_id))
        else:
            textToParse = textToParse.replace(":{}:".format(emoji_name), "<:{}:{}>".format(emoji_name, emoji_id))
    return textToParse


def format_post_content(guild_id, channel_id, message, dbUser):
    illegal_post = False
    illegal_reasons = []
    message = message.replace("<", "\<")
    message = message.replace(">", "\>")
    message = parse_emoji(message, guild_id)

    dbguild = db.session.query(Guilds).filter(Guilds.guild_id == guild_id).first()

    max_len = get_post_content_max_len(guild_id)
    if len(message) > max_len:
        illegal_post = True
        illegal_reasons.append("Exceeded the following message length: {} characters".format(max_len))

    links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    if not dbguild.chat_links and len(links) > 0:
        illegal_post = True
        illegal_reasons.append("Links is not allowed.")
    elif dbguild.chat_links and not dbguild.bracket_links:
        for link in links:
            newlink = "<" + link + ">"
            message = message.replace(link, newlink)

    mention_pattern = re.compile(r'\[@[0-9]+\]')
    all_mentions = re.findall(mention_pattern, message)
    if dbguild.mentions_limit != -1 and len(all_mentions) > dbguild.mentions_limit:
        illegal_post = True
        illegal_reasons.append("Mentions is capped at the following limit: " + str(dbguild.mentions_limit))
    for match in all_mentions:
        mention = "<@" + match[2: len(match) - 1] + ">"
        message = message.replace(match, mention, 1)
    
    if dbguild.banned_words_enabled:
        banned_words = set(json.loads(dbguild.banned_words))
        if dbguild.banned_words_global_included:
            banned_words = banned_words.union(set(constants.GLOBAL_BANNED_WORDS))
        for word in banned_words:
            word_boundaried = r"\b%s\b" % word
            regex = re.compile(word_boundaried, re.IGNORECASE)
            if regex.search(message):
                illegal_post = True
                illegal_reasons.append("The following word is prohibited: " + word)
    
    if not guild_webhooks_enabled(guild_id):
        if (session['unauthenticated']):
            message = u"**[{}#{}]** {}".format(session['username'], session['user_id'], message)
        else:
            username = session['username']
            if dbUser:
                if dbUser["nick"]:
                    username = dbUser["nick"]
            message = u"**<{}#{}>** {}".format(username, session['discriminator'], message) # I would like to do a @ mention, but i am worried about notify spam
    return (message, illegal_post, illegal_reasons)

def format_everyone_mention(channel, content):
    if not channel["mention_everyone"]:
        if "@everyone" in content:
            content = content.replace("@everyone", u"@\u200Beveryone")
        if "@here" in content:
            content = content.replace("@here", u"@\u200Bhere")
    return content

def filter_guild_channel(guild_id, channel_id, force_everyone=False):
    forced_role = get_forced_role(guild_id)
    channels = get_guild_channels(guild_id, force_everyone, forced_role)
    for chan in channels:
        if chan["channel"]["id"] == channel_id:
            return chan
    return None

def get_online_discord_users(guild_id, embed):
    apimembers = redisqueue.list_guild_members(guild_id)
    apimembers_filtered = {}
    for member in apimembers:
        apimembers_filtered[int(member["id"])] = member
    guild_roles = redisqueue.get_guild(guild_id)["roles"]
    guildroles_filtered = {}
    for role in guild_roles:
        guildroles_filtered[role["id"]] = role
    for member in embed['members']:
        apimem = apimembers_filtered.get(int(member["id"]))
        member["hoist-role"] = None
        member["color"] = None
        if apimem:
            member["hoist-role"] = apimem["hoist-role"]
            member["color"] = apimem["color"]
            member["avatar"] = apimem["avatar"]
            member["avatar_url"] = apimem["avatar_url"]
    return embed['members']

def get_online_embed_users(guild_id):
    usrs = get_online_embed_user_keys(guild_id)
    unauths = db.session.query(UnauthenticatedUsers).filter(UnauthenticatedUsers.user_key.in_(usrs["UnauthenticatedUsers"]), UnauthenticatedUsers.revoked == False, UnauthenticatedUsers.guild_id == guild_id).all() if usrs["UnauthenticatedUsers"] else []
    auths = db.session.query(AuthenticatedUsers).filter(AuthenticatedUsers.client_id.in_(usrs["AuthenticatedUsers"]), AuthenticatedUsers.guild_id == guild_id).all() if usrs["AuthenticatedUsers"] else []
    users = {'unauthenticated':[], 'authenticated':[]}
    for user in unauths:
        meta = {
            'username': user.username,
            'discriminator': user.discriminator,
        }
        users['unauthenticated'].append(meta)
    for user in auths:
        client_id = user.client_id
        usrdb = redisqueue.get_guild_member(guild_id, client_id)
        meta = {
            'id': str(usrdb["id"]),
            'username': usrdb["username"],
            'nickname': usrdb["nick"],
            'discriminator': usrdb["discriminator"],
            'avatar_url': generate_avatar_url(usrdb["id"], usrdb["avatar"]),
        }
        users['authenticated'].append(meta)
    return users

def get_guild_emojis(guild_id):
    return redisqueue.get_guild(guild_id)["emojis"]

def get_guild_roles(guild_id):
    return redisqueue.get_guild(guild_id)["roles"]

# Returns webhook url if exists and can post w/webhooks, otherwise None
def get_channel_webhook_url(guild_id, channel_id):
    if not guild_webhooks_enabled(guild_id):
        return None
    guild = redisqueue.get_guild(guild_id)
    guild_webhooks = guild["webhooks"]
    name = "[Titan] "
    username = session["username"]
    if len(username) > 19:
        username = username[:19]
    if user_unauthenticated():
        name = name + username + "#" + str(session["user_id"])
    else:
        name = name + username + "#" + str(session["discriminator"])
    for webhook in guild_webhooks:
        if channel_id == webhook["channel_id"] and webhook["name"] == name:
            return {
                "id": webhook["id"],
                "token": webhook["token"],
                "name": webhook.get("name"),
                "guild_id": webhook.get("guild_id"),
                "channel_id": webhook.get("channel_id")
            }
    webhook = discord_api.create_webhook(channel_id, name)
    if webhook and "content" in webhook:
        return webhook["content"]
    else:
        return None
        
def delete_webhook_if_too_much(webhook):
    if not webhook:
        return
    guild_id = webhook["guild_id"]
    if guild_webhooks_enabled(guild_id):
        guild = redisqueue.get_guild(guild_id)
        guild_webhooks = guild["webhooks"]
        total_wh_cnt = len(guild_webhooks)
        titan_wh_cnt = 0
        for wh in guild_webhooks:
            if wh["name"].startswith("[Titan] "):
                titan_wh_cnt = titan_wh_cnt + 1
        if titan_wh_cnt > 0 and total_wh_cnt >= 8:
            try:
                discord_api.delete_webhook(webhook["id"], webhook["token"])
            except:
                pass # not my problem now

def get_all_users(guild_id):
    users = redisqueue.list_guild_members(guild_id)
    mem = []
    for u in users:
        mem.append({
            "id": str(u["id"]),
            "avatar": u["avatar"],
            "avatar_url": generate_avatar_url(u["id"], u["avatar"], u["discriminator"], True),
            "username": u["username"],
            "nickname": u["nick"],
            "discriminator": u["discriminator"]
        })
    return mem

@api.route("/fetch", methods=["GET"])
@valid_session_required(api=True)
@abort_if_guild_disabled()
@rate_limiter.limit("2 per 2 second", key_func = channel_ratelimit_key)
def fetch():
    guild_id = request.args.get("guild_id")
    channel_id = request.args.get('channel_id')
    after_snowflake = request.args.get('after', 0, type=int)
    if user_unauthenticated():
        key = session['user_keys'][guild_id]
    else:
        key = None
    status = update_user_status(guild_id, session['username'], key)
    messages = {}
    if status['banned'] or status['revoked']:
        status_code = 403
        if user_unauthenticated():
            session['user_keys'].pop(guild_id, None)
            session.modified = True
    else:
        chan = filter_guild_channel(guild_id, channel_id)
        if not chan:
            abort(404)
        if not chan.get("read") or chan["channel"]["type"] != "text":
            status_code = 401
        else:
            messages = redisqueue.get_channel_messages(guild_id, channel_id, after_snowflake)
            status_code = 200
    response = jsonify(messages=messages, status=status)
    response.status_code = status_code
    return response

@api.route("/fetch_visitor", methods=["GET"])
@abort_if_guild_disabled()
@rate_limiter.limit("2 per 2 second", key_func = channel_ratelimit_key)
def fetch_visitor():
    guild_id = request.args.get("guild_id")
    channel_id = request.args.get('channel_id')
    after_snowflake = request.args.get('after', 0, type=int)
    if not guild_accepts_visitors(guild_id):
        abort(403)
    messages = {}
    chan = filter_guild_channel(guild_id, channel_id, True)
    if not chan:
        abort(404)
    if not chan.get("read") or chan["channel"]["type"] != "text":
        status_code = 401
    else:
        messages = redisqueue.get_channel_messages(guild_id, channel_id, after_snowflake)
        status_code = 200
    response = jsonify(messages=messages)
    response.status_code = status_code
    return response

def get_guild_specific_post_limit():
    guild_id = request.form.get("guild_id", None)
    try:
        guild_id = int(guild_id)
    except:
        guild_id = None
    seconds = 5
    if guild_id:
        dbguild = db.session.query(Guilds).filter(Guilds.guild_id == guild_id).first()
        if dbguild:
            seconds = dbguild.post_timeout
    return "1 per {} second".format(seconds)

def get_post_content_max_len(guild_id):
    try:
        guild_id = int(guild_id)
    except:
        guild_id = None
    length = 350
    if guild_id:
        dbguild = db.session.query(Guilds).filter(Guilds.guild_id == guild_id).first()
        if dbguild:
            length = dbguild.max_message_length
    return length

@api.route("/post", methods=["POST"])
@valid_session_required(api=True)
@abort_if_guild_disabled()
@rate_limiter.limit(get_guild_specific_post_limit, key_func = channel_ratelimit_key)
def post():
    guild_id = request.form.get("guild_id")
    channel_id = request.form.get('channel_id')
    content = request.form.get('content', "")
    file = None
    if "file" in request.files:
        file = request.files["file"]
    if file and file.filename == "":
        file = None
    rich_embed = request.form.get("richembed", None)
    if rich_embed:
        rich_embed = json.loads(rich_embed)
    if "user_id" in session:
        dbUser = redisqueue.get_guild_member(guild_id, session["user_id"])
    else:
        dbUser = None
    if user_unauthenticated():
        key = session['user_keys'][guild_id]
    else:
        key = None
    content, illegal_post, illegal_reasons = format_post_content(guild_id, channel_id, content, dbUser)
    status = update_user_status(guild_id, session['username'], key)
    message = {}
    if illegal_post:
        status_code = 417
    if status['banned'] or status['revoked']:
        status_code = 401
    else:
        chan = filter_guild_channel(guild_id, channel_id)
        if not chan.get("write") or chan["channel"]["type"] != "text":
            status_code = 401
        elif (file and not chan.get("attach_files")) or (rich_embed and not chan.get("embed_links")):
            status_code = 406
        elif not illegal_post:
            userid = session["user_id"]
            content = format_everyone_mention(chan, content)
            webhook = get_channel_webhook_url(guild_id, channel_id)
            # if userid in get_administrators_list():
            #     content = "(Titan Dev) " + content
            if webhook:
                if (session['unauthenticated']):
                    username = session["username"]
                    if len(username) > 25:
                        username = username[:25]
                    username = username + "#" + str(session["user_id"])
                    avatar = url_for('static', filename='img/titanembeds_square.png', _external=True)
                    dbguild = db.session.query(Guilds).filter(Guilds.guild_id == guild_id).first()
                    if dbguild:
                        icon = dbguild.guest_icon
                        if icon:
                            avatar = icon
                else:
                    username = session["username"]
                    if dbUser:
                        if dbUser["nick"]:
                            username = dbUser["nick"]
                    # if content.startswith("(Titan Dev) "):
                    #     content = content[12:]
                    #     username = "(Titan Dev) " + username
                    if len(username) > 25:
                        username = username[:25]
                    username = username + "#" + str(session['discriminator'])
                    avatar = session['avatar']
                message = discord_api.execute_webhook(webhook.get("id"), webhook.get("token"), username, avatar, content, file, rich_embed)
                delete_webhook_if_too_much(webhook)
            else:
                message = discord_api.create_message(channel_id, content, file, rich_embed)
            status_code = message['code']
    db.session.commit()
    response = jsonify(message=message.get('content', message), status=status, illegal_reasons=illegal_reasons)
    response.status_code = status_code
    return response

def verify_captcha_request(captcha_response, ip_address):
    payload = {
        "secret": config["recaptcha-secret-key"],
        "response": captcha_response,
        "remoteip": ip_address,
    }
    if app.config["DEBUG"]:
        del payload["remoteip"]
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload).json()
    return r["success"]

@api.route("/create_unauthenticated_user", methods=["POST"])
@rate_limiter.limit("3 per 30 minute", key_func=guild_ratelimit_key)
@abort_if_guild_disabled()
def create_unauthenticated_user():
    session['unauthenticated'] = True
    username = request.form['username']
    guild_id = request.form['guild_id']
    ip_address = get_client_ipaddr()
    username = username.strip()
    if len(username) < 2 or len(username) > 32:
        abort(406)
    if not all(x.isalnum() or x.isspace() or "-" == x or "_" == x for x in username):
        abort(406)
    if not check_guild_existance(guild_id):
        abort(404)
    if not guild_query_unauth_users_bool(guild_id):
        abort(401)
    if guild_unauthcaptcha_enabled(guild_id):
        captcha_response = request.form['captcha_response']
        if not verify_captcha_request(captcha_response, request.remote_addr):
            abort(412)
    final_response = None
    if not checkUserBanned(guild_id, ip_address):
        session['username'] = username
        if 'user_id' not in session or len(str(session["user_id"])) > 4:
            session['user_id'] = random.randint(0,9999)
        user = UnauthenticatedUsers(guild_id, username, session['user_id'], ip_address)
        db.session.add(user)
        key = user.user_key
        if 'user_keys' not in session:
            session['user_keys'] = {guild_id: key}
        else:
            session['user_keys'][guild_id] = key
        session.permanent = False
        status = update_user_status(guild_id, username, key)
        final_response = jsonify(status=status)
    else:
        status = {'banned': True}
        response = jsonify(status=status)
        response.status_code = 403
        final_response = response
    db.session.commit()
    return final_response

@api.route("/change_unauthenticated_username", methods=["POST"])
@rate_limiter.limit("1 per 10 minute", key_func=guild_ratelimit_key)
@abort_if_guild_disabled()
def change_unauthenticated_username():
    username = request.form['username']
    guild_id = request.form['guild_id']
    ip_address = get_client_ipaddr()
    username = username.strip()
    if len(username) < 2 or len(username) > 32:
        abort(406)
    if not all(x.isalnum() or x.isspace() or "-" == x or "_" == x for x in username):
        abort(406)
    if not check_guild_existance(guild_id):
        abort(404)
    if not guild_query_unauth_users_bool(guild_id):
        abort(401)
    final_response = None
    if not checkUserBanned(guild_id, ip_address):
        if 'user_keys' not in session or guild_id not in session['user_keys'] or not session['unauthenticated']:
            abort(424)
        emitmsg = {"unauthenticated": True, "username": session["username"], "discriminator": session["user_id"]}
        session['username'] = username
        if 'user_id' not in session or len(str(session["user_id"])) > 4:
            session['user_id'] = random.randint(0,9999)
        user = UnauthenticatedUsers(guild_id, username, session['user_id'], ip_address)
        db.session.add(user)
        key = user.user_key
        session['user_keys'][guild_id] = key
        status = update_user_status(guild_id, username, key)
        emit("embed_user_disconnect", emitmsg, room="GUILD_"+guild_id, namespace="/gateway")
        final_response = jsonify(status=status)
    else:
        status = {'banned': True}
        response = jsonify(status=status)
        response.status_code = 403
        final_response = response
    db.session.commit()
    return final_response

def get_guild_guest_icon(guild_id):
    guest_icon = db.session.query(Guilds).filter(Guilds.guild_id == guild_id).first().guest_icon
    return guest_icon if guest_icon else url_for('static', filename='img/titanembeds_square.png')

def process_query_guild(guild_id, visitor=False):
    forced_role = get_forced_role(guild_id)
    channels = get_guild_channels(guild_id, visitor, forced_role=forced_role)
    discordmembers = [] # Discord members & embed members listed here is moved to its own api endpoint
    embedmembers = {"authenticated": [], "unauthenticated": []} 
    emojis = get_guild_emojis(guild_id)
    roles = get_guild_roles(guild_id)
    guest_icon = get_guild_guest_icon(guild_id)
    if visitor:
        for channel in channels:
            channel["write"] = False
    return jsonify(channels=channels, discordmembers=discordmembers, embedmembers=embedmembers, emojis=emojis, roles=roles, guest_icon=guest_icon, instant_invite=None)

@api.route("/query_guild", methods=["GET"])
@valid_session_required(api=True)
@abort_if_guild_disabled()
def query_guild():
    guild_id = request.args.get('guild_id')
    if check_guild_existance(guild_id):
        if check_user_in_guild(guild_id):
            return process_query_guild(guild_id)
        abort(403)
    abort(404)

@api.route("/query_guild_visitor", methods=["GET"])
@abort_if_guild_disabled()
def query_guild_visitor():
    guild_id = request.args.get('guild_id')
    if check_guild_existance(guild_id):
        if not guild_accepts_visitors(guild_id):
            abort(403)
        return process_query_guild(guild_id, True)
    abort(404)
    
@api.route("/server_members", methods=["GET"])
@abort_if_guild_disabled()
@valid_session_required(api=True)
def server_members():
    abort(404)
    guild_id = request.args.get("guild_id", None)
    if not check_guild_existance(guild_id):
        abort(404)
    if not check_user_in_guild(guild_id):
        abort(403)
    members = query_server_members(guild_id)
    return jsonify(members)

@api.route("/server_members_visitor", methods=["GET"])
@abort_if_guild_disabled()
def server_members_visitor():
    abort(404)
    guild_id = request.args.get("guild_id", None)
    if not check_guild_existance(guild_id):
        abort(404)
    if not guild_accepts_visitors(guild_id):
        abort(403)
    members = query_server_members(guild_id)
    return jsonify(members)

def query_server_members(guild_id):
    widget = discord_api.get_widget(guild_id)
    if widget.get("success", True):
        discordmembers = get_online_discord_users(guild_id, widget)
        widgetenabled = True
    else:
        discordmembers = [{"id": 0, "color": "FFD6D6", "status": "dnd", "username": "Discord Server Widget is Currently Disabled"}]
        widgetenabled = False
    embedmembers = get_online_embed_users(guild_id)
    return {"discordmembers": discordmembers, "embedmembers": embedmembers, "widgetenabled": widgetenabled}

@api.route("/create_authenticated_user", methods=["POST"])
@discord_users_only(api=True)
@abort_if_guild_disabled()
def create_authenticated_user():
    guild_id = request.form.get('guild_id')
    if session['unauthenticated']:
        response = jsonify(error=True)
        response.status_code = 401
        return response
    else:
        if not check_guild_existance(guild_id):
            abort(404)
        if not check_user_in_guild(guild_id):
            add_member = discord_api.add_guild_member(guild_id, session['user_id'], session['user_keys']['access_token'])
            if not add_member["success"]:
                discord_status_code = add_member["content"].get("code", 0)
                if discord_status_code == 40007: # user banned from server
                    status = {'banned': True}
                    response = jsonify(status=status)
                    response.status_code = 403
                else:
                    response = jsonify(add_member)
                    response.status_code = 422
                return response
        db_user = db.session.query(AuthenticatedUsers).filter(and_(AuthenticatedUsers.guild_id == guild_id, AuthenticatedUsers.client_id == session['user_id'])).first()
        if not db_user:
            db_user = AuthenticatedUsers(guild_id, session['user_id'])
            db.session.add(db_user)
            db.session.commit()
        status = update_user_status(guild_id, session['username'])
        return jsonify(status=status)
            
@api.route("/user/<guild_id>/<user_id>")
@abort_if_guild_disabled()
def user_info(guild_id, user_id):
    usr = {
        "id": None,
        "username": None,
        "nickname": None,
        "discriminator": None,
        "avatar": None,
        "avatar_url": None,
        "roles": [],
        "badges": [],
    }
    member = redisqueue.get_guild_member(guild_id, user_id)
    if member:
        usr["id"] = str(member["id"])
        usr["username"] = member["username"]
        usr["nickname"] = member["nick"]
        usr["discriminator"] = member["discriminator"]
        usr["avatar"] = member["avatar"]
        usr["avatar_url"] = generate_avatar_url(usr["id"], usr["avatar"], usr["discriminator"], True)
        roles = get_member_roles(guild_id, user_id)
        guild_roles = redisqueue.get_guild(guild_id)["roles"]
        for r in roles:
            for gr in guild_roles:
                if gr["id"] == r:
                    usr["roles"].append(gr)
        usr["badges"] = get_badges(user_id)
        if redis_store.get("DiscordBotsOrgVoted/" + str(member["id"])):
            usr["badges"].append("discordbotsorgvoted")
    return jsonify(usr)

@api.route("/user/<guild_id>")
@abort_if_guild_disabled()
@valid_session_required(api=True)
def list_users(guild_id):
    all_users = get_all_users(guild_id)
    return jsonify(all_users)
    
@api.route("/webhook/discordbotsorg/vote", methods=["POST"])
def webhook_discordbotsorg_vote():
    incoming = request.get_json()
    client_id = incoming.get('bot')
    if str(config["client-id"]) != str(client_id):
        abort(401)
    if str(request.headers.get("Authorization", "")) != str(config.get("discordbotsorg-webhook-secret", "")):
        abort(403)
    user_id = str(incoming.get("user"))
    vote_type = str(incoming.get("type"))
    params = dict(parse_qsl(urlsplit(incoming.get("query", "")).query))
    if vote_type == "upvote":
        redis_store.set("DiscordBotsOrgVoted/" + user_id, "voted", 86400)
    referrer = None
    if "referrer" in params:
        try:
            referrer = int(params["referrer"])
        except:
            pass
    DBLTrans = DiscordBotsOrgTransactions(int(user_id), vote_type, referrer)
    db.session.add(DBLTrans)
    db.session.commit()
    return ('', 204)

@api.route("/bot/ban", methods=["POST"])
def bot_ban():
    if request.headers.get("Authorization", "") != config.get("app-secret", ""):
        return jsonify(error="Authorization header does not match."), 403
    incoming = request.get_json()
    guild_id = incoming.get("guild_id", None)
    placer_id = incoming.get("placer_id", None)
    username = incoming.get("username", None)
    discriminator = incoming.get("discriminator", None)
    if not guild_id or not placer_id or not username:
        return jsonify(error="Missing required parameters."), 400
    if discriminator:
        dbuser = db.session.query(UnauthenticatedUsers) \
            .filter(UnauthenticatedUsers.guild_id == str(guild_id)) \
            .filter(UnauthenticatedUsers.username.ilike("%" + username + "%")) \
            .filter(UnauthenticatedUsers.discriminator == discriminator) \
            .order_by(UnauthenticatedUsers.id.desc()).first()
    else:
        dbuser = db.session.query(UnauthenticatedUsers) \
            .filter(UnauthenticatedUsers.guild_id == str(guild_id)) \
            .filter(UnauthenticatedUsers.username.ilike("%" + username + "%")) \
            .order_by(UnauthenticatedUsers.id.desc()).first()
    if not dbuser:
        return jsonify(error="Guest user cannot be found."), 404
    dbban = db.session.query(UnauthenticatedBans) \
        .filter(UnauthenticatedBans.guild_id == str(guild_id)) \
        .filter(UnauthenticatedBans.last_username == dbuser.username) \
        .filter(UnauthenticatedBans.last_discriminator == dbuser.discriminator).first()
    if dbban is not None:
        if dbban.lifter_id is None:
            return jsonify(error="Guest user, **{}#{}**, has already been banned.".format(dbban.last_username, dbban.last_discriminator)), 409
        db.session.delete(dbban)
    dbban = UnauthenticatedBans(str(guild_id), dbuser.ip_address, dbuser.username, dbuser.discriminator, "", int(placer_id))
    db.session.add(dbban)
    db.session.commit()
    return jsonify(success="Guest user, **{}#{}**, has successfully been added to the ban list!".format(dbban.last_username, dbban.last_discriminator))
    
@api.route("/bot/unban", methods=["POST"])
def bot_unban():
    if request.headers.get("Authorization", "") != config.get("app-secret", ""):
        return jsonify(error="Authorization header does not match."), 403
    incoming = request.get_json()
    guild_id = incoming.get("guild_id", None)
    lifter_id = incoming.get("lifter_id", None)
    username = incoming.get("username", None)
    discriminator = incoming.get("discriminator", None)
    if not guild_id or not lifter_id or not username:
        return jsonify(error="Missing required parameters."), 400
    if discriminator:
        dbuser = db.session.query(UnauthenticatedUsers) \
            .filter(UnauthenticatedUsers.guild_id == str(guild_id)) \
            .filter(UnauthenticatedUsers.username.ilike("%" + username + "%")) \
            .filter(UnauthenticatedUsers.discriminator == discriminator) \
            .order_by(UnauthenticatedUsers.id.desc()).first()
    else:
        dbuser = db.session.query(UnauthenticatedUsers) \
            .filter(UnauthenticatedUsers.guild_id == str(guild_id)) \
            .filter(UnauthenticatedUsers.username.ilike("%" + username + "%")) \
            .order_by(UnauthenticatedUsers.id.desc()).first()
    if not dbuser:
        return jsonify(error="Guest user cannot be found."), 404
    dbban = db.session.query(UnauthenticatedBans) \
        .filter(UnauthenticatedBans.guild_id == str(guild_id)) \
        .filter(UnauthenticatedBans.ip_address == dbuser.ip_address).first()
    if dbban is None:
        return jsonify(error="Guest user **{}#{}** has not been banned.".format(dbuser.username, dbuser.discriminator)), 404
    if dbban.lifter_id is not None:
        return jsonify(error="Guest user **{}#{}** ban has already been removed.".format(dbuser.username, dbuser.discriminator)), 409
    dbban.liftBan(int(lifter_id))
    db.session.commit()
    return jsonify(success="Guest user, **{}#{}**, has successfully been removed from the ban list!".format(dbuser.username, dbuser.discriminator))

@api.route("/bot/revoke", methods=["POST"])
def bot_revoke():
    if request.headers.get("Authorization", "") != config.get("app-secret", ""):
        return jsonify(error="Authorization header does not match."), 403
    incoming = request.get_json()
    guild_id = incoming.get("guild_id", None)
    username = incoming.get("username", None)
    discriminator = incoming.get("discriminator", None)
    if not guild_id or not username:
        return jsonify(error="Missing required parameters."), 400
    if discriminator:
        dbuser = db.session.query(UnauthenticatedUsers) \
            .filter(UnauthenticatedUsers.guild_id == str(guild_id)) \
            .filter(UnauthenticatedUsers.username.ilike("%" + username + "%")) \
            .filter(UnauthenticatedUsers.discriminator == discriminator) \
            .order_by(UnauthenticatedUsers.id.desc()).first()
    else:
        dbuser = db.session.query(UnauthenticatedUsers) \
            .filter(UnauthenticatedUsers.guild_id == str(guild_id)) \
            .filter(UnauthenticatedUsers.username.ilike("%" + username + "%")) \
            .order_by(UnauthenticatedUsers.id.desc()).first()
    if not dbuser:
        return jsonify(error="Guest user cannot be found."), 404
    elif dbuser.revoked:
        return jsonify(error="Guest user **{}#{}** has already been kicked!".format(dbuser.username, dbuser.discriminator)), 409
    dbuser.revoked = True
    db.session.commit()
    return jsonify(success="Successfully kicked **{}#{}**!".format(dbuser.username, dbuser.discriminator))

@api.route("/bot/members")
def bot_members():
    if request.headers.get("Authorization", "") != config.get("app-secret", ""):
        return jsonify(error="Authorization header does not match."), 403
    guild_id = request.args.get("guild_id")
    members = get_online_embed_users(guild_id)
    return jsonify(members)

@api.route("/af/direct_message", methods=["POST"])
def af_direct_message_post():
    cs = request.form.get('cs', None)
    input = request.form.get('input')
    cleverbot_url = "http://www.cleverbot.com/getreply"
    payload = {'key': config["cleverbot-api-key"], 'cs': cs, 'input': input}
    r = requests.get(cleverbot_url, params=payload)
    return jsonify(r.json())

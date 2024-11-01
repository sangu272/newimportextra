from secrets import choice
from html import escape
from traceback import format_exc

from pyrogram import enums, filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors import ChatAdminRequired, RPCError
from pyrogram.types import ChatMemberUpdated, Message

from BADMUSIC.logging import LOGGERR
from BADMUSIC import app
from BADMUSIC.utils.decorators import AdminRightsCheck
from BADMUSIC.utils.permissions import adminsOnly

from BADMUSIC.utils.welcome.antispam_db import GBan
from BADMUSIC.utils.welcome.greetings_db import Greetings
from BADMUSIC.utils.welcome.supports import get_support_staff
from BADMUSIC.utils.welcome.cmd_senders import send_cmd
from BADMUSIC.utils.welcome.kbhelpers import ikb
from BADMUSIC.utils.welcome.msg_types import Types, get_wlcm_type
from BADMUSIC.utils.welcome.parser import escape_markdown, mention_html
from BADMUSIC.utils.welcome.string import (build_keyboard, escape_invalid_curly_brackets,
                                 parse_button)
import config

# Initialize
gdb = GBan()

DEV_USERS = get_support_staff("dev")

ChatType = enums.ChatType


async def escape_mentions_using_curly_brackets_wl(
    m: ChatMemberUpdated,
    n: bool,
    text: str,
    parse_words: list,
) -> str:
    teks = await escape_invalid_curly_brackets(text, parse_words)
    if n:
        user = m.new_chat_member.user if m.new_chat_member else m.from_user
    else:
        user = m.old_chat_member.user if m.old_chat_member else m.from_user
    if teks:
        teks = teks.format(
            first=escape(user.first_name),
            last=escape(user.last_name or user.first_name),
            fullname=" ".join(
                [
                    escape(user.first_name),
                    escape(user.last_name),
                ]
                if user.last_name
                else [escape(user.first_name)],
            ),
            username=(
                "@" + (await escape_markdown(escape(user.username)))
                if user.username
                else (await (mention_html(escape(user.first_name), user.id)))
            ),
            mention=await (mention_html(escape(user.first_name), user.id)),
            chatname=escape(m.chat.title)
            if m.chat.type != ChatType.PRIVATE
            else escape(user.first_name),
            id=user.id,
        )
    else:
        teks = ""

    return teks

@app.on_message(
    filters.command(["cleanwelcome"]))
@adminsOnly("can_restrict_members")
async def cleanwlcm(_, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_current_cleanwelcome_settings()
    args = m.text.split(" ", 1)

    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleanwelcome_settings(True)
            await m.reply_text("ᴛᴜʀɴᴇᴅ ᴏɴ!")
            return
        if args[1].lower() == "off":
            db.set_current_cleanwelcome_settings(False)
            await m.reply_text("ᴛᴜʀɴᴇᴅ ᴏꜰꜰ!")
            return
        await m.reply_text("ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏ ??")
        return
    await m.reply_text(f"ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:- {status}")
    return

@app.on_message(
    filters.command(["cleangoodbye"]))
@adminsOnly("can_restrict_members")
async def cleangdbye(_, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_current_cleangoodbye_settings()
    args = m.text.split(" ", 1)

    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleangoodbye_settings(True)
            await m.reply_text("ᴛᴜʀɴᴇᴅ ᴏɴ!")
            return
        if args[1].lower() == "off":
            db.set_current_cleangoodbye_settings(False)
            await m.reply_text("ᴛᴜʀɴᴇᴅ ᴏꜰꜰ!")
            return
        await m.reply_text("ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏ ??")
        return
    await m.reply_text(f"ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:- {status}")
    return

@app.on_message(
    filters.command(["cleanservice"]))
@adminsOnly("can_restrict_members")
async def cleanservice(_, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_current_cleanservice_settings()
    args = m.text.split(" ", 1)

    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleanservice_settings(True)
            await m.reply_text("ᴛᴜʀɴᴇᴅ ᴏɴ!")
            return
        if args[1].lower() == "off":
            db.set_current_cleanservice_settings(False)
            await m.reply_text("ᴛᴜʀɴᴇᴅ ᴏꜰꜰ!")
            return
        await m.reply_text("ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏ ??")
        return
    await m.reply_text(f"ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:- {status}")
    return


@app.on_message(
    filters.command(["setwelcome"]))
@adminsOnly("can_restrict_members")
async def save_wlcm(_, m: Message):
    db = Greetings(m.chat.id)
    if m and not m.from_user:
        return
    args = m.text.split(None, 1)

    if len(args) >= 4096:
        await m.reply_text(
            "ᴡᴏʀᴅ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅ !!",
        )
        return
    if not (m.reply_to_message and m.reply_to_message.text) and len(m.command) == 0:
        await m.reply_text(
            "ᴇʀʀᴏʀ: ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴛᴇxᴛ ɪɴ ʜᴇʀᴇ! ᴀɴᴅ ᴏɴʟʏ ᴛᴇxᴛ ᴡɪᴛʜ ʙᴜᴛᴛᴏɴꜱ ᴀʀᴇ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴄᴜʀʀᴇɴᴛʟʏ !",
        )
        return
    text, msgtype, file = await get_wlcm_type(m)
    if not m.reply_to_message and msgtype == Types.TEXT and len(m.command) <= 2:
        await m.reply_text(f"<code>{m.text}</code>\n\nᴇʀʀᴏʀ: ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴅᴀᴛᴀ ɪɴ ʜᴇʀᴇ!")
        return

    if not text and not file:
        await m.reply_text(
            "ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ꜱᴏᴍᴇ ᴅᴀᴛᴀ!",
        )
        return

    if not msgtype:
        await m.reply_text("ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ꜱᴏᴍᴇ ᴅᴀᴛᴀ ꜰᴏʀ ᴛʜɪꜱ ᴛᴏ ʀᴇᴘʟʏ ᴡɪᴛʜ!")
        return

    db.set_welcome_text(text,msgtype,file)
    await m.reply_text("ꜱᴀᴠᴇᴅ ᴡᴇʟᴄᴏᴍᴇ 🎉")
    return

@app.on_message(
    filters.command(["setgoodbye"]))
@adminsOnly("can_restrict_members")
async def save_gdbye(_, m: Message):
    db = Greetings(m.chat.id)
    if m and not m.from_user:
        return
    args = m.text.split(None, 1)

    if len(args) >= 4096:
        await m.reply_text(
            "ᴡᴏʀᴅ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅꜱ !!",
        )
        return
    if not (m.reply_to_message and m.reply_to_message.text) and len(m.command) == 0:
        await m.reply_text(
            "ᴇʀʀᴏʀ: ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴛᴇxᴛ ɪɴ ʜᴇʀᴇ! ᴀɴᴅ ᴏɴʟʏ ᴛᴇxᴛ ᴡɪᴛʜ ʙᴜᴛᴛᴏɴꜱ ᴀʀᴇ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴄᴜʀʀᴇɴᴛʟʏ !",
        )
        return
    text, msgtype, file = await get_wlcm_type(m)

    if not m.reply_to_message and msgtype == Types.TEXT and len(m.command) <= 2:
        await m.reply_text(f"<code>{m.text}</code>\n\nᴇʀʀᴏʀ: ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴅᴀᴛᴀ ɪɴ ʜᴇʀᴇ!")
        return

    if not text and not file:
        await m.reply_text(
            "ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ꜱᴏᴍᴇ ᴅᴀᴛᴀ!",
        )
        return

    if not msgtype:
        await m.reply_text("ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ꜱᴏᴍᴇ ᴅᴀᴛᴀ ꜰᴏʀ ᴛʜɪꜱ ᴛᴏ ʀᴇᴘʟʏ ᴡɪᴛʜ!")
        return

    db.set_goodbye_text(text,msgtype,file)
    await m.reply_text("ꜱᴀᴠᴇᴅ ɢᴏᴏᴅʙʏᴇ 🎉")
    return


@app.on_message(
    filters.command(["resetgoodbye"]))
@adminsOnly("can_restrict_members")
async def resetgb(_, m: Message):
    db = Greetings(m.chat.id)
    if m and not m.from_user:
        return
    text = "sᴀᴅ ᴛᴏ sᴇᴇ ʏᴏᴜ ʟᴇᴀᴠɪɴɢ {first}.\ ᴛᴀᴋᴇ ᴄᴀʀᴇ! 🌸"
    db.set_goodbye_text(text,None)
    await m.reply_text("Ok Done!")
    return

@app.on_message(
    filters.command(["resetwelcome"]))
@adminsOnly("can_restrict_members")
async def resetwlcm(_, m: Message):
    db = Greetings(m.chat.id)
    if m and not m.from_user:
        return
    text = "ʜᴇʏ {first}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {chatname} 🥀!"
    db.set_welcome_text(text,None)
    await m.reply_text("Done!")
    return


@app.on_message(filters.service & filters.group, group=59)
async def cleannnnn(_, m: Message):
    db = Greetings(m.chat.id)
    clean = db.get_current_cleanservice_settings()
    try:
        if clean:
            await m.delete()
    except Exception:
        pass


@app.on_chat_member_updated(filters.group, group=69)
async def member_has_joined(c: app, member: ChatMemberUpdated):

    if (
        member.new_chat_member
        and member.new_chat_member.status not in {CMS.BANNED, CMS.LEFT, CMS.RESTRICTED}
        and not member.old_chat_member
    ):
        pass
    else:
        return

    user = member.new_chat_member.user if member.new_chat_member else member.from_user

    db = Greetings(member.chat.id)
    banned_users = gdb.check_gban(user.id)
    try:
        if user.id == config.BOT_ID:
            return
        if user.id in DEV_USERS:
            await c.send_animation(
                chat_id=member.chat.id,
                animation="./BADMUSIC/welcome/william (1).gif",
                caption="ᴍʏ ᴏᴡɴᴇʀ ɪs ʜᴇʀᴇ 🌸🙈❤️",
            )
            return
        if banned_users:
            await member.chat.ban_member(user.id)
            await c.send_message(
                member.chat.id,
                f"{user.mention} ᴡᴀꜱ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ꜱᴏ ɪ ʙᴀɴɴᴇᴅ!",
            )
            return
        if user.is_bot:
            return  # ignore bots
    except ChatAdminRequired:
        return
    status = db.get_welcome_status()
    oo = db.get_welcome_text()
    UwU = db.get_welcome_media()
    mtype = db.get_welcome_msgtype()
    parse_words = [
        "first",
        "last",
        "fullname",
        "username",
        "mention",
        "id",
        "chatname",
    ]
    hmm = await escape_mentions_using_curly_brackets_wl(member, True, oo, parse_words)
    if status:
        tek, button = await parse_button(hmm)
        button = await build_keyboard(button)
        button = ikb(button) if button else None

        if "%%%" in tek:
            filter_reply = tek.split("%%%")
            teks = choice(filter_reply)
        else:
            teks = tek
        ifff = db.get_current_cleanwelcome_id()
        gg = db.get_current_cleanwelcome_settings()
        if ifff and gg:
            try:
                await c.delete_messages(member.chat.id, int(ifff))
            except RPCError:
                pass
        if not teks:
            teks = "ʜᴇʏ {first}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {chatname} 🥀"
        try:
            if not UwU:
                jj = await c.send_message(
                    member.chat.id,
                    text=teks,
                    reply_markup=button,
                    disable_web_page_preview=True,
                )
            elif UwU:
                jj = await (await send_cmd(c,mtype))(
                    member.chat.id,
                    UwU,
                    caption=teks,
                    reply_markup=button,
                )

            if jj:
                db.set_cleanwlcm_id(int(jj.id))
        except RPCError as e:
            LOGGER.error(e)
            LOGGER.error(format_exc(e))
            return
    else:
        return


@app.on_chat_member_updated(filters.group, group=99)
async def member_has_left(c: app, member: ChatMemberUpdated):

    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {CMS.BANNED, CMS.RESTRICTED}
        and member.old_chat_member
    ):
        pass
    else:
        return
    db = Greetings(member.chat.id)
    status = db.get_goodbye_status()
    oo = db.get_goodbye_text()
    UwU = db.get_goodbye_media()
    mtype = db.get_goodbye_msgtype()
    parse_words = [
        "first",
        "last",
        "fullname",
        "id",
        "username",
        "mention",
        "chatname",
    ]

    user = member.old_chat_member.user if member.old_chat_member else member.from_user

    hmm = await escape_mentions_using_curly_brackets_wl(member, False, oo, parse_words)
    if status:
        tek, button = await parse_button(hmm)
        button = await build_keyboard(button)
        button = ikb(button) if button else None

        if "%%%" in tek:
            filter_reply = tek.split("%%%")
            teks = choice(filter_reply)
        else:
            teks = tek
        ifff = db.get_current_cleangoodbye_id()
        iii = db.get_current_cleangoodbye_settings()
        if ifff and iii:
            try:
                await c.delete_messages(member.chat.id, int(ifff))
            except RPCError:
                pass
        if user.id in DEV_USERS:
            await c.send_message(
                member.chat.id,
                "ᴡɪʟʟ ᴍɪꜱꜱ ʏᴏᴜ ᴍᴀꜱᴛᴇʀ 🙁",
            )
            return
        if not teks:
            teks = "sᴀᴅ ᴛᴏ sᴇᴇ ʏᴏᴜ ʟᴇᴀᴠɪɴɢ {first}.\ ᴛᴀᴋᴇ ᴄᴀʀᴇ! 🌸"
        try:
            if not UwU:
                ooo = await c.send_message(
                    member.chat.id,
                    text=teks,
                    reply_markup=button,
                    disable_web_page_preview=True,
                )
            elif UwU:
                ooo = await (await send_cmd(c,mtype))(
                    member.chat.id,
                    UwU,
                    caption=teks,
                    reply_markup=button,
                )

            if ooo:
                db.set_cleangoodbye_id(int(ooo.id))
            return
        except RPCError as e:
            LOGGER.error(e)
            LOGGER.error(format_exc(e))
            return
    else:
        return


@app.on_message(
    filters.command(["welcome"]))
@adminsOnly("can_restrict_members")
async def welcome(c: app, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_welcome_status()
    oo = db.get_welcome_text()
    args = m.text.split(" ", 1)

    if m and not m.from_user:
        return

    if len(args) >= 2:
        if args[1].lower() == "noformat":
            await m.reply_text(
                f"""ᴄᴜʀʀᴇɴᴛ ᴡᴇʟᴄᴏᴍᴇ ꜱᴇᴛᴛɪɴɢꜱ:-
            ᴡᴇʟᴄᴏᴍᴇ ᴘᴏᴡᴇʀ: {status}
            ᴄʟᴇᴀɴ ᴡᴇʟᴄᴏᴍᴇ: {db.get_current_cleanwelcome_settings()}
            ᴄʟᴇᴀɴɪɴɢ ꜱᴇʀᴠɪᴄᴇ: {db.get_current_cleanservice_settings()}
            ᴡᴇʟᴄᴏᴍᴇ ᴛᴇxᴛ ɪɴ ɴᴏ ꜰᴏʀᴍᴀᴛɪɴɢ:
            """,
            )
            await c.send_message(
                m.chat.id, text=oo, parse_mode=enums.ParseMode.DISABLED
            )
            return
        if args[1].lower() == "on":
            db.set_current_welcome_settings(True)
            await m.reply_text("ɪ ᴡɪʟʟ ɢʀᴇᴇᴛ ɴᴇᴡʟʏ ᴊᴏɪɴᴇᴅ ᴍᴇᴍʙᴇʀ ꜰʀᴏᴍ ɴᴏᴡ ᴏɴ 👻")
            return
        if args[1].lower() == "off":
            db.set_current_welcome_settings(False)
            await m.reply_text("ɪ ᴡɪʟʟ ꜱᴛᴀʏ Qᴜɪᴇᴛ ᴡʜᴇɴ ꜱᴏᴍᴇᴏɴᴇ ᴊᴏɪɴꜱ🥺")
            return
        await m.reply_text("ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏ ??")
        return
    await m.reply_text(
        f"""ᴄᴜʀʀᴇɴᴛ ᴡᴇʟᴄᴏᴍᴇ ꜱᴇᴛᴛɪɴɢꜱ:-
    ᴡᴇʟᴄᴏᴍᴇ ᴘᴏᴡᴇʀ: {status}
    ᴄʟᴇᴀɴ ᴡᴇʟᴄᴏᴍᴇ: {db.get_current_cleanwelcome_settings()}
    ᴄʟᴇᴀɴɪɴɢ ꜱᴇʀᴠɪᴄᴇ: {db.get_current_cleanservice_settings()}
    ᴡᴇʟᴄᴏᴍᴇ ᴛᴇxᴛ:
    """,
    )
    UwU = db.get_welcome_media()
    mtype = db.get_welcome_msgtype()
    tek, button = await parse_button(oo)
    button = await build_keyboard(button)
    button = ikb(button) if button else None
    if not UwU:
            await c.send_message(
            m.chat.id,
            text=tek,
            reply_markup=button,
            disable_web_page_preview=True,
        )
    elif UwU:
            await (await send_cmd(c,mtype))(
            m.chat.id,
            UwU,
            caption=tek,
            reply_markup=button,
        )
    return


@app.on_message(
    filters.command(["goodbye"]))
@adminsOnly("can_restrict_members")
async def goodbye(c: app, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_goodbye_status()
    oo = db.get_goodbye_text()
    args = m.text.split(" ", 1)
    if m and not m.from_user:
        return
    if len(args) >= 2:
        if args[1].lower() == "noformat":
            await m.reply_text(
                f"""ᴄᴜʀʀᴇɴᴛ ɢᴏᴏᴅʙʏᴇ ꜱᴇᴛᴛɪɴɢꜱ:-
            ɢᴏᴏᴅʙʏᴇ ᴘᴏᴡᴇʀ: {status}
            ᴄʟᴇᴀɴ ɢᴏᴏᴅʙʏᴇ: {db.get_current_cleangoodbye_settings()}
            ᴄʟᴇᴀɴɪɴɢ ꜱᴇʀᴠɪᴄᴇ: {db.get_current_cleanservice_settings()}
            ɢᴏᴏᴅʙʏᴇ ᴛᴇxᴛ ɪɴ ɴᴏ ꜰᴏʀᴍᴀᴛɪɴɢ:
            """,
            )
            await c.send_message(
                m.chat.id, text=oo, parse_mode=enums.ParseMode.DISABLED
            )
            return
        if args[1].lower() == "on":
            db.set_current_goodbye_settings(True)
            await m.reply_text("ɪ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ʙᴜᴛ ɪ ᴡɪʟʟ ꜱᴀʏ ɢᴏᴏᴅʙʏᴇ ᴛᴏ ᴛʜᴇ ꜰᴜɢɪᴛɪᴠᴇꜱ")
            return
        if args[1].lower() == "off":
            db.set_current_goodbye_settings(False)
            await m.reply_text("ɪ ᴡɪʟʟ ꜱᴛᴀʏ Qᴜɪᴇᴛ ꜰᴏʀ ꜰᴜɢɪᴛɪᴠᴇꜱ")
            return
        await m.reply_text("ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏ ??")
        return
    await m.reply_text(
        f"""ᴄᴜʀʀᴇɴᴛ ɢᴏᴏᴅʙʏᴇ ꜱᴇᴛᴛɪɴɢꜱ:-
    ɢᴏᴏᴅʙʏᴇ ᴘᴏᴡᴇʀ: {status}
    ᴄʟᴇᴀɴ ɢᴏᴏᴅʙʏᴇ: {db.get_current_cleangoodbye_settings()}
    ᴄʟᴇᴀɴɪɴɢ ꜱᴇʀᴠɪᴄᴇ: {db.get_current_cleanservice_settings()}
    ɢᴏᴏᴅʙʏᴇ ᴛᴇxᴛ:
    """,
    )
    UwU = db.get_goodbye_media()
    mtype = db.get_goodbye_msgtype()
    tek, button = await parse_button(oo)
    button = await build_keyboard(button)
    button = ikb(button) if button else None
    if not UwU:
            await c.send_message(
            m.chat.id,
            text=tek,
            reply_markup=button,
            disable_web_page_preview=True,
        )
    elif UwU:
            await (await send_cmd(c,mtype))(
            m.chat.id,
            UwU,
            caption=tek,
            reply_markup=button,
        )
    return
    return

  

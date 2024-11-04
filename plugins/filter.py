import re
from BADMUSIC import app
from config import BOT_USERNAME
from BADMUSIC.utils.bad_ban import admin_filter
from utils.filtersdb import *
from config import BANNED_USERS
from BADMUSIC.utils.filters_func import GetFIlterMessage, get_text_reason, SendFilterMessage
from BADMUSIC.utils.admin import user_admin
from pyrogram import filters
from utils.permissions import adminsOnly, member_permissions
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from BADMUSIC.utils.database import (
    deleteall_filters,
    get_filter,
    get_filters_names,
    save_filter,
)

@app.on_message(filters.command("filter") & admin_filter)
@user_admin
async def _filter(client, message):
    
    chat_id = message.chat.id 
    if (
        message.reply_to_message
        and not len(message.command) == 2
    ):
        await message.reply("You need to give the filter a name!")  
        return 
    
    filter_name, filter_reason = get_text_reason(message)
    if (
        message.reply_to_message
        and not len(message.command) >=2
    ):
        await message.reply("You need to give the filter some content!")
        return

    content, text, data_type = await GetFIlterMessage(message)
    await add_filter_db(chat_id, filter_name=filter_name, content=content, text=text, data_type=data_type)
    await message.reply(
        f"Saved filter '`{filter_name}`'."
    )


@app.on_message(~filters.bot & filters.group, group=4)
async def FilterCheckker(client, message):
    if not message.text:
        return
    text = message.text
    chat_id = message.chat.id
    if (
        len(await get_filters_list(chat_id)) == 0
    ):
        return

    ALL_FILTERS = await get_filters_list(chat_id)
    for filter_ in ALL_FILTERS:
        
        if (
            message.command
            and message.command[0] == 'filter'
            and len(message.command) >= 2
            and message.command[1] ==  filter_
        ):
            return
            
        pattern = r"( |^|[^\w])" + re.escape(filter_) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            filter_name, content, text, data_type = await get_filter(chat_id, filter_)
            await SendFilterMessage(
                message=message,
                filter_name=filter_,
                content=content,
                text=text,
                data_type=data_type
            )

@app.on_message(filters.command('filters') & filters.group)
async def _filters(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    if message.chat.type == 'private':
        chat_title = 'local'
    FILTERS = await get_filters_list(chat_id)
    
    if len(FILTERS) == 0:
        await message.reply(
            f'No filters in {chat_title}.'
        )
        return

    filters_list = f'List of filters in {chat_title}:\n'
    
    for filter_ in FILTERS:
        filters_list += f'- `{filter_}`\n'
    
    await message.reply(
        filters_list
    )


@app.on_message(filters.command("stopall") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def stop_all(_, message):
    _filters = await get_filters_names(message.chat.id)
    if not _filters:
        await message.reply_text("**ɴᴏ ғɪʟᴛᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ʏᴇs, ᴅᴏ ɪᴛ", callback_data="stop_yes"),
                    InlineKeyboardButton("ɴᴏ, ᴅᴏɴ'ᴛ ᴅᴏ ɪᴛ", callback_data="stop_no"),
                ]
            ]
        )
        await message.reply_text(
            "**ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴛʜᴇ ғɪʟᴛᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ ғᴏʀᴇᴠᴇʀ ?.**",
            reply_markup=keyboard,
        )


@app.on_callback_query(filters.regex("^custfilters_"))
async def stopall_callback(client, callback_query: CallbackQuery):  
    chat_id = callback_query.message.chat.id 
    query_data = callback_query.data.split('_')[1]  

    user = await client.get_chat_member(chat_id, callback_query.from_user.id)

    if not user.status == ChatMemberStatus.OWNER :
        return await callback_query.answer("Only Owner Can Use This!!") 
    
    if query_data == 'stopall':
        await stop_all_db(chat_id)
        await callback_query.edit_message_text(text="I've deleted all chat filters.")
    
    elif query_data == 'cancel':
        await callback_query.edit_message_text(text='Cancelled.')


@app.on_callback_query(filters.regex("stop_(.*)") & ~BANNED_USERS)
async def stop_all_cb(_, cb):
    chat_id = cb.message.chat.id
    from_user = cb.from_user
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_change_info"
    if permission not in permissions:
        return await cb.answer(
            f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀᴇᴄǫᴜʀɪᴇᴅ ᴘᴇʀᴍɪssɪᴏɴ.\n ᴘᴇʀᴍɪssɪᴏɴ: {permission}",
            show_alert=True,
        )
    input = cb.data.split("_", 1)[1]
    if input == "yes":
        stoped_all = await deleteall_filters(chat_id)
        if stoped_all:
            return await cb.message.edit(
                "**sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴅᴇᴅ ᴀʟʟ ғɪʟᴛᴇʀ's ᴏɴ ᴛʜɪs ᴄʜᴀᴛ.**"
            )
    if input == "no":
        await cb.message.reply_to_message.delete()
        await cb.message.delete()

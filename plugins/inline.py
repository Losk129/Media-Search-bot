from urllib.parse import quote
from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument
from utils import get_search_results
from info import MAX_RESULTS, CACHE_TIME, SHARE_BUTTON_TEXT


@Client.on_inline_query()
async def answer(bot, query):
    """Show search results for given inline query"""

    results = []
    string = query.query
    reply_markup = get_reply_markup(bot.username)
    files = await get_search_results(string, max_results=MAX_RESULTS)

    for file in files:
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                file_id=file.file_id,
                caption=file.caption,
                description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
                reply_markup=reply_markup,
            )
        )

    if results:
        switch_pm_text = f"{emoji.CHECK_MARK} Hasil"
        if string:
            switch_pm_text += f" Untuk {string}"

        await query.answer(results=results,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
    else:

        switch_pm_text = f'{emoji.CROSS_MARK} Belum ada - Silahkan Hub. Admin! (Klik disini)'
        
        await query.answer(results=results,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="invite",
                           next_offset=str(next_offset))

def get_reply_markup(username, query):
    url = 'trakteer.id/ccgnimeX'
    url1 = 't.me/share/url?url=' + quote(SHARE_BUTTON_TEXT.format(username=username))
    buttons = [
        [
            InlineKeyboardButton('🔍 Cari Lagi', switch_inline_query_current_chat=query),
            InlineKeyboardButton('📤 Share', url=url1),
            InlineKeyboardButton('❣️Donasi', url=url),
        ]   
    ]
    return InlineKeyboardMarkup(buttons)


def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

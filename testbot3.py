import asyncio
import re
from telethon import TelegramClient, events

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

API_ID = 33650478
API_HASH = "be28efd94368d184e4410cd69e55ebb2"
NICK_BOT_USERNAME = "Nick_Bypass_Bot"
GROUP_CHAT_ID = -1003978964029

# 📢 Yahan apna Telegram Channel link dalein
CHANNEL_LINK = "https://t.me/+JA3lCMRFgFk5ODk9"

client = TelegramClient("my_userbot", API_ID, API_HASH, loop=loop)

pending_bypasses = {}

# =========================================================
# 🎨 STYLISH TEMPLATES (Channel Added)
# =========================================================

SUCCESS_TEMPLATE = """⚡ **LINK BYPASSED SUCCESSFULLY** ⚡
╭─────────────────────────────
├ ✅🌐 **Original Link:**
│ {orig_link}
│
├ ✅🎯 **Bypassed Link:**
│ {bypassed_link}
│
├ ⏱️ **Time Taken:** `{time_taken}`
╰─────────────────────────────
📢 **Join Channel:** {channel_link}
🚀 *Powered by @XDevil_Father *"""

FAILED_TEMPLATE = """❌ **BYPASS FAILED** ❌
╭─────────────────────────────
├ ⚠️ **Status:** No Link 🔗 Found / Unsupported
│
├ 🔗 **Target Link:**
│ {orig_link}
╰─────────────────────────────
📢 **Join Channel:** {channel_link}
💡 *Kripya sahi shortener link bheje!*"""

# =========================================================


def clean_url(url):
    return url.strip("`*_\n ")


def format_bot_response(bot_text, original_user_link):
    original_user_link = clean_url(original_user_link)

    if (
        "No Script Found" in bot_text
        or "Failed" in bot_text
        or "Error" in bot_text
    ):
        return FAILED_TEMPLATE.format(
            orig_link=original_user_link, channel_link=CHANNEL_LINK
        )

    raw_urls = re.findall(r"https?://[^\s`*_\)]+", bot_text)
    urls = [clean_url(u) for u in raw_urls]

    time_match = re.search(
        r"Time Taken\s*:\s*([\d\.\s\w]+)", bot_text, re.IGNORECASE
    )
    time_taken = time_match.group(1).strip() if time_match else "0 seconds"

    if len(urls) >= 2:
        return SUCCESS_TEMPLATE.format(
            orig_link=urls[0],
            bypassed_link=urls[1],
            time_taken=time_taken,
            channel_link=CHANNEL_LINK,
        )
    elif len(urls) == 1:
        return SUCCESS_TEMPLATE.format(
            orig_link=original_user_link,
            bypassed_link=urls[0],
            time_taken=time_taken,
            channel_link=CHANNEL_LINK,
        )
    else:
        return FAILED_TEMPLATE.format(
            orig_link=original_user_link, channel_link=CHANNEL_LINK
        )


@client.on(events.NewMessage(chats=GROUP_CHAT_ID))
async def group_message_handler(event):
    if event.message.text and "http" in event.message.text:
        raw_urls = re.findall(r"https?://[^\s`*_\)]+", event.message.text)
        orig_link = clean_url(raw_urls[0]) if raw_urls else event.message.text

        status_msg = await event.reply(
            "⏳ **Bypassing your link... Please wait!**"
        )

        sent_to_bot = await client.send_message(
            NICK_BOT_USERNAME, event.message.text
        )

        pending_bypasses[sent_to_bot.id] = {
            "status_msg": status_msg,
            "orig_link": orig_link,
        }


@client.on(events.NewMessage(from_users=NICK_BOT_USERNAME))
@client.on(events.MessageEdited(from_users=NICK_BOT_USERNAME))
async def nick_reply_handler(event):
    if not event.is_private:
        return

    reply_to_id = event.message.reply_to_msg_id

    if reply_to_id in pending_bypasses:
        data = pending_bypasses[reply_to_id]
        status_msg = data["status_msg"]
        orig_link = data["orig_link"]
        bot_text = event.message.text

        if "Processing" in bot_text:
            await status_msg.edit("⏳ **Processing your link...**")
        else:
            formatted_msg = format_bot_response(bot_text, orig_link)
            await status_msg.edit(formatted_msg, link_preview=False)
            del pending_bypasses[reply_to_id]


async def main():
    await client.start()
    print("\n✅ Bot is running with Channel Link...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n\n👋 Safely Exited.")
    finally:
        loop.close()

from telethon import TelegramClient, events

from telegram_listener.services.signal_service import post_raw_message


def register_handlers(client: TelegramClient, account_id: int) -> None:
    @client.on(events.NewMessage)
    async def handle_new_message(event):
        if not event.raw_text:
            return

        chat = await event.get_chat()
        sender = await event.get_sender()

        if event.is_channel:
            chat_type = "channel"
        elif event.is_group:
            chat_type = "group"
        else:
            chat_type = "private"

        sender_name = ""
        sender_id = None
        if sender:
            sender_id = sender.id
            first = getattr(sender, "first_name", "") or ""
            last = getattr(sender, "last_name", "") or ""
            sender_name = f"{first} {last}".strip()

        payload = {
            "telegram_account_id": account_id,
            "telegram_message_id": event.id,
            "channel_id": event.chat_id,
            "channel_title": getattr(chat, "title", "") or "",
            "channel_username": getattr(chat, "username", "") or "",
            "sender_id": sender_id,
            "sender_name": sender_name,
            "raw_text": event.raw_text,
            "message_date": event.date.isoformat(),
            "chat_type": chat_type,
        }

        print(f"[account={account_id}][{payload['channel_title'] or payload['channel_id']}] {event.raw_text[:80]}")
        post_raw_message(payload)

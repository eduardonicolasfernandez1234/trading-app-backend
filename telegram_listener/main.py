import argparse
import logging

from telegram_listener.app.client import create_client
from telegram_listener.app.listeners import register_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def main():
    parser = argparse.ArgumentParser(description="Telegram channel listener")
    parser.add_argument("--api-id", type=int, required=True)
    parser.add_argument("--api-hash", required=True)
    parser.add_argument("--phone", required=True)
    parser.add_argument("--session", required=True, help="Session file name (without .session)")
    parser.add_argument("--account-id", type=int, required=True, help="TelegramAccount DB id")
    args = parser.parse_args()

    client = create_client(args.session, args.api_id, args.api_hash)
    register_handlers(client, args.account_id)

    client.start(phone=args.phone)
    print(f"Listener running [account_id={args.account_id}]. Press Ctrl+C to stop.")
    client.run_until_disconnected()


if __name__ == "__main__":
    main()

from telegram_listener.parsers.base import BaseSignalParser


class ChannelBParser(BaseSignalParser):

    def parse(self, message: str) -> dict | None:
        return None

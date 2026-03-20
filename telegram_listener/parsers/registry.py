from telegram_listener.parsers.channel_a import ChannelAParser
from telegram_listener.parsers.channel_b import ChannelBParser

PARSER_REGISTRY = {
    "canal_username_a": ChannelAParser(),
    "canal_username_b": ChannelBParser(),
}


def get_parser(channel_username: str):
    return PARSER_REGISTRY.get(channel_username)
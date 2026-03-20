import re

from telegram_listener.parsers.base import BaseSignalParser


class ChannelAParser(BaseSignalParser):

    def parse(self, message: str) -> dict | None:
        if "BUY" not in message and "SELL" not in message:
            return None

        try:
            symbol_match = re.search(r"(BUY|SELL)\s+([A-Z]+)", message)
            entry_match = re.search(r"Entry[:\s]+([\d.]+)", message)
            sl_match = re.search(r"SL[:\s]+([\d.]+)", message)
            tp_match = re.search(r"TP1?[:\s]+([\d.]+)", message)

            return {
                "side": symbol_match.group(1) if symbol_match else None,
                "symbol": symbol_match.group(2) if symbol_match else None,
                "entry": float(entry_match.group(1)) if entry_match else None,
                "stop_loss": float(sl_match.group(1)) if sl_match else None,
                "take_profit": float(tp_match.group(1)) if tp_match else None,
                "raw": message,
            }

        except Exception as e:
            print("Parsing error:", e)
            return None

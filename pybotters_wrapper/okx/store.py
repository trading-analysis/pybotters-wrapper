from __future__ import annotations

import pandas as pd
from pybotters.models.okx import OKXDataStore

from pybotters_wrapper.core import (
    DataStoreWrapper,
    OrderbookStore,
    PositionStore,
    TickerStore,
    TradesStore,
)
from pybotters_wrapper.okx import OKXTESTWebsocketChannels, OKXWebsocketChannels
from pybotters_wrapper.utils.mixins import OKXMixin, OKXTESTMixin


class OKXTickerStore(TickerStore):
    def _normalize(
        self, store: "DataStore", operation: str, source: dict, data: dict
    ) -> "TickerItem":
        return self._itemize(data["instId"], float(data["last"]))


class OKXTradesStore(TradesStore):
    def _normalize(
        self, store: "DataStore", operation: str, source: dict, data: dict
    ) -> "TradesItem":
        return self._itemize(
            data["tradeId"],
            data["instId"],
            data["side"].upper(),
            float(data["px"]),
            float(data["sz"]),
            pd.to_datetime(data["ts"], unit="ms", utc=True),
        )


class OKXOrderbookStore(OrderbookStore):
    def _normalize(
        self, store: "DataStore", operation: str, source: dict, data: dict
    ) -> "OrderbookItem":
        return self._itemize(
            data["instId"],
            "SELL" if data["side"] == "asks" else "BUY",
            float(data["px"]),
            float(data["sz"]),
        )


class OKXPositionStore(PositionStore):
    def _normalize(
        self, store: "DataStore", operation: str, source: dict, data: dict
    ) -> "PositionItem":
        size = float(data["pos"])
        side = "BUY" if data["posSide"] == "long" else "SELL"

        return self._itemize(
            data["ccy"].upper(),
            side,
            float(data["avgPx"]),
            abs(size),
        )


class OKXDataStoreWrapper(OKXMixin, DataStoreWrapper[OKXDataStore]):
    _WRAP_STORE = OKXDataStore
    _WEBSOCKET_CHANNELS = OKXWebsocketChannels
    _TICKER_STORE = (OKXTickerStore, "tickers")
    _TRADES_STORE = (OKXTradesStore, "trades")
    _ORDERBOOK_STORE = (OKXOrderbookStore, "books")


class OKXTESTDataStoreWrapper(OKXTESTMixin, OKXDataStoreWrapper):
    _WRAP_STORE = OKXDataStore
    _WEBSOCKET_CHANNELS = OKXTESTWebsocketChannels
    _TICKER_STORE = (OKXTickerStore, "tickers")
    _TRADES_STORE = (OKXTradesStore, "trades")
    _ORDERBOOK_STORE = (OKXOrderbookStore, "books")

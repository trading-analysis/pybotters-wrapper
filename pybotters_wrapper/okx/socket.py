from __future__ import annotations

from pybotters_wrapper.core import WebsocketChannels


class OKXWebsocketChannels(WebsocketChannels):
    PUBLIC_ENDPOINT = "wss://ws.okx.com:8443/ws/v5/public"
    PRIVATE_ENDPOINT = "wss://ws.okx.com:8443/ws/v5/private"
    ENDPOINT = PUBLIC_ENDPOINT
    INST_TYPE = "SWAP"

    def subscribe(self, channel: str, *args, **kwargs) -> OKXWebsocketChannels:
        return super().subscribe(channel, *args, **kwargs)

    def make_subscribe_request(self, channel: str, *args, **kwargs) -> dict:
        return {"op": "subscribe", "args": [{"channel": channel, **kwargs}]}

    def make_subscribe_endpoint(self, channel: str, *args, **kwargs) -> str:
        # TODO: private endpoint
        return self.ENDPOINT

    def ticker(self, symbol: str, **kwargs) -> OKXWebsocketChannels:
        return self.tickers(symbol)

    def trades(self, symbol: str, **kwargs) -> OKXWebsocketChannels:
        return self.subscribe("trades", instId=symbol)

    def orderbook(self, symbol: str, **kwargs) -> OKXWebsocketChannels:
        return self.books(symbol)

    def tickers(self, symbol: str) -> OKXWebsocketChannels:
        return self.subscribe("tickers", instId=symbol)

    def books(self, symbol: str) -> OKXWebsocketChannels:
        return self.subscribe("books", instId=symbol)

    def order(self, symbol: str, **kwargs) -> OKXWebsocketChannels:
        return self.subscribe(
            "orders", symbol=symbol, instType=self.INST_TYPE, **kwargs
        )

    def position(self, symbol: str, **kwargs) -> OKXWebsocketChannels:
        return self.subscribe(
            "positions", symbol=symbol, instType=self.INST_TYPE, **kwargs
        )


class OKXTESTWebsocketChannels(WebsocketChannels):
    PUBLIC_ENDPOINT = "wss://ws.okx.com:8443/ws/v5/public"
    PRIVATE_ENDPOINT = "wss://ws.okx.com:8443/ws/v5/private"
    ENDPOINT = PUBLIC_ENDPOINT
    INST_TYPE = "SWAP"

    def subscribe(self, channel: str, *args, **kwargs) -> OKXTESTWebsocketChannels:
        return super().subscribe(channel, *args, **kwargs)

    def make_subscribe_request(self, channel: str, *args, **kwargs) -> dict:
        return {"op": "subscribe", "args": [{"channel": channel, **kwargs}]}

    def make_subscribe_endpoint(self, channel: str, *args, **kwargs) -> str:
        # TODO: private endpoint
        return self.ENDPOINT

    def ticker(self, symbol: str, **kwargs) -> OKXTESTWebsocketChannels:
        return self.tickers(symbol)

    def trades(self, symbol: str, **kwargs) -> OKXTESTWebsocketChannels:
        return self.subscribe("trades", instId=symbol)

    def orderbook(self, symbol: str, **kwargs) -> OKXTESTWebsocketChannels:
        return self.books(symbol)

    def tickers(self, symbol: str) -> OKXTESTWebsocketChannels:
        return self.subscribe("tickers", instId=symbol)

    def books(self, symbol: str) -> OKXTESTWebsocketChannels:
        return self.subscribe("books", instId=symbol)

    def order(self, symbol: str, **kwargs) -> OKXTESTWebsocketChannels:
        return self.subscribe(
            "orders", symbol=symbol, instType=self.INST_TYPE, **kwargs
        )

    def position(self, symbol: str, **kwargs) -> OKXTESTWebsocketChannels:
        return self.subscribe(
            "positions", symbol=symbol, instType=self.INST_TYPE, **kwargs
        )

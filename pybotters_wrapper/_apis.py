from __future__ import annotations

import traceback
from typing import Callable, Type, TypeVar

import pybotters
from pybotters.store import DataStoreManager

import pybotters_wrapper as pbw
from pybotters_wrapper import plugins
from pybotters_wrapper.common import API, DataStoreWrapper
from pybotters_wrapper.common.socket import (
    WebsocketChannels,
    WebsocketConnection,
    WsHandler,
)

TWebsocketChannels = TypeVar("TWebsocketChannels", bound=WebsocketChannels)

EXCHANGE2BASEURL = {
    "binancespot": pbw.binance.BinanceSpotAPI.BASE_URL,
    "binanceusdsm": pbw.binance.BinanceUSDSMAPI.BASE_URL,
    "binancecoinm": pbw.binance.BinanceCOINMAPI.BASE_URL,
    "bitbank": pbw.bitbank.bitbankAPI.BASE_URL,
    "bitflyer": pbw.bitflyer.bitFlyerAPI.BASE_URL,
    "bitget": pbw.bitget.BitgetAPI.BASE_URL,
    "bybitusdt": pbw.bybit.BybitUSDTAPI.BASE_URL,
    "bybitinverse": pbw.bybit.BybitInverseAPI.BASE_URL,
    "coincheck": pbw.coincheck.CoincheckAPI.BASE_URL,
    "gmocoin": pbw.gmocoin.GMOCoinAPI.BASE_URL,
    "kucoinspot": pbw.kucoin.KuCoinSpotAPI.BASE_URL,
    "kucoinfutures": pbw.kucoin.KuCoinFuturesAPI.BASE_URL,
    "okx": pbw.okx.OKXAPI.BASE_URL,
    "phemex": pbw.phemex.PhemexAPI.BASE_URL,
}

EXCHANGE2STORE = {
    "binancespot": pbw.binance.BinanceSpotDataStoreWrapper,
    "binanceusdsm": pbw.binance.BinanceUSDSMDataStoreWrapper,
    "binancecoinm": pbw.binance.BinanceCOINMDataStoreWrapper,
    "bitbank": pbw.bitbank.bitbankDataStoreWrapper,
    "bitflyer": pbw.bitflyer.bitFlyerDataStoreWrapper,
    "bitget": pbw.bitget.BitgetDataStoreWrapper,
    "bybitusdt": pbw.bybit.BybitUSDTDataStoreWrapper,
    "bybitinverse": pbw.bybit.BybitInverseDataStoreWrapper,
    "coincheck": pbw.coincheck.CoincheckDataStoreWrapper,
    "ftx": pbw.ftx.FTXDataStoreWrapper,
    "gmocoin": pbw.gmocoin.GMOCoinDataStoreWrapper,
    "kucoinspot": pbw.kucoin.KuCoinSpotDataStoreWrapper,
    "kucoinfutures": pbw.kucoin.KuCoinFuturesDataStoreWrapper,
    "okx": pbw.okx.OKXDataStoreWrapper,
    "phemex": pbw.phemex.PhemexDataStoreWrapper,
}

EXCHANGE2API: dict[str, Type[API]] = {
    "binancespot": pbw.binance.BinanceSpotAPI,
    "binanceusdsm": pbw.binance.BinanceUSDSMAPI,
    "binancecoinm": pbw.binance.BinanceCOINMAPI,
    "bitbank": pbw.bitbank.bitbankAPI,
    "bitget": pbw.bitget.BitgetAPI,
    "bitflyer": pbw.bitflyer.bitFlyerAPI,
    "bybitusdt": pbw.bybit.BybitUSDTAPI,
    "bybitinverse": pbw.bybit.BybitInverseAPI,
    "coincheck": pbw.coincheck.CoincheckAPI,
    "ftx": pbw.ftx.FTXAPI,
    "gmocoin": pbw.gmocoin.GMOCoinAPI,
    "kucoinspot": pbw.kucoin.KuCoinSpotAPI,
    "kucoinfutures": pbw.kucoin.KuCoinFuturesAPI,
    "okx": pbw.okx.OKXAPI,
    "phemex": pbw.phemex.PhemexAPI,
}


def _get_value(exchange, dic):
    if exchange not in dic:
        f = [t for t in traceback.extract_stack() if t.filename.endswith("_apis.py")][0]
        raise RuntimeError(f"Unsupported exchange: {exchange} (`{f.name}()`)")
    return dic[exchange]


def create_store(
    exchange: str, *, store: DataStoreManager = None, **kwargs
) -> DataStoreWrapper:
    return _get_value(exchange, EXCHANGE2STORE)(store)


def create_api(exchange: str, client: pybotters.Client, **kwargs) -> API:
    return _get_value(exchange, EXCHANGE2API)(client, **kwargs)


def create_plugin(store: DataStoreWrapper, name: str, **kwargs):
    try:
        factory_fn = getattr(plugins, name)
    except AttributeError:
        raise RuntimeError(f"Unsupported plugin: {name}")
    return factory_fn(store, **kwargs)


def create_socket_channels(exchange: str) -> TWebsocketChannels:
    return EXCHANGE2STORE[exchange]._WEBSOCKET_CHANNELS()


async def create_ws_connect(
    client: pybotters.Client,
    *,
    endpoint: str = None,
    send: any = None,
    hdlr: WsHandler = None,
    subscribe_list: dict[str, list[str]] = None,
    send_type: str = "json",
    hdlr_type: str = "json",
    auto_reconnect: bool = False,
    on_reconnection: Callable = None,
) -> WebsocketConnection | list[WebsocketConnection]:
    if endpoint is not None and send is not None:
        return await WebsocketConnection(
            endpoint, send, hdlr=hdlr, send_type=send_type, hdlr_type=hdlr_type
        ).connect(client, auto_reconnect, on_reconnection)
    elif subscribe_list is not None:
        conns = []
        for endpoint, send in subscribe_list.items():
            conn = await create_ws_connect(
                client,
                endpoint=endpoint,
                send=send,
                hdlr=hdlr,
                send_type=send_type,
                hdlr_type=hdlr_type,
                auto_reconnect=auto_reconnect,
                on_reconnection=on_reconnection,
            )
            conns.append(conn)
        return conns
    else:
        raise RuntimeError("Need either of `endpoint` and `send` or `subscribe_list`")


def get_base_url(exchange: str) -> str:
    return EXCHANGE2API[exchange].BASE_URL

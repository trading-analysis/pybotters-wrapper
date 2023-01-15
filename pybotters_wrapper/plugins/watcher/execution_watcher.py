from __future__ import annotations

import asyncio
from typing import Callable

from ...core.store import DataStoreWrapper, ExecutionItem
from .._base import DataStorePlugin


class ExecutionWatcher(DataStorePlugin):
    def __init__(
        self,
        store: "DataStoreWrapper",
        *,
        store_name: str = None,
        is_target: Callable[["DataStore", str, dict, dict], bool] = None,
    ):
        # ExecutionDataStoreを監視
        store_name = store_name or "execution"
        watch_store = getattr(store, store_name)
        super(ExecutionWatcher, self).__init__(watch_store)
        self._order_id = None
        self._item = None
        self._done = None
        self._event = asyncio.Event()
        self._is_target_fn = is_target

    def set(self, order_id: str = None) -> ExecutionWatcher:
        """監視対象の注文IDをセット"""
        if self._order_id is not None:
            raise RuntimeError(
                "ExecutionWatcher must not be 'reused', create a new instance instead."
            )
        self._order_id = order_id
        self._event.set()
        return self

    async def _on_watch(self, store, operation: str, source, data: ExecutionItem):
        """流れてきた約定情報が監視中の注文に関するものであるかをチェック

        ExecutionStoreを監視してるので、流れてくるdictはExecutionItem

        """
        if not self._event.is_set():
            # order_idがsetされるまで待機
            # 注文が即約定した時にsocket messageがresのresponseより早く到達するケースがあるので、
            # order_idがセットされるまでメッセージをここで待機させておく
            await self._event.wait()

        if self._is_target(store, operation, source, data):
            self._done = True
            self._item = data

    def _on_watch_is_stop(
        self, store: "DataStore", operation: str, source: dict, data: dict
    ) -> bool:
        """監視終了判定"""
        return self._done

    def _is_target(self, store: "DataStore", operation: str, source: dict, data: dict):
        if self._is_target_fn:
            return self._is_target_fn(store, operation, source, data)
        else:
            return data["id"] == self._order_id

    def done(self) -> bool:
        return self._done

    def result(self) -> ExecutionItem:
        return self._item

    async def wait(self):
        return await self._watch_task

    @property
    def order_id(self) -> str:
        return self._order_id

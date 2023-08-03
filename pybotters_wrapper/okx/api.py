from __future__ import annotations

from pybotters_wrapper.core import API
from pybotters_wrapper.utils.mixins import OKXTESTMixin


class OKXAPI(API):
    BASE_URL = "https://www.okx.com"


class OKXTESTAPI(API, OKXTESTMixin):
    BASE_URL = "https://www.okx.com"

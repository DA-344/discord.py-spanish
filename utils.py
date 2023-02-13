"""
La Licencia MIT (MIT)

Copyright (c) 2015-presente Rapptz
Copyright (c) 2023-presente Developer Anonymous

Por la presente se concede permiso, sin cargo, a cualquier persona que obtenga una
copia de este software y los archivos de documentación asociados (el "Software"),
comercializar el Software sin restricciones, incluidos, entre otros,
los derechos de uso, copia, modificación, fusión, publicación, distribución, sublicencia,
y/o vender copias del Software, y permitir a las personas a quienes el
El software se proporciona para hacerlo, sujeto a las siguientes condiciones:

El aviso de derechos de autor anterior y este aviso de permiso se incluirán en
todas las copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA
O IMPLÍCITO, INCLUYENDO PERO NO LIMITADO A LAS GARANTÍAS DE COMERCIABILIDAD,
IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO VIOLACIÓN. EN NINGÚN CASO LA
LOS AUTORES O TITULARES DE LOS DERECHOS DE AUTOR SERÁN RESPONSABLES DE CUALQUIER RECLAMACIÓN, DAÑOS U OTROS
RESPONSABILIDAD, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O DE OTRA FORMA, DERIVADA
DESDE, FUERA DE O EN RELACIÓN CON EL SOFTWARE O EL USO U OTRO
TRATAMIENTOS EN EL SOFTWARE.
"""

from __future__ import annotations

import array
import asyncio
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Collection,
    Coroutine,
    Dict,
    ForwardRef,
    Generic,
    Iterable,
    Iterator,
    List,
    Literal,
    Mapping,
    NamedTuple,
    Optional,
    Protocol,
    Set,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
    TYPE_CHECKING,
)
import unicodedata
from base64 import b64encode
from bisect import bisect_left
import datetime
import functools
from inspect import isawaitable as _isawaitable, signature as _signature
from operator import attrgetter
from urllib.parse import urlencode
import json
import re
import os
import sys
import types
import warnings
import logging

import yarl

try:
    import orjson #type: ingore
except ModuleNotFoundError:
    HAS_ORJSON = False
else:
    HAS_ORJSON = True
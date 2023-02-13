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

import types
from collections import namedtuple
from typing import Any, ClassVar, Dict, List, Optional, TYPE_CHECKING, Tuple, Type, TypeVar, Iterator, Mapping

__all__ = (
    'Enum',
    'TipoCanal',
    'TipoMensaje',
    'EstadoHabla',
    'NivelVerificacion',
    'FiltroContenido',
    'Estado',
    'AvatarPredeterminado',
    'AccionRegistro',
    'CategoriaAccionRegistro',
    'BanderasUsuario',
    'TipoActividad',
    'NivelNotificaciones',
    'EstadoMembresia',
    'TipoWebhook',
    'ComportamientoExpiracion',
    'RespuestaExpiracion',
    'TipoPegatina',
    'TipoFormatoPegatina',
    'ObjetivoInvitacion',
    'ModoCalidadVideo',
    'TipoComponente',
    'EstiloBoton',
    'EstiloTexto',
    'NivelPrivacidad',
    'TipoInteraccion',
    'TipoRespuestaInteraccion',
    'NivelNSFW',
    'NivelMFA',
    'Lengua',
    'TipoEntidad',
    'EstadoEvento',
    'TipoComandoAplicacion',
    'TipoOpcionComandoAplicacion',
    'TipoPermisoComandoAplicacion',
    'TipoTriggerReglaAutoMod',
    'TipoEventoReglaAutoMod',
    'TipoAccionReglaAutoMod',
)

if TYPE_CHECKING:
    from typing_extensions import Self

def _create_value_cls(name: str, comparable: bool):
    
    cls = namedtuple('_EnumValue_' + name, 'name value')

    cls.__repr__ = lambda self: f'<{name}.{self.name}: {self.value!r}'
    cls.__str__ = lambda self: f'{name}.{self.name}'

    if comparable:
        cls.__le__ = lambda self, other: isinstance(other, self.__class__) and self.value <= other.value
        cls.__ge__ = lambda self, other: isinstance(other, self.__class__) and self.value >= other.value
        cls.__lt__ = lambda self, other: isinstance(other, self.__class__) and self.value < other.value
        cls.__gt__ = lambda self, other: isinstance(other, self.__class__) and self.value > other.value

    return cls

def _is_descriptor(obj):
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')

class EnumMeta(type):
    if TYPE_CHECKING:
        __name__: ClassVar[str]
        _enum_member_names_: ClassVar[List[str]]
        _enum_member_map_: ClassVar[Dict[str, Any]]
        _enum_value_map_: ClassVar[Dict[Any, Any]]

    def __new__(cls, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any], *, comparable: bool = False) -> Self:
        value_mapping = {}
        member_mapping = {}
        member_names = []

        value_cls = _create_value_cls(name, comparable)

        for key, value in list(attrs.items()):
            is_descriptor = _is_descriptor(value)
            if key[0] == '_' and not is_descriptor:
                continue

            if isinstance(value, classmethod):
                continue

            try:
                new_value = value_mapping[value]
            
            except KeyError:
                new_value = value_cls(name=key, value=value)
                value_mapping[value] = new_value
                member_names.append(key)

            member_mapping[key] = new_value
            attrs[key] = new_value
        
        attrs['_enum_value_map_'] = value_mapping
        attrs['_enum_member_map_'] = member_mapping
        attrs['_enum_member_names_'] = member_names
        attrs['_enum_value_cls_'] = value_cls
        actual_cls = super().__new__(cls, name, bases, attrs)
        value_cls._actual_enum_cls_ = actual_cls

        return actual_cls

    def __iter__(cls) -> Iterator[Any]:
        return (cls._enum_member_map_[name] for name in reversed(cls._enum_member_names_))

    def __len__(cls) -> int:
        return len(cls._enum_member_names_)

    def __repr__(cls) -> str:
        return f'<enum {cls.__name__}>'

    @property
    def __members__(cls) -> Mapping[str, Any]:
        return types.MappingProxyType(cls._enum_member_map_)
    
    def __call__(cls, value:str) -> Any:
        try:
            return cls._enum_member_map_[value]
        
        except (KeyError, TypeError):
            raise ValueError(f"{value!r} no es un {cls.__name__} válido.")
        
    def __getitem__(cls, key: str) -> Any:
        return cls._enum_member_map_[key]

    def __setattr__(cls, name: str, value: Any) -> None:
        raise TypeError('Los Enums son inmutables.')

    def __delattr__(cls, attr: str) -> None:
        raise TypeError('Los Enums son inmutables.')

    def __instancecheck__(self, instance: Any) -> bool:
        # isinstance(x, Y)
        # -> __instancecheck__(Y, x)

        try:
            return instance._actual_enum_cls is self
        
        except AttributeError:
            return False

if TYPE_CHECKING:
    from enum import Enum

else:

    class Enum(metaclass=EnumMeta):
        @classmethod
        def try_value(cls, value):
            try:
                return cls._enum_value_map_[value]

            except (KeyError, TypeError):
                return value

class TipoCanal(Enum):
    texto = 0
    privado = 1
    voz = 2
    grupo = 3
    categoria = 4
    anuncios = 5
    hilo_anuncios = 10
    hilo_publico = 11
    hilo_privado = 12
    escenario = 13
    foro = 15

    def __str__(self) -> str:
        return self.name

class TipoMensaje(Enum):
    predeterminado = 0
    nuevo_recipiente = 1
    elminiacion_recipiente = 2
    llamada = 3
    nombre_canal_cambiado = 4
    icono_canal_cambiado = 5
    nuevo_fijado = 6
    nuevo_miembro = 7
    suscripcion_premium_servidor = 8
    servidor_premium_nivel_1 = 9
    servidor_premium_nivel_2 = 10
    servidor_premium_nivel_3 = 11
    nuevo_canal_seguido = 12
    vivo_servidor = 13
    descubrimiento_servidor_desclasificado = 14
    descubrimiento_servidor_recalificado = 15
    primera_advertencia_eliminacion_servidor_descubrimiento = 16
    ultima_advertencia_elminiacion_servidor_descubrimiento = 17
    hilo_creado = 18
    respuesta = 19
    comando_de_texto = 20
    mensaje_inicio_hilo = 21
    recordatoria_invitacion_servidor = 22
    comando_menu_contextual = 23
    accion_auto_moderacion = 24

class EstadoHabla(Enum):
    ninguna = 0
    voz = 1
    sonido_compartido = 2
    prioridad = 4

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

class NivelVerificacion(Enum, comparable=True):
    ninguna = 0
    baja = 1
    media = 2
    alta = 3
    altisima = 4

    def __str__(self) -> str:
        return self.name

class FiltroContenido(Enum, comparable=True):
    disabled = 0
    no_role = 1
    all_members = 2

    def __str__(self) -> str:
        return self.name

class Estado(Enum):
    en_linea = 'online'
    desconectado = 'offline'
    ausente = 'idle'
    nm = 'dnd'
    no_molestar = 'dnd'
    invisible = 'invisible'

    def __str__(self) -> str:
        return self.value

class AvatarPredeterminado(Enum):
    azul = 0
    gris = 1
    grisaceo = 1
    verde = 2
    naranja = 3
    rojo = 4

    def __str__(self) -> str:
        return self.name

class NivelNotificaciones(Enum, comparable = True):
    todos_mensajes = 0
    solo_menciones = 1

class CategoriaAccionRegistro(Enum):
    creacion = 1
    eliminacion = 2
    actualizacion = 3

class AccionRegistro(Enum):
    # fmt: off

    actualizacion_servidor                    = 1
    creacion_canal                  = 10
    actualizacion_canal                  = 11
    eliminar_canal                  = 12
    creacion_sobreescritura                = 13
    actualizacion_sobreescritura              = 14
    eliminar_sobreescritura                = 15
    expulsar                            = 20
    purga_miembros                    = 21
    veto                             = 22
    anulacion_veto                           = 23
    actualizacion_miembro                   = 24
    actualizacion_roles_miembro              = 25
    mover_miembro                     = 26
    desconexion_miembro               = 27
    bot_añadido                         = 28
    creacion_rol                     = 30
    actualizacion_rol                     = 31
    eliminar_rol                     = 32
    creacion_invitacion                   = 40
    actualizacion_invitacion                   = 41
    revocamiento_invitacion                   = 42
    creacion_webhook                  = 50
    actualizacion_webhook                  = 51
    eliminar_webhook                  = 52
    creacion_emoji                    = 60
    actualizacion_emoji                    = 61
    eliminar_emoji                    = 62
    eliminar_mensaje                  = 72
    eliminacion_masiva_mensajes             = 73
    fijar_mensaje                     = 74
    desclavar_mensaje                   = 75
    creacion_integracion              = 80
    actualizacion_integracion              = 81
    eliminar_integracion              = 82
    creacion_instancia_escenario           = 83
    actualizacion_instancia_escenario           = 84
    elminar_instancia_escenario           = 85
    creacion_pegatina                  = 90
    actualizacion_pegatina                  = 91
    eliminar_pegatina                  = 92
    creacion_evento          = 100
    actualizacion_evento          = 101
    eliminar_evento          = 102
    creacion_hilo                   = 110
    actualizacion_hilo                   = 111
    eliminar_hilo                   = 112
    actualizacion_permisos_comandos_aplicacion   = 121
    creacion_regla_automod             = 140
    actualizacion_regla_automod             = 141
    eliminar_regla_automod             = 142
    bloquear_mensaje_automod           = 143
    # fmt: on

    @property
    def category(self) -> Optional[CategoriaAccionRegistro]:
        # fmt: off

        lookup: Dict[AccionRegistro, Optional[CategoriaAccionRegistro]] = {
            AccionRegistro.actualizacion_servidor:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.creacion_canal:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_canal:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_canal:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.creacion_sobreescritura:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_sobreescritura:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_sobreescritura:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.expulsar:
            None,
            AccionRegistro.purga_miembros:
            None,
            AccionRegistro.veto:
            None,
            AccionRegistro.anulacion_veto:
            None,
            AccionRegistro.actualizacion_miembro:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.actualizacion_roles_miembro:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.mover_miembro:
            None,
            AccionRegistro.desconexion_miembro:
            None,
            AccionRegistro.bot_añadido:
            None,
            AccionRegistro.creacion_rol:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_rol:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_rol:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.creacion_invitacion:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_invitacion:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.revocamiento_invitacion:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.creacion_webhook:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_webhook:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_webhook:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.creacion_emoji:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_emoji:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_emoji:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.eliminar_mensaje:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.eliminacion_masiva_mensajes:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.fijar_mensaje:
            None,
            AccionRegistro.desclavar_mensaje:
            None,
            AccionRegistro.creacion_integracion:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_integracion:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_integracion:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.creacion_instancia_escenario:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_instancia_escenario:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.elminar_instancia_escenario:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.creacion_pegatina:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_pegatina:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_pegatina:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.creacion_evento:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_evento:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_evento:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.creacion_hilo:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_hilo:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_hilo:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.actualizacion_permisos_comandos_aplicacion:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.creacion_regla_automod:
            CategoriaAccionRegistro.creacion,
            AccionRegistro.actualizacion_regla_automod:
            CategoriaAccionRegistro.actualizacion,
            AccionRegistro.eliminar_regla_automod:
            CategoriaAccionRegistro.eliminacion,
            AccionRegistro.bloquear_mensaje_automod:
            None,
        }
        # fmt: on
        return lookup[self]

    @property
    def target_type(self) -> Optional[str]:
        v = self.value

        if v == -1:
            return 'all'

        elif v < 10:
            return 'guild'
        
        elif v < 20:
            return 'channel'

        elif v < 30:
            return 'user'
        elif v < 40:
            return 'role'
        elif v < 50:
            return 'invite'
        elif v < 60:
            return 'webhook'
        elif v < 70:
            return 'emoji'
        elif v == 73:
            return 'channel'
        elif v < 80:
            return 'message'
        elif v < 83:
            return 'integration'
        elif v < 90:
            return 'stage_instance'
        elif v < 93:
            return 'sticker'
        elif v < 103:
            return 'guild_scheduled_event'
        elif v < 113:
            return 'thread'
        elif v < 122:
            return 'integration_or_app_command'
        elif v < 143:
            return 'auto_moderation'
        elif v == 143:
            return 'user'

class BanderasUsuario(Enum):
    staff = 1
    socio = 2
    hypesquad = 4
    caza_errores = 8
    mfs_sms = 16
    promocion_premium_removida = 32
    hypesquad_bravery = 64
    hypesquad_brilliance = 128
    hypesquad_balance = 256
    partidario_inicial = 512
    usuario_equipo = 1024
    sistema = 4096
    tiene_mensajes_urgentes_sin_leer = 8192
    caza_errores_nivel_2 = 16384
    bot_verificado = 65536
    desarrollador_bots_verificado = 131072
    moderador_discord_certificado = 262144
    bot_interacciones_http = 524288
    spammer = 1048576

class TipoActividad(Enum):
    desconocido = -1
    jugando = 0
    transmitiendo = 1
    escuchando = 2
    viendo = 3
    personalizado = 4
    compitiendo = 5

    def __int__(self) -> int:
        return self.value

class EstadoMembresía(Enum):
    invitado = 1
    aceptado = 2

class TipoWebhook(Enum):
    entrante = 1
    seguidor_canal = 2
    aplicacion = 3

class ComportamientoExpiracion(Enum):
    rol_removido = 0
    expulsion = 1

RespuestaExpiracion = ComportamientoExpiracion

class TipoPegatina(Enum):
    estandar = 1
    servidor = 2

class FormatoTipoPegatina(Enum):
    png = 1
    apng = 2
    lottie = 3

    @property
    def file_extension(self) -> str:
        # fmt: off
        lookup: Dict[FormatoTipoPegatina, str] = {
            FormatoTipoPegatina.png: 'png',
            FormatoTipoPegatina.apng: 'png',
            FormatoTipoPegatina.lottie: 'json',
        }
        # fmt: on
        return lookup[self]

class ObjetivoInvitacion(Enum):
    desconocido = 0
    transmision = 1
    aplicacion_incorporada = 2

class TipoInteraccion(Enum):
    ping = 1
    comando_aplicacion = 2
    componente = 3
    autocompletar = 4
    entrega_cuestionario = 5

class TipoRespuestaInteraccion(Enum):
    pong = 1
    mensaje_canal = 4
    mensaje_canal_diferido = 5 # (con codigo)
    actualizacion_mensaje_diferido = 6 # para componentes
    actualizacion_mensaje = 7 # para componentes
    resultado_autocompletar = 8
    cuestionario = 9 # para "modals"

class ModoCalidadVideo(Enum):
    auto = 1
    completa = 2

    def __int__(self) -> int:
        return self.value

class TipoComponente(Enum):
    fila_de_accion = 1
    boton = 2
    seleccion = 3
    entrada_texto = 4

    def __int__(self) -> int:
        return self.value

class EstiloBoton(Enum):
    primario = 1
    secundario = 2
    exito = 3
    peligro = 4
    hipervinculo =  5

    # <!-- Aliases -->
    azul = 1
    gris = 2
    grisaceo = 2
    verde = 3
    rojo = 4
    link = 5

    def __int__(self) -> int:
        return self.value

class EstiloTexto(Enum):
    corto = 1
    parrafo = 2

    # <!-- Aliases -->
    largo = 2

    def __int__(self) -> int:
        return self.value

class NivelPrivacidad(Enum):
    solo_servidor = 2

class NivelNSFW(Enum, comparable = True):
    predeterminado = 0
    explicito = 1
    seguro = 2
    restriccion_edad = 3

class NivelMFA(Enum, comparable = True):
    deshabilitado = 0
    requiere_a2f = 1

class Lengua(Enum):
    ingles_americano = 'en-US'
    ingles_britanico = 'en-GB'
    bulgaro = 'bg'
    chino = 'zh-CN'
    chino_tailandes = 'zn-TW'
    croata = 'hr'
    checo = 'cs'
    danes = 'da'
    holandes = 'nl'
    fines = 'fi'
    frances = 'fr'
    aleman = 'de'
    griego = 'el'
    hindi = 'hi'
    hungaro = 'hu'
    italiano = 'it'
    japones = 'ja'
    coreano = 'ko'
    lituano = 'lt'
    noruego = 'no'
    polaco = 'pl'
    portuges_brasileño = 'pt-BR'
    rumano = 'ro'
    ruso = 'ru'
    español_españa = 'es-ES'
    sueco = 'sv-SE'
    tailandes = 'th'
    turco = 'tr'
    ucraniano = 'uk'
    vietnamita = 'vi'

    def __str__(self) -> str:
        return self.value
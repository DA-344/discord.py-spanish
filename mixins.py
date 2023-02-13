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

__all__ = (
    'EquealityComparable',
    'Hashable',
)

class EqualityComparable:
    __slots__ = ()

    id: int

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, self.__class__):
            return otro.id == self.id

        return NotImplemented

class Hashable(EqualityComparable):
    __slots__ = ()

    def __hash__(self) -> int:
        return self.id >> 22
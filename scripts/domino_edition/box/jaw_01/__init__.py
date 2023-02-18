# domino
from domino.api import matrix
from domino_edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Jaw01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "jaw"
    side = "C"
    index = 0
    description = "턱 입니다."


class Jaw01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Jaw01Identifier(self)
        super(Jaw01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Jaw01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1],
                        "multi": True},
        })
        return preset


class Jaw01Guide(piece.Guide):

    def guide(self):
        super(Jaw01Guide, self).guide()


class Jaw01Rig(piece.Rig):

    def objects(self, context):
        super(Jaw01Rig, self).objects(context)

        data = self.data(Jaw01Data.SELF)
        assembly_data = self.data(Jaw01Data.ASSEMBLY)

    def attributes(self, context):
        super(Jaw01Rig, self).attributes(context)

    def operators(self, context):
        super(Jaw01Rig, self).operators(context)

    def connections(self, context):
        super(Jaw01Rig, self).connections(context)


class Jaw01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Jaw01Data(node=node, data=data)
        self._guide = Jaw01Guide(self._ddata)
        self._rig = Jaw01Rig(self._ddata)

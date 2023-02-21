# domino
from domino.core.api import matrix
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class ChainFk01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = ""
    side = "C"
    index = 0
    description = ""


class ChainFk01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = ChainFk01Identifier(self)
        super(ChainFk01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(ChainFk01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1],
                        "multi": True},
        })
        return preset


class ChainFk01Guide(piece.Guide):

    def guide(self):
        super(ChainFk01Guide, self).guide()


class ChainFk01Rig(piece.Rig):

    def objects(self, context):
        super(ChainFk01Rig, self).objects(context)

        data = self.data(ChainFk01Data.SELF)
        assembly_data = self.data(ChainFk01Data.ASSEMBLY)

    def attributes(self, context):
        super(ChainFk01Rig, self).attributes(context)

    def operators(self, context):
        super(ChainFk01Rig, self).operators(context)

    def connections(self, context):
        super(ChainFk01Rig, self).connections(context)


class ChainFk01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = ChainFk01Data(node=node, data=data)
        self._guide = ChainFk01Guide(self._ddata)
        self._rig = ChainFk01Rig(self._ddata)

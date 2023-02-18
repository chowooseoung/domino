# domino
from domino.api import matrix
from domino_edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Eye01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "eye"
    side = "C"
    index = 0
    description = "눈 입니다."


class Eye01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Eye01Identifier(self)
        super(Eye01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Eye01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1],
                        "multi": True},
        })
        return preset


class Eye01Guide(piece.Guide):

    def guide(self):
        super(Eye01Guide, self).guide()


class Eye01Rig(piece.Rig):

    def objects(self, context):
        super(Eye01Rig, self).objects(context)

        data = self.data(Eye01Data.SELF)
        assembly_data = self.data(Eye01Data.ASSEMBLY)

    def attributes(self, context):
        super(Eye01Rig, self).attributes(context)

    def operators(self, context):
        super(Eye01Rig, self).operators(context)

    def connections(self, context):
        super(Eye01Rig, self).connections(context)


class Eye01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Eye01Data(node=node, data=data)
        self._guide = Eye01Guide(self._ddata)
        self._rig = Eye01Rig(self._ddata)

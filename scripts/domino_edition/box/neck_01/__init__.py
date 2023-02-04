# domino
from domino.api import matrix
from domino_edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Neck01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    module = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "neck"
    side = "C"
    index = 0
    description = "목 입니다."


class Neck01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Neck01Identifier(self)
        super(Neck01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Neck01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1],
                        "multi": True},
        })
        return preset


class Neck01Guide(piece.Guide):

    def guide(self):
        super(Neck01Guide, self).guide()


class Neck01Rig(piece.Rig):

    def objects(self, context):
        super(Neck01Rig, self).objects(context)

        data = self.data(Neck01Data.SELF)
        assembly_data = self.data(Neck01Data.ASSEMBLY)

    def attributes(self, context):
        super(Neck01Rig, self).attributes(context)

    def operators(self, context):
        super(Neck01Rig, self).operators(context)

    def connections(self, context):
        super(Neck01Rig, self).connections(context)


class Neck01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Neck01Data(node=node, data=data)
        self._guide = Neck01Guide(self._ddata)
        self._rig = Neck01Rig(self._ddata)

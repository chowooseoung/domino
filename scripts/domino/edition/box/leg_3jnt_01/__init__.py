# domino
from domino.core import matrix
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Leg3jnt01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "leg"
    side = "C"
    index = 0
    description = "quadruped 다리 입니다."


class Leg3jnt01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Leg3jnt01Identifier(self)
        super(Leg3jnt01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Leg3jnt01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1],
                        "multi": True},
        })
        return preset


class Leg3jnt01Guide(piece.Guide):

    def guide(self):
        super(Leg3jnt01Guide, self).guide()


class Leg3jnt01Rig(piece.Rig):

    def objects(self, context):
        super(Leg3jnt01Rig, self).objects(context)

        data = self.data(Leg3jnt01Data.SELF)
        assembly_data = self.data(Leg3jnt01Data.ASSEMBLY)

    def attributes(self, context):
        super(Leg3jnt01Rig, self).attributes(context)

    def operators(self, context):
        super(Leg3jnt01Rig, self).operators(context)

    def connections(self, context):
        super(Leg3jnt01Rig, self).connections(context)


class Leg3jnt01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Leg3jnt01Data(node=node, data=data)
        self._guide = Leg3jnt01Guide(self._ddata)
        self._rig = Leg3jnt01Rig(self._ddata)

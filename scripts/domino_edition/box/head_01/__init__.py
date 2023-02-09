# domino
from domino.api import matrix
from domino_edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Head01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "head"
    side = "C"
    index = 0
    description = "머리 입니다."


class Head01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))
    _m2 = matrix.get_matrix_from_pos((0, 2, 0))
    _m3 = matrix.get_matrix_from_pos((0, 0, 0.2))

    def __init__(self, node=None, data=None):
        self._identifier = Head01Identifier(self)
        super(Head01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Head01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2, self._m3],
                        "multi": True},
        })
        return preset


class Head01Guide(piece.Guide):

    def guide(self):
        data = self.data(Head01Data.SELF)
        root = super(Head01Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        pos1 = self.create_position(root, data["anchors"][2])
        self.create_display_crv(root, [root, pos])
        self.create_display_crv(root, [root, pos1])


class Head01Rig(piece.Rig):

    def objects(self, context):
        super(Head01Rig, self).objects(context)

        data = self.data(Head01Data.SELF)
        assembly_data = self.data(Head01Data.ASSEMBLY)

    def attributes(self, context):
        super(Head01Rig, self).attributes(context)

    def operators(self, context):
        super(Head01Rig, self).operators(context)

    def connections(self, context):
        super(Head01Rig, self).connections(context)


class Head01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Head01Data(node=node, data=data)
        self._guide = Head01Guide(self._ddata)
        self._rig = Head01Rig(self._ddata)

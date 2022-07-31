# domino
from domino.api import (matrix,
                        attribute,
                        icon)
from domino_edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

# ui
from domino_edition.ui import division_ui

dt = pm.datatypes


class Foot01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    module = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "foot"
    side = "C"
    index = 0
    description = "발 입니다. 원하는 관절의 수를 지정할 수 있습니다. leg_2jnt_01과 연결될 수 있습니다."


class Foot01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))
    _m2 = matrix.get_matrix_from_pos((0, -2, -1))
    _m3 = matrix.get_matrix_from_pos((-1, -2, 0))
    _m3.rotate = dt.EulerRotation((0, -90, 0)).asQuaternion()
    _m4 = matrix.get_matrix_from_pos((1, -2, 0))
    _m4.rotate = dt.EulerRotation((0, -90, 0)).asQuaternion()
    _m5 = matrix.get_matrix_from_pos((0, -2, 2))

    def __init__(self, node=None, data=None):
        self._identifier = Foot01Identifier(self)
        super(Foot01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Foot01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2, self._m3, self._m4, self._m5],
                        "multi": True},
        })
        return preset


class Foot01Guide(piece.Guide):

    def guide(self):
        data = self.data(Foot01Data.SELF)
        if len(data["anchors"]) == 5:
            ui = division_ui.DivisionUI()
            ui.line_edit.setText("3")
            if ui.exec_():
                div_value = int(ui.line_edit.text())
                d = []
                for i, v in enumerate(range(div_value)):
                    d.append(matrix.get_matrix_from_pos((0, -1, i + 1)))
                self.ddata._data["anchors"].extend(d)
            else:
                return False

        data = self.data(Foot01Data.SELF)
        pos = []
        pos.append(super(Foot01Guide, self).guide())
        heel_pos = self.create_position(pos[0], data["anchors"][1])
        in_pos = self.create_position(pos[0], data["anchors"][2])
        out_pos = self.create_position(pos[0], data["anchors"][3])
        toe_pos = self.create_position(pos[0], data["anchors"][4])

        temp = pm.createNode("transform")
        icon.guide_orientation(temp, pos[0])
        attribute.unlock(temp, ["sx", "sy", "sz"])
        temp.attr("s").set(0.5, 0.5, 0.5)
        pm.makeIdentity(temp, apply=True, scale=True)
        icon.replace(temp, in_pos)
        pm.delete(temp)
        temp = pm.createNode("transform")
        icon.guide_orientation(temp, pos[0])
        attribute.unlock(temp, ["sx", "sy", "sz"])
        temp.attr("s").set(0.5, 0.5, 0.5)
        pm.makeIdentity(temp, apply=True, scale=True)
        icon.replace(temp, out_pos)
        pm.delete(temp)
        self.create_display_crv(pos[0], [pos[0], heel_pos, toe_pos, out_pos, in_pos])

        chain_m = data["anchors"][5:]
        parent = pos[0]
        for i, m in enumerate(chain_m):
            parent = self.create_position(parent, m)
            pos.append(parent)
        self.create_display_crv(pos[0], pos)


class Foot01Rig(piece.Rig):

    def objects(self, context):
        super(Foot01Rig, self).objects(context)

        data = self.data(Foot01Data.SELF)
        assembly_data = self.data(Foot01Data.ASSEMBLY)

    def attributes(self, context):
        super(Foot01Rig, self).attributes(context)

    def operators(self, context):
        super(Foot01Rig, self).operators(context)

    def connections(self, context):
        super(Foot01Rig, self).connections(context)


class Foot01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Foot01Data(node=node, data=data)
        self._guide = Foot01Guide(self._ddata)
        self._rig = Foot01Rig(self._ddata)

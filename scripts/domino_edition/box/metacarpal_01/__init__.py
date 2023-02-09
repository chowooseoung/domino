# built-ins
import os

# maya
from pymel import core as pm

# ui
from domino_edition.ui import division_ui

# domino
from domino.api import (matrix,
                        vector)
from domino_edition.api import piece

dt = pm.datatypes


class Metacarpal01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "metacarpal"
    side = "C"
    index = 0
    description = "손바닥뼈입니다. 원하는 관절의 수를 지정할 수 있습니다."


class Metacarpal01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Metacarpal01Identifier(self)
        super(Metacarpal01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Metacarpal01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [],
                        "multi": True},
            "offset": {"typ": "doubleAngle",
                       "value": 0,
                       "keyable": False,
                       "channelBox": True},
            "offset_matrix": {"typ": "matrix",
                              "value": self._m1},
        })
        return preset


class Metacarpal01Guide(piece.Guide):

    def guide(self):
        data = self.data(Metacarpal01Data.SELF)
        if not data["anchors"]:
            ui = division_ui.DivisionUI()
            if ui.exec_():
                div_value = int(ui.line_edit.text())
                d = []
                for i, v in enumerate(range(div_value)):
                    d.append(matrix.get_matrix_from_pos((0, 0, i * -1)))
                self.ddata._data["anchors"] = d
            else:
                return False

        data = self.data(Metacarpal01Data.SELF)
        pos = []
        pos.append(super(Metacarpal01Guide, self).guide())
        for i, m in enumerate(data["anchors"][1:]):
            pos.append(self.create_position(pos[i], m))
        self.create_display_crv(pos[0], pos)
        self.create_orientation(pos[0], pos[1])


class Metacarpal01Rig(piece.Rig):

    def objects(self, context):
        super(Metacarpal01Rig, self).objects(context)

        data = self.data(Metacarpal01Data.SELF)
        assembly_data = self.data(Metacarpal01Data.ASSEMBLY)

        fk_color = self.get_fk_ctl_color()

        orient_xyz = matrix.OrientXYZ(dt.Matrix(data["offset_matrix"]))
        normal = orient_xyz.z

        root_m = dt.Matrix(data["anchors"][0])
        root = self.create_root(context, root_m.translate)

        matrices = [dt.Matrix(x) for x in data["anchors"]]
        positions = [m.translate for m in matrices]
        matrices = matrix.get_chain_matrix(positions, normal, self.ddata.negate)
        matrices.append(matrix.set_matrix_position(matrices[-1], positions[-1]))

        name = self.naming("main", _s="ctl")
        distance = vector.get_distance(positions[0], positions[1])
        self.main_ctl, self.main_loc = self.create_ctl(context=context, parent=root, name=name, parent_ctl=None,
                                                       color=fk_color, keyable_attrs=["tx", "ty", "tz",
                                                                                      "rx", "ry", "rz",
                                                                                      "sx", "sy", "sz"], m=matrices[0],
                                                       shape="circle3", cns=False, width=distance * 2)
        self.ctls = []
        self.locs = []
        ctl = self.main_ctl
        for i, m in enumerate(matrices):
            name = self.naming(f"{i}", _s="ctl")
            index = i - 1 if i == len(matrices) - 1 else i + 1
            distance = vector.get_distance(positions[i], positions[index])
            ctl, loc = self.create_ctl(context=context, parent=root, name=name, parent_ctl=ctl, color=fk_color,
                                       keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"], m=m,
                                       shape="cube", cns=False, width=distance, height=distance, depth=distance)
            self.ctls.append(ctl)
            self.locs.append(loc)

        ratio = 1.0 / len(self.ctls)
        value = 0
        for i, ctl in enumerate(self.ctls):
            blend_m = pm.createNode("blendMatrix")
            blend_m.attr("envelope").set(value)
            pm.connectAttr(self.main_ctl.attr("matrix"), blend_m.attr("target[0].targetMatrix"))
            pm.connectAttr(blend_m.attr("outputMatrix"), ctl.attr("offsetParentMatrix"))
            value += ratio

        # refs
        self.refs = []
        for i, loc in enumerate(self.locs):
            name = self.naming(f"{i}", "ref", _s="ctl")
            ref = self.create_ref(context=context,
                                  name=name,
                                  anchor=True,
                                  m=loc)
            self.refs.append(ref)

        # jnts
        uni_scale = False
        if assembly_data["force_uni_scale"]:
            uni_scale = True
        self.jnts = []
        jnt = None
        for i, ref in enumerate(self.refs):
            name = self.naming(f"{i}", _s="jnt")
            jnt = self.create_jnt(context=context,
                                  parent=jnt,
                                  name=name,
                                  description=f"{i}",
                                  ref=ref,
                                  m=matrices[i],
                                  leaf=False,
                                  uni_scale=uni_scale)
            self.jnts.append(jnt)

    def attributes(self, context):
        super(Metacarpal01Rig, self).attributes(context)

    def operators(self, context):
        super(Metacarpal01Rig, self).operators(context)

    def connections(self, context):
        super(Metacarpal01Rig, self).connections(context)


class Metacarpal01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Metacarpal01Data(node=node, data=data)
        self._guide = Metacarpal01Guide(self._ddata)
        self._rig = Metacarpal01Rig(self._ddata)

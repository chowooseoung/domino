# domino
from domino.core import matrix, vector
from domino.edition.api import piece

# ui
from domino.edition.ui import division_ui

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
    name = "chain"
    side = "C"
    index = 0
    description = "fk chain."


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
                        "value": [],
                        "multi": True},
            "offset": {"typ": "doubleAngle",
                       "value": 0,
                       "keyable": False,
                       "channelBox": True},
            "offset_matrix": {"typ": "matrix",
                              "value": self._m1},
            "guide_orientation": {"typ": "bool",
                                  "value": False,
                                  "keyable": False},
        })
        return preset


class ChainFk01Guide(piece.Guide):

    def guide(self):
        data = self.data(ChainFk01Data.SELF)
        if not data["anchors"]:
            ui = division_ui.DivisionUI()
            if ui.exec_():
                div_value = int(ui.line_edit.text())
                d = []
                for i, v in enumerate(range(div_value)):
                    d.append(matrix.get_matrix_from_pos((i, 0, 0)))
                self.ddata._data["anchors"] = d
            else:
                return False

        data = self.data(ChainFk01Data.SELF)
        pos = []
        pos.append(super(ChainFk01Guide, self).guide())
        for i, m in enumerate(data["anchors"][1:]):
            pos.append(self.create_position(pos[i], m))
        self.create_display_crv(pos[0], pos)
        self.create_orientation(pos[0], pos[1])


class ChainFk01Rig(piece.Rig):

    def objects(self, context):
        super(ChainFk01Rig, self).objects(context)

        data = self.data(ChainFk01Data.SELF)
        assembly_data = self.data(ChainFk01Data.ASSEMBLY)

        fk_color = self.get_fk_ctl_color()

        orient_xyz = matrix.OrientXYZ(dt.Matrix(data["offset_matrix"]))
        normal = orient_xyz.z

        root_m = dt.Matrix(data["anchors"][0])
        root = self.create_root(context, root_m.translate)

        matrices = [dt.Matrix(x) for x in data["anchors"]]
        positions = [m.translate for m in matrices]
        if not data["guide_orientation"]:
            matrices = matrix.get_chain_matrix(positions, normal, self.ddata.negate)
            matrices.append(matrix.set_matrix_position(matrices[-1], positions[-1]))

        self.ctls = []
        self.locs = []
        loc = root
        ctl = None
        for i, m in enumerate(matrices):
            name = self.naming(f"{i}", _s="ctl")
            index = i - 1 if i == len(matrices) - 1 else i + 1
            distance = vector.get_distance(positions[i], positions[index])
            ctl, loc = self.create_ctl(context=context,
                                       parent=loc,
                                       name=name,
                                       parent_ctl=ctl,
                                       color=fk_color,
                                       keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                       m=m,
                                       shape="cube",
                                       cns=False,
                                       width=distance,
                                       height=1,
                                       depth=1,
                                       po=(distance / 2, 0, 0))
            self.ctls.append(ctl)
            self.locs.append(loc)

        # refs
        self.refs = []
        for i, loc in enumerate(self.locs):
            name = self.naming(f"{i}", "ref", _s="ctl")
            ref = self.create_ref(context=context, name=name, anchor=True, m=loc)
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

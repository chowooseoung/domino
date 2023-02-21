# domino
from domino.core.api import matrix, vector
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Shoulder01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "shoulder"
    side = "C"
    index = 0
    description = "사람의 빗장뼈 입니다. arm_2jnt_01는 shoulder_01과 연결될 수 있습니다."


class Shoulder01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))
    _m2 = matrix.get_matrix_from_pos((2, 0, 0))
    _m3 = matrix.get_matrix_from_pos((3, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Shoulder01Identifier(self)
        super(Shoulder01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Shoulder01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2, self._m3],
                        "multi": True},
            "offset": {"typ": "doubleAngle",
                       "value": 0,
                       "keyable": False,
                       "channelBox": True},
            "offset_matrix": {"typ": "matrix",
                              "value": self._m1},
        })
        return preset


class Shoulder01Guide(piece.Guide):

    def guide(self):
        data = self.data(Shoulder01Data.SELF)
        root = super(Shoulder01Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        self.create_display_crv(root, [root, pos])
        self.create_orientation(root, pos)
        pos1 = self.create_position(root, data["anchors"][2])
        self.create_display_crv(root, [root, pos1])


class Shoulder01Rig(piece.Rig):

    def objects(self, context):
        super(Shoulder01Rig, self).objects(context)

        data = self.data(Shoulder01Data.SELF)
        assembly_data = self.data(Shoulder01Data.ASSEMBLY)

        fk_color = self.get_fk_ctl_color()

        orient_xyz = matrix.OrientXYZ(dt.Matrix(data["offset_matrix"]))
        normal = orient_xyz.z

        start_pos, end_pos = [dt.Matrix(x).translate for x in data["anchors"][:-1]]

        root = self.create_root(context, start_pos)

        look_at_m = matrix.get_matrix_look_at(start_pos, end_pos, normal, "xz", self.ddata.negate)
        orbit_m = matrix.get_matrix_from_pos(dt.Matrix(data["anchors"][-1]).translate)
        if self.ddata.negate:
            orbit_m = matrix.get_mirror_matrix(orbit_m)
            orbit_m = matrix.set_matrix_position(orbit_m, dt.Matrix(data["anchors"][-1]).translate)

        name = self.naming("", _s="ctl")
        distance = vector.get_distance(start_pos, dt.Matrix(data["anchors"][-1]).translate)
        offset = distance / -2 if self.ddata.negate else distance / 2
        self.shoulder_ctl, self.shoulder_loc = self.create_ctl(context=context,
                                                               parent=None,
                                                               name=name,
                                                               parent_ctl=None,
                                                               color=fk_color,
                                                               keyable_attrs=["tx", "ty", "tz",
                                                                              "rx", "ry", "rz"],
                                                               m=look_at_m,
                                                               shape="cube",
                                                               width=distance,
                                                               height=distance / 3,
                                                               depth=distance / 3,
                                                               po=(offset, 0, 0))
        name = self.naming("", "ref", _s="ctl")
        self.shoulder_ref = self.create_ref(context=context, name=name, anchor=False, m=self.shoulder_loc)

        uni_scale = False
        if assembly_data["force_uni_scale"]:
            uni_scale = True
        name = self.naming("", _s="jnt")
        self.shoulder_jnt = self.create_jnt(context=context,
                                            parent=None,
                                            name=name,
                                            description="",
                                            ref=self.shoulder_ref,
                                            m=look_at_m,
                                            leaf=False,
                                            uni_scale=uni_scale)

        name = self.naming("orbit", _s="ctl")
        self.orbit_ctl, self.orbit_loc = self.create_ctl(context=context,
                                                         parent=self.shoulder_loc,
                                                         name=name,
                                                         parent_ctl=None,
                                                         color=fk_color,
                                                         keyable_attrs=["tx", "ty", "tz",
                                                                        "rx", "ry", "rz"],
                                                         m=orbit_m,
                                                         shape="circle3",
                                                         width=1.5)
        name = self.naming("orbit", "ref", _s="ctl")
        self.orbit_ref = self.create_ref(context=context, name=name, anchor=True, m=self.orbit_loc)

    def attributes(self, context):
        super(Shoulder01Rig, self).attributes(context)
        self.create_host(context)

    def operators(self, context):
        super(Shoulder01Rig, self).operators(context)

    def connections(self, context):
        super(Shoulder01Rig, self).connections(context)

        host = self.host()
        if "auto_clavicle" not in context:
            context["auto_clavicle"] = {}
        context["auto_clavicle"][str(self.ddata.identifier)] = [self.shoulder_ctl, self.root, host]


class Shoulder01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Shoulder01Data(node=node, data=data)
        self._guide = Shoulder01Guide(self._ddata)
        self._rig = Shoulder01Rig(self._ddata)

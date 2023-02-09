# domino
from domino.api import (matrix,
                        vector,
                        nurbs)
from domino_edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Neck01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "neck"
    side = "C"
    index = 0
    description = "목 입니다."


class Neck01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))  # root
    _m2 = matrix.get_matrix_from_pos((0, 0.5, 0))  # cv1
    _m3 = matrix.get_matrix_from_pos((0, 1.5, 0))  # neck
    _m4 = matrix.get_matrix_from_pos((0, 1, 0))  # cv2
    _m5 = matrix.get_matrix_from_pos((0, 1.2, -0.5))  # orbit

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
                        "value": [self._m1, self._m2, self._m3, self._m4, self._m5],
                        "multi": True},
            "offset": {"typ": "doubleAngle",
                       "value": 0,
                       "keyable": False,
                       "channelBox": True},
            "offset_matrix": {"typ": "matrix",
                              "value": self._m1},
            "division": {"typ": "long",
                         "value": 2,
                         "keyable": False},
            "max_stretch": {"typ": "float",
                            "value": 1.1,
                            "keyable": False},
            "max_squash": {"typ": "float",
                           "value": 0.95,
                           "keyable": False},
            "stretch_volume_fcurve": {"typ": "float",
                                      "value": 0,
                                      "keyable": False,
                                      "fcurve": {"name": "stretch_volume_fcurve_UU",
                                                 "driven": [],
                                                 "driver": [],
                                                 "floatChange": [0.0, 0.5, 1.0],
                                                 "inAngle": [0.0, 0.0, 0.0],
                                                 "inTangentType": ["auto", "auto", "auto"],
                                                 "inWeight": [1.0, 1.0, 1.0],
                                                 "lock": [True, True, True],
                                                 "outAngle": [0.0, 0.0, 0.0],
                                                 "outTangentType": ["auto", "auto", "auto"],
                                                 "outWeight": [1.0, 1.0, 1.0],
                                                 "time": [],
                                                 "type": "animCurveUU",
                                                 "valueChange": [0.0, -1.0, 0.0],
                                                 "weightedTangents": [False]}},
            "squash_volume_fcurve": {"typ": "float",
                                     "value": 0,
                                     "keyable": False,
                                     "fcurve": {"name": "squash_volume_fcurve_UU",
                                                "driven": [],
                                                "driver": [],
                                                "floatChange": [0.0, 0.5, 1.0],
                                                "inAngle": [0.0, 0.0, 0.0],
                                                "inTangentType": ["auto", "auto", "auto"],
                                                "inWeight": [1.0, 1.0, 1.0],
                                                "lock": [True, True, True],
                                                "outAngle": [0.0, 0.0, 0.0],
                                                "outTangentType": ["auto", "auto", "auto"],
                                                "outWeight": [1.0, 1.0, 1.0],
                                                "time": [],
                                                "type": "animCurveUU",
                                                "valueChange": [0.0, 1.0, 0.0],
                                                "weightedTangents": [False]}}
        })
        return preset


class Neck01Guide(piece.Guide):

    def guide(self):
        data = self.data(Neck01Data.SELF)
        root = super(Neck01Guide, self).guide()
        pos1 = self.create_position(root, data["anchors"][1])
        pos2 = self.create_position(root, data["anchors"][2])
        pos3 = self.create_position(pos2, data["anchors"][3])
        pos4 = self.create_position(pos2, data["anchors"][4])
        self.create_orientation(root, pos1)

        self.create_display_crv(root, [root, pos1, pos3, pos2], degree=3)


class Neck01Rig(piece.Rig):

    def objects(self, context):
        super(Neck01Rig, self).objects(context)

        data = self.data(Neck01Data.SELF)
        assembly_data = self.data(Neck01Data.ASSEMBLY)

        uni_scale = False
        if assembly_data["force_uni_scale"]:
            uni_scale = True

        ik_color = self.get_ik_ctl_color()
        fk_color = self.get_fk_ctl_color()

        orient_xyz = matrix.OrientXYZ(dt.Matrix(data["offset_matrix"]))
        normal = orient_xyz.z

        positions = [dt.Matrix(x).translate for x in data["anchors"]]

        root = self.create_root(context, positions[0])
        root_m = root.getMatrix(worldSpace=True)

        name = self.naming("orbit", _s="ctl")
        m = matrix.set_matrix_position(root_m, positions[-1])
        self.orbit_ctl, self.orbit_loc = self.create_ctl(context=context,
                                                         parent=None,
                                                         name=name,
                                                         parent_ctl=None,
                                                         color=ik_color,
                                                         keyable_attrs=["rx", "ry", "rz"],
                                                         m=m,
                                                         shape="circle3",
                                                         width=0.5)

        name = self.naming("ik", _s="ctl")
        m = matrix.set_matrix_position(root_m, positions[2])
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context,
                                                   parent=self.orbit_loc,
                                                   name=name,
                                                   parent_ctl=self.orbit_ctl,
                                                   color=ik_color,
                                                   keyable_attrs=["tx", "ty", "tz",
                                                                  "rx", "ry", "rz"],
                                                   m=m,
                                                   shape="arrow4",
                                                   width=3)
        name = self.naming("lookAtStart", "grp", _s="ctl")
        m = matrix.get_matrix_look_at(positions[0], positions[1], normal, "xz", self.ddata.negate)
        self.look_at_start_grp = matrix.transform(root, name, m, True)

        name = self.naming("cv1", "pos", _s="ctl")
        m = matrix.set_matrix_position(m, positions[1])
        self.cv1_pos = matrix.transform(self.look_at_start_grp, name, m, True)

        name = self.naming("lookAtEnd", "grp", _s="ctl")
        m = matrix.get_matrix_look_at(positions[2], positions[3], normal, "xz", self.ddata.negate)
        self.look_at_end_grp = matrix.transform(self.ik_loc, name, m, True)

        name = self.naming("cv2", "pos", _s="ctl")
        m = matrix.set_matrix_position(m, positions[3])
        self.cv2_pos = matrix.transform(self.look_at_end_grp, name, m, True)

        name = self.naming("original", "crv", _s="ctl")
        _p = [dt.Vector() for _ in range(4)]
        self.original_crv = nurbs.create(root,
                                         name,
                                         degree=3,
                                         positions=_p,
                                         m=root_m,
                                         bezier=False,
                                         vis=True,
                                         inherits=True,
                                         display_type=1)

        name = self.naming("deform", "crv", _s="ctl")
        self.deform_crv = nurbs.create(root,
                                       name,
                                       degree=3,
                                       positions=_p,
                                       m=root_m,
                                       bezier=False,
                                       vis=True,
                                       inherits=False,
                                       display_type=1)
        nurbs.constraint(self.deform_crv, [self.look_at_start_grp, self.cv1_pos, self.cv2_pos, self.ik_loc])

        neck_jnt_positions = nurbs.point_on_curve(self.deform_crv, data["division"])
        parent_ctl = self.ik_ctl
        parent = root
        self.fk_ctls = []
        self.fk_locs = []
        for i, p in enumerate(neck_jnt_positions):
            name = self.naming(f"fk{i}", _s="ctl")
            if i < len(neck_jnt_positions) - 1:
                m = matrix.get_matrix_look_at(p, neck_jnt_positions[i + 1], normal, "xz", self.ddata.negate)
            else:
                m = matrix.set_matrix_position(m, neck_jnt_positions[i])
            fk_ctl, fk_loc = self.create_ctl(context=context,
                                             parent=parent,
                                             name=name,
                                             parent_ctl=parent_ctl,
                                             color=fk_color,
                                             keyable_attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz", "ro"],
                                             m=m,
                                             shape="cube",
                                             width=0.1,
                                             height=1,
                                             depth=1)
            parent_ctl = fk_ctl
            parent = fk_ctl
            self.fk_ctls.append(fk_ctl)
            self.fk_locs.append(fk_loc)

        name = self.naming("volume", "crv", _s="ctl")
        self.volume_crv = nurbs.create(root,
                                       name,
                                       degree=1,
                                       positions=[dt.Vector((0, 0, 0)) for _ in self.fk_ctls],
                                       m=root.getMatrix(worldSpace=True),
                                       bezier=False,
                                       vis=False,
                                       inherits=False,
                                       display_type=1)

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

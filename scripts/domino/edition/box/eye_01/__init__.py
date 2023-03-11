# domino
from domino.core import matrix, vector, nurbs, operators, callback
from domino.edition.api import piece

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
    _m2 = matrix.get_matrix_from_pos((0, 0, 3))
    _m3 = matrix.get_matrix_from_pos((0, 1, 0))

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
                        "value": [self._m1, self._m2, self._m3],
                        "multi": True},
            "mirror_behaviour": {"typ": "bool",
                                 "value": False,
                                 "keyable": False},
            "aim_space_switch_array": {"typ": "string",
                                       "value": ""}
        })
        return preset


class Eye01Guide(piece.Guide):

    def guide(self):
        data = self.data(Eye01Data.SELF)
        root = super(Eye01Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        pos1 = self.create_position(root, data["anchors"][2])
        self.create_display_crv(root, [root, pos])


class Eye01Rig(piece.Rig):

    def objects(self, context):
        super(Eye01Rig, self).objects(context)

        data = self.data(Eye01Data.SELF)
        assembly_data = self.data(Eye01Data.ASSEMBLY)

        m0 = dt.Matrix(data["anchors"][0])
        m1 = dt.Matrix(data["anchors"][1])
        m2 = dt.Matrix(data["anchors"][2])

        positions = [dt.Vector(x.translate) for x in [m0, m1, m2]]
        normal = vector.getPlaneNormal(*positions)

        root = self.create_root(context, positions[0])
        fk_color = self.get_fk_ctl_color()
        ik_color = self.get_ik_ctl_color()

        m = matrix.get_matrix_look_at(positions[0], positions[1], normal, "xy", False)

        name = self.naming("aim", "", _s="ctl")
        aim_m = matrix.set_matrix_position(m, positions[1])
        self.aim_ctl, self.aim_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=name,
                                                     parent_ctl=None,
                                                     color=ik_color,
                                                     keyable_attrs=["tx", "ty", "tz"],
                                                     m=aim_m,
                                                     shape="circle3",
                                                     cns=True,
                                                     width=0.5)

        name = self.naming("aim", "target", _s="ctl")
        self.aim_target = matrix.transform(root, name, m, True)

        name = self.naming("aim", "orient", _s="ctl")
        self.aim_orient = matrix.transform(root, name, m, True)

        negate = False
        if data["mirror_behaviour"] and self.ddata.negate:
            negate = True
        m = matrix.get_matrix_look_at(positions[0], positions[1], normal, "xz", negate)
        name = self.naming("", "", _s="ctl")
        self.eye_ctl, self.eye_loc = self.create_ctl(context=context,
                                                     parent=self.aim_target,
                                                     name=name,
                                                     parent_ctl=self.aim_ctl,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz",
                                                                    "rx", "ry", "rz", "ro",
                                                                    "sx", "sy", "sz"],
                                                     m=m,
                                                     shape="circle3",
                                                     cns=False,
                                                     width=1)

        m = matrix.get_matrix_look_at(positions[0], positions[1], normal, "xz", self.ddata.negate)
        name = self.naming("ref", "source", _s="ctl")
        self.ref_source = matrix.transform(self.eye_loc, name, m)

        name = self.naming("display", "crv", _s="ctl")
        display_crv = nurbs.create(parent=root,
                                   name=name,
                                   degree=1,
                                   positions=[(0, 0, 0), (0, 0, 0)],
                                   vis=True,
                                   inherits=False,
                                   display_type=2)
        nurbs.constraint(display_crv, [self.aim_loc, self.ref_source])

        name = self.naming("ref", _s="ctl")
        ref = self.create_ref(context=context, name=name, anchor=True, m=self.ref_source)

        uni_scale = False
        if assembly_data["force_uni_scale"]:
            uni_scale = True

        name = self.naming("", _s="ctl")
        jnt = self.create_jnt(context=context,
                              parent=None,
                              name=name,
                              description="0",
                              ref=ref,
                              m=ref.getMatrix(worldSpace=True),
                              leaf=False,
                              uni_scale=uni_scale)

    def attributes(self, context):
        super(Eye01Rig, self).attributes(context)
        self.create_host(context)

    def operators(self, context):
        super(Eye01Rig, self).operators(context)

        data = self.data(Eye01Data.SELF)
        host = self.host()

        pm.aimConstraint(self.aim_loc,
                         self.aim_target,
                         aimVector=(1, 0, 0),
                         upVector=(0, 1, 0),
                         worldUpType="objectrotation",
                         worldUpObject=self.aim_orient)

        if data["aim_space_switch_array"]:
            source_ctls = self.find_ctls(data["aim_space_switch_array"])
            operators.space_switch(source_ctls, self.aim_ctl, host, attr_name="aim_space_switch")
            script_node = callback.space_switch(source_ctls,
                                                self.aim_ctl,
                                                host,
                                                switch_attr_name="aim_space_switch")
            context["callbacks"].append(script_node)

    def connections(self, context):
        super(Eye01Rig, self).connections(context)


class Eye01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Eye01Data(node=node, data=data)
        self._guide = Eye01Guide(self._ddata)
        self._rig = Eye01Rig(self._ddata)

# domino
from domino.core.api import (attribute)
from domino.core.api import matrix, vector
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Jaw01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "jaw"
    side = "C"
    index = 0
    description = "턱 입니다."


class Jaw01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))
    _m2 = matrix.get_matrix_from_pos((0, -1, 1))
    _m3 = matrix.get_matrix_from_pos((0, -2, 3))

    def __init__(self, node=None, data=None):
        self._identifier = Jaw01Identifier(self)
        super(Jaw01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Jaw01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2, self._m3],
                        "multi": True},
            "sliding_angle": {"typ": "double",
                              "value": -10},
            "sliding": {"typ": "double",
                        "value": 1,
                        "minValue": 0,
                        "maxValue": 10}
        })
        return preset


class Jaw01Guide(piece.Guide):

    def guide(self):
        data = self.data(Jaw01Data.SELF)
        root = super(Jaw01Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        pos1 = self.create_position(pos, data["anchors"][2])
        self.create_display_crv(root, [root, pos, pos1])


class Jaw01Rig(piece.Rig):

    def objects(self, context):
        super(Jaw01Rig, self).objects(context)

        data = self.data(Jaw01Data.SELF)
        assembly_data = self.data(Jaw01Data.ASSEMBLY)

        m0 = dt.Matrix(data["anchors"][0])
        m1 = dt.Matrix(data["anchors"][1])
        m2 = dt.Matrix(data["anchors"][2])

        positions = [dt.Vector(x.translate) for x in [m0, m1, m2]]
        normal = vector.getPlaneNormal(*positions) * -1

        root = self.create_root(context, positions[0])
        fk_color = self.get_fk_ctl_color()
        ik_color = self.get_ik_ctl_color()

        aim_m = matrix.get_matrix_look_at(positions[-1], positions[1], normal, "xz", True)
        name = self.naming("jawAim", _s="ctl")
        self.aim_ctl, self.aim_loc = self.create_ctl(context=context,
                                                     parent=root,
                                                     name=name,
                                                     parent_ctl=None,
                                                     color=ik_color,
                                                     keyable_attrs=["tx", "ty", "tz"],
                                                     m=aim_m,
                                                     shape="circle",
                                                     cns=False,
                                                     ro=(0, 0, 90))

        distance = vector.get_distance(positions[0], positions[-1])
        m = matrix.get_matrix_look_at(positions[0], positions[-1], normal, "-xz", True)
        name = self.naming("", "", _s="ctl")
        self.jaw_ctl, self.jaw_loc = self.create_ctl(context=context,
                                                     parent=root,
                                                     name=name,
                                                     parent_ctl=self.aim_ctl,
                                                     color=fk_color,
                                                     keyable_attrs=["rx", "ry", "rz"],
                                                     m=m,
                                                     shape="cube",
                                                     cns=False,
                                                     width=distance,
                                                     depth=distance / 2,
                                                     po=(distance / 2, 0, 0))
        name = self.naming("rot", _s="ctl")
        self.rot_obj = matrix.transform(root, name, m, True)

        sliding_m = matrix.get_matrix_look_at(positions[0], positions[1], normal, "-xz", True)
        name = self.naming("sliding", "space", _s="ctl")
        self.sliding_grp = matrix.transform(root, name, sliding_m, True)

        name = self.naming("sliding", "aim", _s="ctl")
        self.sliding_aim = matrix.transform(self.sliding_grp, name, m, True)

        name = self.naming("", "ref", _s="ctl")
        ref = self.create_ref(context, name, True, self.sliding_aim)

        uni_scale = False
        if assembly_data["force_uni_scale"]:
            uni_scale = True
        jnt = self.create_jnt(context=context,
                              parent=None,
                              name=name,
                              description="",
                              ref=ref,
                              m=m,
                              leaf=False,
                              uni_scale=uni_scale)

    def attributes(self, context):
        super(Jaw01Rig, self).attributes(context)
        host = self.create_host(context)

        data = self.data(Jaw01Data.SELF)
        self.sliding_attr = attribute.add(host,
                                          "sliding",
                                          "double",
                                          value=data["sliding"],
                                          minValue=0,
                                          keyable=True)
        self.sliding_angle_attr = attribute.add(host,
                                                "sliding_angle",
                                                "double",
                                                value=data["sliding_angle"],
                                                keyable=True)

    def operators(self, context):
        super(Jaw01Rig, self).operators(context)

        jaw_npo = self.jaw_ctl.getParent()
        pm.aimConstraint(self.aim_loc,
                         jaw_npo,
                         aimVector=(1, 0, 0),
                         upVector=(0, 0, 1),
                         worldUpType="object",
                         worldUpObject=self.root)
        pm.orientConstraint(self.jaw_loc, self.sliding_aim)
        pm.orientConstraint(self.jaw_loc, self.rot_obj)

        md = pm.createNode("multiplyDivide")
        md.attr("input1X").set(-1)
        pm.connectAttr(self.sliding_angle_attr, md.attr("input2X"))

        adl = pm.createNode("addDoubleLinear")
        pm.connectAttr(self.rot_obj.attr("rz"), adl.attr("input1"))
        pm.connectAttr(md.attr("outputX"), adl.attr("input2"))

        clamp = pm.createNode("clamp")
        clamp.attr("minR").set(-360)
        pm.connectAttr(adl.attr("output"), clamp.attr("inputR"))

        data = self.data(Jaw01Data.SELF)
        distance = vector.get_distance(dt.Matrix(data["anchors"][1]).translate, dt.Matrix(data["anchors"][-1]))

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(clamp.attr("outputR"), md.attr("input1X"))
        md.attr("input2X").set(distance / -300)
        sliding_value = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(sliding_value, md.attr("input1X"))
        pm.connectAttr(self.sliding_attr, md.attr("input2X"))

        pm.connectAttr(md.attr("outputX"), self.sliding_grp.attr("tx"))

    def connections(self, context):
        super(Jaw01Rig, self).connections(context)


class Jaw01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Jaw01Data(node=node, data=data)
        self._guide = Jaw01Guide(self._ddata)
        self._rig = Jaw01Rig(self._ddata)

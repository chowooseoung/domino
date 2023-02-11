# domino
from domino.api import (matrix,
                        attribute,
                        fcurve,
                        joint,
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
    _m5 = matrix.get_matrix_from_pos((0, 1.6, 0))  # lookAt
    _m6 = matrix.get_matrix_from_pos((0, 1.2, -0.5))  # orbit

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
                        "value": [self._m1, self._m2, self._m3, self._m4, self._m5, self._m6],
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
            "max_stretch": {"typ": "double",
                            "value": 1.1,
                            "keyable": False},
            "max_squash": {"typ": "double",
                           "value": 0.9,
                           "keyable": False},
            "stretch_volume_fcurve": {"typ": "double",
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
            "squash_volume_fcurve": {"typ": "double",
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
        pos5 = self.create_position(pos2, data["anchors"][5])
        self.create_orientation(root, pos1)

        self.create_display_crv(root, [root, pos1, pos3, pos2, pos4], degree=3)
        self.create_display_crv(root, [root, pos1, pos3, pos2], degree=1, thickness=1)


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
        normal = orient_xyz.y

        m0 = dt.Matrix(data["anchors"][0])  # root
        m1 = dt.Matrix(data["anchors"][1])  # cv1
        m2 = dt.Matrix(data["anchors"][2])  # neck
        m3 = dt.Matrix(data["anchors"][3])  # cv2
        m4 = dt.Matrix(data["anchors"][4])  # lookAt
        m5 = dt.Matrix(data["anchors"][5])  # orbit

        pos0 = m0.translate
        pos1 = m1.translate
        pos2 = m2.translate
        pos3 = m3.translate
        pos4 = m4.translate
        pos5 = m5.translate

        root = self.create_root(context, pos0)
        root_m = root.getMatrix(worldSpace=True)

        name = self.naming("orbit", _s="ctl")
        look_at_ik_m = matrix.get_matrix_look_at(pos2, pos4, normal, "xz", self.ddata.negate)
        m = matrix.set_matrix_position(look_at_ik_m, pos5)
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
        m = matrix.set_matrix_position(look_at_ik_m, pos2)
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context,
                                                   parent=self.orbit_loc,
                                                   name=name,
                                                   parent_ctl=self.orbit_ctl,
                                                   color=ik_color,
                                                   keyable_attrs=["tx", "ty", "tz",
                                                                  "rx", "ry", "rz"],
                                                   m=m,
                                                   shape="arrow4",
                                                   width=3,
                                                   ro=(0, 0, 90))
        name = self.naming("lookAtStart", "grp", _s="ctl")
        m = matrix.get_matrix_look_at(pos0, pos1, normal, "xz", self.ddata.negate)
        self.look_at_start_grp = matrix.transform(root, name, m, True)

        name = self.naming("cv1", "pos", _s="ctl")
        m = matrix.set_matrix_position(m, pos1)
        self.cv1_pos = matrix.transform(self.look_at_start_grp, name, m, False)

        name = self.naming("lookAtEnd", "grp", _s="ctl")
        m = matrix.get_matrix_look_at(pos2, pos3, normal, "-xz", self.ddata.negate)
        self.look_at_end_grp = matrix.transform(self.ik_loc, name, m, True)

        name = self.naming("cv2", "pos", _s="ctl")
        m = matrix.set_matrix_position(m, pos3)
        self.cv2_pos = matrix.transform(self.look_at_end_grp, name, m, False)

        name = self.naming("original", "crv", _s="ctl")
        self.original_crv = nurbs.create(root,
                                         name,
                                         degree=3,
                                         positions=[pos0, pos1, pos3, pos2],
                                         m=root_m,
                                         bezier=False,
                                         vis=False,
                                         inherits=True,
                                         display_type=1)

        name = self.naming("deform", "crv", _s="ctl")
        self.deform_crv = nurbs.create(root,
                                       name,
                                       degree=3,
                                       positions=[pos0, pos1, pos3, pos2],
                                       m=root_m,
                                       bezier=False,
                                       vis=False,
                                       inherits=False,
                                       display_type=1)
        nurbs.constraint(self.deform_crv, [self.look_at_start_grp, self.cv1_pos, self.cv2_pos, self.ik_loc])

        neck_jnt_positions = nurbs.point_on_curve(self.deform_crv, data["division"])
        name = self.naming("SP%s", _s="jnt")
        self.sp_chain = joint.add_chain(root,
                                        name,
                                        neck_jnt_positions,
                                        normal,
                                        negate=self.ddata.negate)

        name = self.naming("SP", "ikh", _s="ctl")
        self.sp_ik_h = joint.sp_ikh(root, name, self.sp_chain, self.deform_crv)

        name = self.naming("startUp", "loc", _s="ctl")
        self.start_up_loc = matrix.transform(self.root, name, self.sp_chain[0].getMatrix(worldSpace=True))

        name = self.naming("lockOrient", "loc", _s="ctl")
        self.lock_orient_loc = matrix.transform(self.ik_loc, name, self.sp_chain[-1].getMatrix(worldSpace=True))

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

        name = self.naming("volumeOrig", "crv", _s="ctl")
        positions = [x.getTranslation(worldSpace=True) for x in self.fk_ctls]
        self.orig_volume_crv = nurbs.create(root,
                                            name,
                                            degree=1,
                                            positions=positions,
                                            m=root_m,
                                            bezier=False,
                                            vis=False,
                                            inherits=True,
                                            display_type=1)
        name = self.naming("volumeDeform", "crv", _s="ctl")
        self.deform_volume_crv = nurbs.create(root,
                                              name,
                                              degree=1,
                                              positions=positions,
                                              m=root_m,
                                              bezier=False,
                                              vis=False,
                                              inherits=False,
                                              display_type=1)
        nurbs.constraint(self.deform_volume_crv, self.fk_ctls)

        refs = []
        for i in range(len(self.fk_ctls)):
            anchor = False if i < len(self.fk_ctls) - 1 else True
            name = self.naming(f"{i}", "ref", _s="ctl")
            m = self.fk_locs[i]
            refs.append(self.create_ref(context=context, name=name, anchor=anchor, m=m))

        parent = None
        for i, r in enumerate(refs):
            name = self.naming(f"{i}", _s="jnt")
            parent = self.create_jnt(context=context,
                                     parent=parent,
                                     name=name,
                                     description=str(i),
                                     ref=r,
                                     m=r.getMatrix(worldSpace=True),
                                     leaf=False,
                                     uni_scale=uni_scale)

    def attributes(self, context):
        super(Neck01Rig, self).attributes(context)
        host = self.create_host(context)
        data = self.data(Neck01Data.SELF)

        self.stretch_squash = attribute.add(host,
                                            "stretch_squash_enable",
                                            "double",
                                            keyable=True,
                                            minValue=0,
                                            maxValue=1,
                                            defaultValue=1)
        self.max_stretch = attribute.add(host,
                                         "max_stretch",
                                         "double",
                                         keyable=True,
                                         minValue=1,
                                         defaultValue=data["max_stretch"])
        self.max_squash = attribute.add(host,
                                        "max_squash",
                                        "double",
                                        keyable=True,
                                        minValue=0.001,
                                        maxValue=1,
                                        defaultValue=data["max_squash"])
        self.tangent0 = attribute.add(host,
                                      "tangent0",
                                      "double",
                                      keyable=True,
                                      minValue=0,
                                      defaultValue=1)
        self.tangent1 = attribute.add(host,
                                      "tangent1",
                                      "double",
                                      keyable=True,
                                      minValue=0,
                                      defaultValue=1)
        self.lock_orient_0 = attribute.add(host,
                                           "lock_orient",
                                           "double",
                                           keyable=True,
                                           minValue=0,
                                           maxValue=1,
                                           defaultValue=1)
        self.volume = attribute.add(host,
                                    "volume",
                                    "double",
                                    keyable=True,
                                    minValue=0,
                                    maxValue=1,
                                    defaultValue=1)
        self.stretch_attrs = []
        self.squash_attrs = []
        stretch_volume_fcurve = self.root.attr("stretch_volume_fcurve").inputs()[0]
        squash_volume_fcurve = self.root.attr("squash_volume_fcurve").inputs()[0]
        stretch_values = fcurve.get_fcurve_values(stretch_volume_fcurve, data["division"])
        for i, value in enumerate(stretch_values):
            self.stretch_attrs.append(attribute.add(self.root,
                                                    f"stretch_volume_value{i}",
                                                    "double",
                                                    keyable=False,
                                                    defaultValue=value))
        squash_values = fcurve.get_fcurve_values(squash_volume_fcurve, data["division"])
        for i, value in enumerate(squash_values):
            self.squash_attrs.append(attribute.add(self.root,
                                                   f"squash_volume_value{i}",
                                                   "double",
                                                   keyable=False,
                                                   defaultValue=value))
        self.fk_vis = attribute.add(host,
                                    "fk_vis",
                                    "bool",
                                    keyable=True,
                                    defaultValue=False)

    def operators(self, context):
        super(Neck01Rig, self).operators(context)
        data = self.data(Neck01Data.SELF)

        # fk vis
        for ctl in self.fk_ctls:
            shapes = ctl.getShapes()
            for shape in shapes:
                pm.connectAttr(self.fk_vis, shape.attr("v"))

        # spline ik handle
        self.sp_ik_h.attr("dTwistControlEnable").set(True)
        self.sp_ik_h.attr("dWorldUpType").set(4)
        self.sp_ik_h.attr("dWorldUpAxis").set(3)
        self.sp_ik_h.attr("dWorldUpVector").set((0, 0, 1))
        self.sp_ik_h.attr("dWorldUpVectorEnd").set((0, 0, 1))
        if self.ddata.negate:
            self.sp_ik_h.attr("dForwardAxis").set(1)
        pm.connectAttr(self.start_up_loc.attr("worldMatrix")[0], self.sp_ik_h.attr("dWorldUpMatrix"))
        pm.connectAttr(self.lock_orient_loc.attr("worldMatrix")[0], self.sp_ik_h.attr("dWorldUpMatrixEnd"))

        # curve info
        original_crv_shape = self.original_crv.getShape()
        curve_info = pm.arclen(original_crv_shape, ch=1)
        original_curve_length = curve_info.attr("arcLength")

        deform_crv_shape = self.deform_crv.getShape()
        curve_info = pm.arclen(deform_crv_shape, ch=1)
        deform_curve_length = curve_info.attr("arcLength")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(deform_curve_length, md.attr("input1X"))
        pm.connectAttr(original_curve_length, md.attr("input2X"))
        deform_curve_ratio = md.attr("outputX")

        # stretch & squash
        condition = pm.createNode("condition")
        pm.connectAttr(deform_curve_ratio, condition.attr("firstTerm"))
        pm.connectAttr(self.max_stretch, condition.attr("secondTerm"))
        condition.attr("operation").set(2)
        pm.connectAttr(self.max_stretch, condition.attr("colorIfTrueR"))
        pm.connectAttr(deform_curve_ratio, condition.attr("colorIfFalseR"))
        max_stretch_multiple = condition.attr("outColorR")

        condition = pm.createNode("condition")
        pm.connectAttr(deform_curve_ratio, condition.attr("firstTerm"))
        pm.connectAttr(self.max_squash, condition.attr("secondTerm"))
        condition.attr("operation").set(5)
        pm.connectAttr(self.max_squash, condition.attr("colorIfTrueR"))
        pm.connectAttr(deform_curve_ratio, condition.attr("colorIfFalseR"))
        max_squash_multiple = condition.attr("outColorR")

        condition = pm.createNode("condition")
        pm.connectAttr(deform_curve_ratio, condition.attr("firstTerm"))
        condition.attr("secondTerm").set(1)
        condition.attr("operation").set(3)
        pm.connectAttr(max_stretch_multiple, condition.attr("colorIfTrueR"))
        pm.connectAttr(max_squash_multiple, condition.attr("colorIfFalseR"))
        stretch_squash_multiple = condition.attr("outColorR")

        bta = pm.createNode("blendTwoAttr")
        bta.attr("input")[0].set(1)
        pm.connectAttr(stretch_squash_multiple, bta.attr("input")[1])
        pm.connectAttr(self.stretch_squash, bta.attr("attributesBlender"))
        stretch_squash_switch = bta.attr("output")

        for j in self.sp_chain:
            md = pm.createNode("multiplyDivide")
            pm.connectAttr(stretch_squash_switch, md.attr("input1X"))
            md.attr("input2X").set(j.attr("tx").get())
            pm.connectAttr(md.attr("outputX"), j.attr("tx"))

        # volume
        orig_volume_crv_shape = self.orig_volume_crv.getShape()
        curve_info = pm.arclen(orig_volume_crv_shape, ch=1)
        orig_volume_curve_length = curve_info.attr("arcLength")

        deform_volume_crv_shape = self.deform_volume_crv.getShape()
        curve_info = pm.arclen(deform_volume_crv_shape, ch=1)
        deform_volume_curve_length = curve_info.attr("arcLength")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(deform_volume_curve_length, md.attr("input1X"))
        pm.connectAttr(orig_volume_curve_length, md.attr("input2X"))
        volume_curve_ratio = md.attr("outputX")

        pma = pm.createNode("plusMinusAverage")
        pma.attr("operation").set(2)
        pm.connectAttr(volume_curve_ratio, pma.attr("input1D")[0])
        pma.attr("input1D")[1].set(1)

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(3)
        pm.connectAttr(pma.attr("output1D"), md.attr("input1X"))
        md.attr("input2X").set(2)
        pow_value = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(3)
        pm.connectAttr(pow_value, md.attr("input1X"))
        md.attr("input2X").set(0.5)
        abs_value = md.attr("outputX")

        for i in range(data["division"]):
            condition = pm.createNode("condition")
            condition.attr("operation").set(3)
            pm.connectAttr(stretch_squash_switch, condition.attr("firstTerm"))
            condition.attr("secondTerm").set(1)
            pm.connectAttr(self.stretch_attrs[i], condition.attr("colorIfTrueR"))
            pm.connectAttr(self.squash_attrs[i], condition.attr("colorIfFalseR"))

            md = pm.createNode("multiplyDivide")
            pm.connectAttr(condition.attr("outColorR"), md.attr("input1X"))
            pm.connectAttr(self.volume, md.attr("input2X"))
            volume_multiple = md.attr("outputX")

            md = pm.createNode("multiplyDivide")
            pm.connectAttr(abs_value, md.attr("input1X"))
            pm.connectAttr(volume_multiple, md.attr("input2X"))

            pma = pm.createNode("plusMinusAverage")
            pma.attr("input3D")[0].set((1, 1, 1))
            pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dx"))
            pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dy"))
            pm.connectAttr(md.attr("outputX"), pma.attr("input3D[1].input3Dz"))

            attribute.unlock(self.fk_locs[i], ["sx", "sy", "sz"])
            pm.connectAttr(pma.attr("output3D"), self.fk_locs[i].attr("s"))

        # lock orient
        for i, npo in enumerate([x.getParent() for x in self.fk_ctls]):
            if i == len(self.fk_ctls) - 1:
                pb = pm.createNode("pairBlend")
                pb.attr("rotInterpolation").set(1)
                pm.connectAttr(self.lock_orient_0, pb.attr("weight"))

                target = self.sp_chain[-1]
                target_parent = target.getParent()

                mult_m = pm.createNode("multMatrix")
                pm.connectAttr(self.lock_orient_loc.attr("worldMatrix")[0], mult_m.attr("matrixIn")[0])
                pm.connectAttr(target_parent.attr("worldInverseMatrix")[0], mult_m.attr("matrixIn")[1])

                decom_m = pm.createNode("decomposeMatrix")
                pm.connectAttr(mult_m.attr("matrixSum"), decom_m.attr("inputMatrix"))
                lock_orient = decom_m.attr("outputRotate")

                pm.connectAttr(lock_orient, pb.attr("inRotate2"))
                pm.connectAttr(pb.attr("outRotate"), self.sp_chain[-1].attr("r"))
            pm.connectAttr(self.sp_chain[i].attr("dagLocalMatrix"), npo.attr("offsetParentMatrix"))

        # tangent
        distance = pm.createNode("distanceBetween")
        decom = pm.createNode("decomposeMatrix")
        pm.connectAttr(self.look_at_start_grp.attr("worldMatrix")[0], decom.attr("inputMatrix"))
        pm.connectAttr(decom.attr("outputTranslate"), distance.attr("point1"))
        decom = pm.createNode("decomposeMatrix")
        pm.connectAttr(self.ik_loc.attr("worldMatrix")[0], decom.attr("inputMatrix"))
        pm.connectAttr(decom.attr("outputTranslate"), distance.attr("point2"))
        distance = distance.attr("distance")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(original_curve_length, md.attr("input1X"))
        md.attr("input2X").set(original_curve_length.get())
        original_crv_ratio = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(original_crv_ratio, md.attr("input1X"))
        md.attr("input2X").set(distance.get())
        scaled_distance = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        md.attr("operation").set(2)
        pm.connectAttr(distance, md.attr("input1X"))
        pm.connectAttr(scaled_distance, md.attr("input2X"))
        normalize_distance = md.attr("outputX")

        cv1_tx = self.cv1_pos.attr("tx").get()
        md = pm.createNode("multiplyDivide")
        pm.connectAttr(normalize_distance, md.attr("input1X"))
        md.attr("input2X").set(cv1_tx)
        cv1_scaled_offset_value = md.attr("outputX")

        cv2_tx = self.cv2_pos.attr("tx").get()
        md = pm.createNode("multiplyDivide")
        pm.connectAttr(normalize_distance, md.attr("input1X"))
        md.attr("input2X").set(cv2_tx)
        cv2_scaled_offset_value = md.attr("outputX")

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(self.tangent0, md.attr("input1X"))
        pm.connectAttr(self.tangent1, md.attr("input1Y"))
        pm.connectAttr(cv1_scaled_offset_value, md.attr("input2X"))
        pm.connectAttr(cv2_scaled_offset_value, md.attr("input2Y"))
        tan0_value = md.attr("outputX")
        tan1_value = md.attr("outputY")

        pm.connectAttr(tan0_value, self.cv1_pos.attr("tx"))
        pm.connectAttr(tan1_value, self.cv2_pos.attr("tx"))

    def connections(self, context):
        super(Neck01Rig, self).connections(context)


class Neck01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Neck01Data(node=node, data=data)
        self._guide = Neck01Guide(self._ddata)
        self._rig = Neck01Rig(self._ddata)

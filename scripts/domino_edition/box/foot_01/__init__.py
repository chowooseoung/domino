# domino
from domino.api import (matrix,
                        vector,
                        attribute,
                        controller,
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
    description = ("발 입니다. 원하는 관절의 수를 지정할 수 있습니다. leg_2jnt_01과 연결될 수 있습니다."
                   "\n- 주의사항 : heel, tip, toe 는 일직선 위에 놓여 있어야 합니다. "
                   "in, out, toe 는 normal 을 구하는데 사용됩니다.\n"
                   "fk chain 또한 같은 평면 위에 있어야합니다.")


class Foot01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))  # root
    _m2 = matrix.get_matrix_from_pos((0, -2, -1))  # heel
    _m3 = matrix.get_matrix_from_pos((-1, -2, 0))  # in
    _m3.rotate = dt.EulerRotation((0, -90, 0)).asQuaternion()
    _m4 = matrix.get_matrix_from_pos((1, -2, 0))  # out
    _m4.rotate = dt.EulerRotation((0, -90, 0)).asQuaternion()
    _m5 = matrix.get_matrix_from_pos((0, -2, 1))  # tip
    _m6 = matrix.get_matrix_from_pos((0, -2, 2))  # toe

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
                        "value": [],
                        "multi": True},
            "roll_angle": {"typ": "float",
                           "value": 20},
            "connector": {"typ": "string",
                          "value": "default"}
        })
        return preset


class Foot01Guide(piece.Guide):

    def guide(self):
        data = self.data(Foot01Data.SELF)
        if len(data["anchors"]) == 0:
            ui = division_ui.DivisionUI()
            ui.line_edit.setText("3")
            if ui.exec_():
                div_value = int(ui.line_edit.text())
                d = []
                for i, v in enumerate(range(div_value)):
                    d.append(matrix.get_matrix_from_pos((0, -1, i + 1)))
                self.ddata._data["anchors"].extend([Foot01Data._m1])
                self.ddata._data["anchors"].extend(d)
                self.ddata._data["anchors"].extend([Foot01Data._m2,
                                                    Foot01Data._m3,
                                                    Foot01Data._m4,
                                                    Foot01Data._m5,
                                                    Foot01Data._m6])
            else:
                return False

        data = self.data(Foot01Data.SELF)
        pos = []
        pos.append(super(Foot01Guide, self).guide())

        chain_m = data["anchors"][1:-5]
        parent = pos[0]
        for i, m in enumerate(chain_m):
            parent = self.create_position(parent, m)
            pos.append(parent)
        self.create_display_crv(pos[0], pos)

        heel_pos = self.create_position(pos[0], data["anchors"][-5])
        in_pos = self.create_position(heel_pos, data["anchors"][-4])
        out_pos = self.create_position(heel_pos, data["anchors"][-3])
        tip_pos = self.create_position(heel_pos, data["anchors"][-2])
        toe_pos = self.create_position(heel_pos, data["anchors"][-1])

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
        self.create_display_crv(pos[0], [in_pos, out_pos, heel_pos, tip_pos, toe_pos])


class Foot01Rig(piece.Rig):

    def objects(self, context):
        super(Foot01Rig, self).objects(context)

        data = self.data(Foot01Data.SELF)
        assembly_data = self.data(Foot01Data.ASSEMBLY)

        root_m = dt.Matrix(data["anchors"][0])
        root_pos = root_m.translate
        heel_m = dt.Matrix(data["anchors"][-5])
        heel_pos = heel_m.translate
        in_m = dt.Matrix(data["anchors"][-4])
        in_pos = in_m.translate
        out_m = dt.Matrix(data["anchors"][-3])
        out_pos = out_m.translate
        tip_m = dt.Matrix(data["anchors"][-2])
        tip_pos = tip_m.translate
        toe_m = dt.Matrix(data["anchors"][-1])
        toe_pos = toe_m.translate

        fk_positions = [dt.Matrix(x).translate for x in data["anchors"][1:-5]]
        fk_normal = vector.getPlaneNormal(root_pos, fk_positions[0], fk_positions[1])
        fk_matrices = matrix.get_chain_matrix(fk_positions, fk_normal, self.ddata.negate)
        fk_matrices.append(matrix.set_matrix_position(fk_matrices[-1], fk_positions[-1]))

        normal = vector.getPlaneNormal(in_pos, out_pos, toe_pos) * -1

        root = self.create_root(context, root_pos)
        fk_color = self.get_fk_ctl_color()
        ik_color = self.get_ik_ctl_color()

        heel_m = matrix.get_matrix_look_at(heel_pos, toe_pos, normal, "xz", self.ddata.negate)
        tip_m = matrix.get_matrix_look_at(tip_pos, toe_pos, normal, "xz", self.ddata.negate)
        toe_m = matrix.set_matrix_position(heel_m, toe_pos)

        name = self.naming("roll", _s="ctl")
        m = matrix.get_matrix_look_at(dt.Vector(0, 0, 0), normal, fk_normal, "xz", True)
        m = matrix.set_matrix_position(m, root_pos)
        self.roll_ctl, self.roll_loc = self.create_ctl(context=context,
                                                       parent=root,
                                                       name=name,
                                                       parent_ctl=None,
                                                       color=ik_color,
                                                       keyable_attrs=["ry", "rz"],
                                                       m=m,
                                                       shape="dodecahedron",
                                                       cns=False,
                                                       width=2,
                                                       height=2,
                                                       depth=2,
                                                       ro=(0, 0, 90))

        name = self.naming("in", _s="ctl")
        self.in_ctl, self.in_loc = self.create_ctl(context=context,
                                                   parent=root,
                                                   name=name,
                                                   parent_ctl=None,
                                                   color=ik_color,
                                                   keyable_attrs=["rx", "ry", "rz"],
                                                   m=in_m,
                                                   shape="halfmoon",
                                                   cns=False,
                                                   width=1,
                                                   height=0.2,
                                                   depth=0.5,
                                                   ro=(0, 90, 0))
        name = self.naming("out", _s="ctl")
        self.out_ctl, self.out_loc = self.create_ctl(context=context,
                                                     parent=self.in_loc,
                                                     name=name,
                                                     parent_ctl=self.in_ctl,
                                                     color=ik_color,
                                                     keyable_attrs=["rx", "ry", "rz"],
                                                     m=out_m,
                                                     shape="halfmoon",
                                                     cns=False,
                                                     width=1,
                                                     height=0.2,
                                                     depth=0.5,
                                                     ro=(0, -90, 0))
        name = self.naming("heel", _s="ctl")
        offset = vector.get_distance(heel_pos, tip_pos)
        self.heel_ctl, self.heel_loc = self.create_ctl(context=context,
                                                       parent=self.out_loc,
                                                       name=name,
                                                       parent_ctl=self.out_ctl,
                                                       color=ik_color,
                                                       keyable_attrs=["rx", "ry", "rz"],
                                                       m=heel_m,
                                                       shape="halfmoon",
                                                       cns=False,
                                                       width=offset / 2,
                                                       po=(0, 0, 0),
                                                       ro=(90, 0, 180 if self.ddata.negate else 0))
        name = self.naming("tip", _s="ctl")
        offset = vector.get_distance(tip_pos, toe_pos)
        self.tip_ctl, self.tip_loc = self.create_ctl(context=context,
                                                     parent=self.heel_loc,
                                                     name=name,
                                                     parent_ctl=self.heel_ctl,
                                                     color=ik_color,
                                                     keyable_attrs=["rx", "ry", "rz"],
                                                     m=tip_m,
                                                     shape="square",
                                                     cns=False,
                                                     width=offset,
                                                     height=offset,
                                                     po=(0, 0, 0),
                                                     ro=(90, 0, 0))
        name = self.naming("toe", _s="ctl")
        self.toe_ctl, self.toe_loc = self.create_ctl(context=context,
                                                     parent=self.tip_loc,
                                                     name=name,
                                                     parent_ctl=self.tip_ctl,
                                                     color=ik_color,
                                                     keyable_attrs=["rx", "ry", "rz"],
                                                     m=toe_m,
                                                     shape="halfmoon",
                                                     cns=False,
                                                     width=offset,
                                                     po=(0, 0, 0),
                                                     ro=(90, 0, 0 if self.ddata.negate else 180))

        self.rev_fk_ctls = []
        self.rev_fk_locs = []
        ctl = self.toe_ctl
        loc = self.toe_loc
        for i, m in enumerate(reversed(fk_matrices)):
            name = self.naming(f"rev{i}", _s="ctl")
            ctl, loc = self.create_ctl(context=context,
                                       parent=loc,
                                       name=name,
                                       parent_ctl=ctl,
                                       color=ik_color,
                                       keyable_attrs=["rx", "ry", "rz"],
                                       m=m,
                                       shape="circle3",
                                       cns=False,
                                       width=0.5)
            self.rev_fk_ctls.append(ctl)
            self.rev_fk_locs.append(loc)

        name = self.naming("legRef", "space", _s="ctl")
        self.leg_space = matrix.transform(self.rev_fk_locs[-1], name, root.attr("offsetParentMatrix").get(), True)

        name = self.naming("ref0", "space", _s="ctl")
        ref0_obj = controller.child(self.leg_space, name=name, shape="")
        ref0_obj.setMatrix(root_m, worldSpace=True)

        ctl = self.rev_fk_ctls[-1]
        loc = self.leg_space
        self.fk_ctls = []
        self.fk_locs = []
        for i in range(len(fk_matrices) - 1):
            name = self.naming(f"fk{i}", _s="ctl")
            offset = vector.get_distance(fk_positions[i], fk_positions[i + 1]) / 2.0
            po = offset * -1 if self.ddata.negate else offset
            ctl, loc = self.create_ctl(context=context,
                                       parent=loc,
                                       name=name,
                                       parent_ctl=ctl,
                                       color=fk_color,
                                       keyable_attrs=["rx", "ry", "rz"],
                                       m=fk_matrices[i],
                                       shape="cube",
                                       cns=False,
                                       width=offset * 2,
                                       height=offset,
                                       depth=1,
                                       po=(po, 0, 0))
            name = self.naming("inv", "rot", _s="ctl")
            controller.npo(ctl, name)
            self.fk_ctls.append(ctl)
            self.fk_locs.append(loc)

        self.refs = []
        name = self.naming(0, "ref", _s="ctl")
        ref = self.create_ref(context=context,
                              name=name,
                              anchor=True,
                              m=ref0_obj)
        self.refs.append(ref)
        for i, loc in enumerate(self.fk_locs):
            name = self.naming(i + 1, "ref", _s="ctl")
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
        parent = None
        for i, ref in enumerate(self.refs[1:]):
            if i == 1:
                pm.connectAttr(parent.attr("message"), root.attr("jnts")[1])
            name = self.naming(f"{i}", _s="jnt")
            m = ref.getMatrix(worldSpace=True)
            parent = self.create_jnt(context=context,
                                     parent=parent,
                                     name=name,
                                     description=f"{i}",
                                     ref=ref,
                                     m=m,
                                     leaf=False,
                                     uni_scale=uni_scale)
            self.jnts.append(parent)

    def attributes(self, context):
        super(Foot01Rig, self).attributes(context)
        host = self.create_host(context)

        data = self.data(Foot01Data.SELF)
        name = str(self.ddata.identifier)
        self.roll_angle_attrs = []
        for i, ctl in enumerate(self.fk_ctls):
            attr = attribute.add(host,
                                 f"{name}_angle{i}",
                                 "float",
                                 value=data["roll_angle"],
                                 defaultValue=data["roll_angle"],
                                 keyable=True)
            self.roll_angle_attrs.append(attr)

    def operators(self, context):
        super(Foot01Rig, self).operators(context)

        # roll - rev
        reversed_rev_fk_ctls = list(reversed(self.rev_fk_ctls))
        limit_value = self.roll_angle_attrs[0]
        input_value = self.roll_ctl.attr("rz")
        for i, attr in enumerate(self.roll_angle_attrs):
            cmp = pm.createNode("clamp")
            pm.connectAttr(attr, cmp.attr("maxR"))
            pm.connectAttr(input_value, cmp.attr("inputR"))

            npo = reversed_rev_fk_ctls[i].getParent()
            pm.connectAttr(cmp.attr("outputR"), npo.attr("rz"))

            if i < len(self.roll_angle_attrs) - 1:
                md = pm.createNode("multiplyDivide")
                md.attr("input1X").set(-1)
                pm.connectAttr(limit_value, md.attr("input2X"))

                adl = pm.createNode("addDoubleLinear")
                pm.connectAttr(md.attr("outputX"), adl.attr("input1"))
                pm.connectAttr(self.roll_ctl.attr("rz"), adl.attr("input2"))
                input_value = adl.attr("output")

                adl = pm.createNode("addDoubleLinear")
                pm.connectAttr(limit_value, adl.attr("input1"))
                pm.connectAttr(self.roll_angle_attrs[i + 1], adl.attr("input2"))
                limit_value = adl.attr("output")
        md = pm.createNode("multiplyDivide")
        md.attr("input1X").set(-1)
        pm.connectAttr(limit_value, md.attr("input2X"))

        adl = pm.createNode("addDoubleLinear")
        pm.connectAttr(md.attr("outputX"), adl.attr("input1"))
        pm.connectAttr(self.roll_ctl.attr("rz"), adl.attr("input2"))
        input_value = adl.attr("output")

        cmp = pm.createNode("clamp")
        cmp.attr("maxR").set(360)
        pm.connectAttr(input_value, cmp.attr("inputR"))

        npo = reversed_rev_fk_ctls[-1].getParent()
        pm.connectAttr(cmp.attr("outputR"), npo.attr("rz"))

        # roll - heel
        cmp = pm.createNode("clamp")
        cmp.attr("minR").set(-360)
        pm.connectAttr(self.roll_ctl.attr("rz"), cmp.attr("inputR"))

        md = pm.createNode("multiplyDivide")
        pm.connectAttr(cmp.attr("outputR"), md.attr("input1X"))
        md.attr("input2X").set(-1)

        npo = self.heel_ctl.getParent()
        pm.connectAttr(md.attr("outputX"), npo.attr("ry"))

        # roll - in, out
        cmp = pm.createNode("clamp")
        cmp.attr("maxR").set(360)
        pm.connectAttr(self.roll_ctl.attr("ry"), cmp.attr("inputR"))

        npo = self.in_ctl.getParent()
        pm.connectAttr(cmp.attr("outputR"), npo.attr("rx"))

        cmp = pm.createNode("clamp")
        cmp.attr("minR").set(-360)
        pm.connectAttr(self.roll_ctl.attr("ry"), cmp.attr("inputR"))

        npo = self.out_ctl.getParent()
        pm.connectAttr(cmp.attr("outputR"), npo.attr("rx"))

        # fk ctl
        fk_ctls_reverse = list(reversed(self.fk_ctls))
        for i, ctl in enumerate(fk_ctls_reverse):
            inv_rot = ctl.getParent()
            npo = inv_rot.getParent()
            rev_npo = self.rev_fk_ctls[i + 1].getParent()

            inv_m = pm.createNode("inverseMatrix")
            pm.connectAttr(rev_npo.attr("matrix"), inv_m.attr("inputMatrix"))

            decom_m = pm.createNode("decomposeMatrix")
            pm.connectAttr(inv_m.attr("outputMatrix"), decom_m.attr("inputMatrix"))
            pm.connectAttr(decom_m.attr("outputRotate"), inv_rot.attr("rotate"))

            inv_m = pm.createNode("inverseMatrix")
            pm.connectAttr(self.rev_fk_ctls[i + 1].attr("matrix"), inv_m.attr("inputMatrix"))

            decom_m = pm.createNode("decomposeMatrix")
            pm.connectAttr(inv_m.attr("outputMatrix"), decom_m.attr("inputMatrix"))
            pm.connectAttr(decom_m.attr("outputRotate"), npo.attr("rotate"))

    def connections(self, context):
        super(Foot01Rig, self).connections(context)

        data = self.data(Foot01Data.SELF)
        parent_component = self.ddata.parent
        parent_data = parent_component.data(parent_component.SELF)
        if data["connector"] == "leg_2jnt_01" and parent_data["module"] == "leg_2jnt_01":
            connector_data = context["leg_2jnt_01"][str(parent_component.identifier)]
            ik_local_loc, ikh, last_ref, fk_ik_attr = connector_data

            pm.disconnectAttr(self.root.attr("offsetParentMatrix"))
            attribute.unlock(self.root, ["tx", "ty", "tz", "rx", "ry", "rz"])
            cons = pm.parentConstraint(last_ref, self.root, maintainOffset=True)
            pm.connectAttr(ik_local_loc.attr("worldMatrix"), self.root.attr("offsetParentMatrix"))
            pm.delete(cons)
            attribute.lock(self.root, ["tx", "ty", "tz", "rx", "ry", "rz"])

            pm.parent(ikh, self.rev_fk_locs[-1])

            pm.parentConstraint(last_ref, self.leg_space, maintainOffset=True)

            for i, ctl in enumerate(self.fk_ctls):
                inv_rot = ctl.getParent()
                npo = inv_rot.getParent()

                pb = pm.createNode("pairBlend")
                pb.attr("rotInterpolation").set(1)
                pm.connectAttr(fk_ik_attr, pb.attr("weight"))
                pm.connectAttr(inv_rot.attr("rotate").inputs(plugs=True)[0], pb.attr("inRotate2"))
                pm.disconnectAttr(inv_rot.attr("rotate"))
                pm.connectAttr(pb.attr("outRotate"), inv_rot.attr("rotate"))

                pb = pm.createNode("pairBlend")
                pb.attr("rotInterpolation").set(1)
                pm.connectAttr(fk_ik_attr, pb.attr("weight"))
                pm.connectAttr(npo.attr("rotate").inputs(plugs=True)[0], pb.attr("inRotate2"))
                pm.disconnectAttr(npo.attr("rotate"))
                pm.connectAttr(pb.attr("outRotate"), npo.attr("rotate"))

            vis_ctls = [self.roll_ctl,
                        self.in_ctl,
                        self.out_ctl,
                        self.heel_ctl,
                        self.tip_ctl,
                        self.toe_ctl] + self.rev_fk_ctls
            for ctl in vis_ctls:
                shapes = ctl.getShapes()
                for shape in shapes:
                    pm.connectAttr(fk_ik_attr, shape.attr("v"))


class Foot01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Foot01Data(node=node, data=data)
        self._guide = Foot01Guide(self._ddata)
        self._rig = Foot01Rig(self._ddata)

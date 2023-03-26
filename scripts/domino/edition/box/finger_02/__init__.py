# domino
from domino.core import attribute, joint, matrix, vector, operators, callback
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Finger02Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "finger"
    side = "C"
    index = 0
    description = "엄지손가락 입니다. fk와 ik를 가지고 있습니다."


class Finger02Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))
    _m2 = matrix.get_matrix_from_pos((2, 0, 0))
    _m3 = matrix.get_matrix_from_pos((4, 0.01, 0))
    _m4 = matrix.get_matrix_from_pos((6, -0.01, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Finger02Identifier(self)
        super(Finger02Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Finger02Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2, self._m3, self._m4],
                        "multi": True},
            "offset_pole_vec": {"typ": "double",
                                "value": 1,
                                "channelBox": True},
            "offset_pole_vec_matrix": {"typ": "matrix",
                                       "value": dt.Matrix()},
            "ik_space_switch_array": {"typ": "string",
                                      "value": ""},
        })
        return preset


class Finger02Guide(piece.Guide):

    def guide(self):
        data = self.data(Finger02Data.SELF)
        root = super(Finger02Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        pos1 = self.create_position(pos, data["anchors"][2])
        pos2 = self.create_position(pos1, data["anchors"][3])
        pv = self.create_pv_locator(root, [pos, pos1, pos2])
        self.create_display_crv(root, [root, pos, pos1, pos2])
        self.create_display_crv(root, [pos1, pv], thickness=1)


class Finger02Rig(piece.Rig):

    def objects(self, context):
        super(Finger02Rig, self).objects(context)

        data = self.data(Finger02Data.SELF)
        assembly_data = self.data(Finger02Data.ASSEMBLY)

        m0 = dt.Matrix(data["anchors"][0])
        m1 = dt.Matrix(data["anchors"][1])
        m2 = dt.Matrix(data["anchors"][2])
        m3 = dt.Matrix(data["anchors"][3])

        positions = [dt.Vector(x.translate) for x in [m0, m1, m2, m3]]
        normal = vector.getPlaneNormal(*positions[1:])

        root = self.create_root(context, positions[0])
        fk_color = self.get_fk_ctl_color()
        ik_color = self.get_ik_ctl_color()

        # fk ctl
        fk0_m = matrix.get_matrix_look_at(positions[0], positions[1], normal, "xz", self.ddata.negate)
        name = self.naming("fk0", "", _s="ctl")
        offset = ((positions[1] - positions[0]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        height_depth = offset
        self.fk0_ctl, self.fk0_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=name,
                                                     parent_ctl=None,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                                     m=fk0_m,
                                                     shape="cube",
                                                     cns=False,
                                                     width=offset * 2,
                                                     height=height_depth,
                                                     depth=height_depth,
                                                     po=(po, 0, 0))

        fk1_m = matrix.get_matrix_look_at(positions[1], positions[2], normal, "xz", self.ddata.negate)
        name = self.naming("fk1", "", _s="ctl")
        offset = ((positions[2] - positions[1]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        height_depth *= 0.9
        self.fk1_ctl, self.fk1_loc = self.create_ctl(context=context,
                                                     parent=self.fk0_loc,
                                                     name=name,
                                                     parent_ctl=self.fk0_ctl,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                                     m=fk1_m,
                                                     shape="cube",
                                                     cns=False,
                                                     width=offset * 2,
                                                     height=height_depth,
                                                     depth=height_depth,
                                                     po=(po, 0, 0))
        fk2_m = matrix.get_matrix_look_at(positions[2], positions[3], normal, "xz", self.ddata.negate)
        name = self.naming("fk2", "", _s="ctl")
        offset = ((positions[3] - positions[2]) / 2.0).length()
        po = offset * -1 if self.ddata.negate else offset
        height_depth *= 0.9
        self.fk2_ctl, self.fk2_loc = self.create_ctl(context=context,
                                                     parent=self.fk1_loc,
                                                     name=name,
                                                     parent_ctl=self.fk1_ctl,
                                                     color=fk_color,
                                                     keyable_attrs=["tx", "ty", "tz",
                                                                    "rx", "ry", "rz", "ro",
                                                                    "sx", "sy", "sz"],
                                                     m=fk2_m,
                                                     shape="cube",
                                                     cns=False,
                                                     width=offset * 2,
                                                     height=height_depth,
                                                     depth=height_depth,
                                                     po=(po, 0, 0))

        # ik ctl
        axis = "xz" if self.ddata.negate else "-xz"
        ik_m = matrix.get_matrix_look_at(positions[-1], positions[-2], normal, axis, self.ddata.negate)
        if self.ddata.negate:
            ik_m.scale = (1, 1, -1)
        name = self.naming("ik", "", _s="ctl")
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context, parent=self.fk0_loc, name=name,
                                                   parent_ctl=self.fk0_ctl, color=ik_color,
                                                   keyable_attrs=["tx", "ty", "tz"], m=ik_m, shape="circle", cns=True,
                                                   width=offset, ro=(0, 0, 90))

        # ik jnt
        name = self.naming("SC%s", _s="jnt")
        self.ik_sc_jnts = joint.add_chain(self.fk0_loc, name, [positions[1], positions[-1]], normal, vis=False)
        name = self.naming("SC", "ikh", _s="jnt")
        self.ik_sc_ikh = joint.ikh(self.ik_loc, name, self.ik_sc_jnts, solver="ikSCsolver")

        # poleVec loc
        name = self.naming("poleVec", "grp", _s="ctl")
        m = matrix.get_matrix_look_at(positions[1], positions[-1], normal, "xz", negate=False)
        self.sc_space_grp = matrix.transform(self.fk0_loc, name, m, True)
        name = self.naming("poleVec", "loc", _s="ctl")
        pole_vec_pos = dt.Matrix(data["offset_pole_vec_matrix"]).translate
        pole_vec_m = matrix.set_matrix_position(fk1_m, pole_vec_pos)
        self.pole_vec_obj = matrix.transform(self.sc_space_grp, name, pole_vec_m, offsetParentMatrix=True)

        # ik jnt
        name = self.naming("ik%s", _s="jnt")
        self.ik_jnts = joint.add_chain(self.fk0_loc,
                                       name,
                                       positions[1:],
                                       normal,
                                       last_orient=fk2_m,
                                       negate=self.ddata.negate,
                                       vis=False)

        name = self.naming("RP", "ikh", _s="jnt")
        self.ik_ikh = joint.ikh(self.ik_loc, name, self.ik_jnts, pole_vector=self.pole_vec_obj)

        # refs
        self.refs = []
        for i, obj in enumerate((self.fk0_loc, self.fk1_loc, self.fk2_loc)):
            name = self.naming(f"{i}", "ref", _s="ctl")
            self.refs.append(self.create_ref(context=context,
                                             name=name,
                                             anchor=True,
                                             m=obj))
        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            parent = None
            for i, ref in enumerate(self.refs):
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

    def attributes(self, context):
        super(Finger02Rig, self).attributes(context)
        self.create_host(context)

        self.roll_attr = attribute.add(self.ik_ctl,
                                       "roll",
                                       typ="double",
                                       defaultValue=0,
                                       keyable=True)

    def operators(self, context):
        super(Finger02Rig, self).operators(context)
        data = self.data(Finger02Data.SELF)
        host = self.host()

        pm.connectAttr(self.ik_sc_jnts[0].attr("dagLocalMatrix"), self.sc_space_grp.attr("offsetParentMatrix"))

        if not self.ddata.negate:
            md = pm.createNode("multiplyDivide")
            md.attr("input1X").set(-1)
            pm.connectAttr(self.roll_attr, md.attr("input2X"))
            self.roll_attr = md.attr("outputX")
        pm.connectAttr(self.roll_attr, self.sc_space_grp.attr("rx"))

        fk0_npo = self.fk0_ctl.getParent()
        if pm.controller(fk0_npo, query=True):
            fk0_npo = fk0_npo.getParent()
        fk1_npo = self.fk1_ctl.getParent()
        if pm.controller(fk1_npo, query=True):
            fk1_npo = fk1_npo.getParent()
        fk2_npo = self.fk2_ctl.getParent()
        if pm.controller(fk2_npo, query=True):
            fk2_npo = fk2_npo.getParent()
        pm.connectAttr(self.ik_jnts[0].attr("dagLocalMatrix"), fk1_npo.attr("offsetParentMatrix"))
        pm.connectAttr(self.ik_jnts[1].attr("dagLocalMatrix"), fk2_npo.attr("offsetParentMatrix"))

        # space switch
        if data["ik_space_switch_array"]:
            source_ctls = self.find_ctls(data["ik_space_switch_array"])
            operators.space_switch(source_ctls, self.ik_ctl, host, attr_name="ik_space_switch")
            script_node = callback.space_switch(source_ctls,
                                                self.ik_ctl,
                                                host,
                                                switch_attr_name="ik_space_switch")
            context["callbacks"].append(script_node)

    def connections(self, context):
        super(Finger02Rig, self).connections(context)


class Finger02Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Finger02Data(node=node, data=data)
        self._guide = Finger02Guide(self._ddata)
        self._rig = Finger02Rig(self._ddata)

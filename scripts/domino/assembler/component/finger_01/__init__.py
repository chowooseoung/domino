# domino
from domino.lib import attribute, matrix, vector, hierarchy
from domino.lib.rigging import operators, callback, joint
from domino import assembler

# built-ins
import os
import uuid

# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "finger"
    side = "C"
    index = 0
    description = "엄지를 제외한 손가락입니다. fk와 ik를 가지고 있습니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset_pole_vec": {"type": "double", "minValue": 0},
        "offset_pole_vec_matrix": {"type": "matrix"},
        "ik_space_switch_array": {"type": "string"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))
        m2 = matrix.set_matrix_translate(m, (2, 0.01, 0))
        m3 = matrix.set_matrix_translate(m, (4, 0, 0))
        m4 = matrix.set_matrix_translate(m, (6, 0, 0))
        return m1, m2, m3, m4

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "offset_pole_vec": 1,
        "offset_pole_vec_matrix": list(om2.MMatrix()),
    })
    return common_preset


def guide_recipe():
    return {
        "position": [
            (0, "fk0"),
            (1, "fk1"),  # parent node index, extension
            (2, "fk2")
        ],
        "pole_vec": ((0, 1, 2), "poleVec"),  # source node indexes, extension
        "display_curve": [
            ((0, 1, 2, 3), "dpCrv"),  # source node indexes, extension
        ],
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        m0 = om2.MMatrix(data["anchors"][0])
        m1 = om2.MMatrix(data["anchors"][1])
        m2 = om2.MMatrix(data["anchors"][2])
        m3 = om2.MMatrix(data["anchors"][3])

        positions = [om2.MVector(list(x)[12:-1]) for x in [m0, m1, m2, m3]]
        normal = vector.get_plane_normal(*positions[:-1])

        root = self.create_root(context)
        fk_color = self.generate_color("fk")
        ik_color = self.generate_color("ik")

        self.distance0 = vector.get_distance(positions[0], positions[1])
        self.distance1 = vector.get_distance(positions[1], positions[2])
        self.distance2 = vector.get_distance(positions[2], positions[3])

        # ik ctl
        axis = "xz" if self.component.negate else "-xz"
        ik_m = matrix.get_look_at_matrix(positions[-1], positions[0], normal, axis, self.component.negate)
        if self.component.negate:
            ik_m = matrix.set_matrix_scale(ik_m, (1, 1, -1))
        offset = ((positions[3] - positions[2]) / 2.0).length()
        self.ik_ctl, self.ik_loc = self.create_ctl(context=context,
                                                   parent=None,
                                                   name=self.generate_name("ik", "", "ctl"),
                                                   parent_ctl=None,
                                                   attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                                   m=ik_m,
                                                   cns=True,
                                                   mirror_config=(0, 0, 1, 0, 0, 0, 0, 0, 0),
                                                   shape_args={
                                                       "shape": "circle",
                                                       "width": offset,
                                                       "ro": (0, 0, 90),
                                                       "color": ik_color
                                                   },
                                                   mirror_ctl_name=self.generate_name("ik", "", "ctl", True))

        # fk ctl
        fk0_m = matrix.get_look_at_matrix(positions[0], positions[1], normal, "xz", self.component.negate)
        offset = ((positions[1] - positions[0]) / 2.0).length()
        po = offset * -1 if self.component.negate else offset
        height_depth = offset
        self.fk0_ctl, self.fk0_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=self.generate_name("fk0", "", "ctl"),
                                                     parent_ctl=self.ik_ctl,
                                                     attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz",
                                                            "sx", "sy", "sz"],
                                                     m=fk0_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "width": offset * 2,
                                                         "height": height_depth,
                                                         "depth": height_depth,
                                                         "po": (po, 0, 0),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk0", "", "ctl", True))

        fk1_m = matrix.get_look_at_matrix(positions[1], positions[2], normal, "xz", self.component.negate)
        offset = ((positions[2] - positions[1]) / 2.0).length()
        po = offset * -1 if self.component.negate else offset
        height_depth *= 0.9
        self.fk1_ctl, self.fk1_loc = self.create_ctl(context=context,
                                                     parent=self.fk0_loc,
                                                     name=self.generate_name("fk1", "", "ctl"),
                                                     parent_ctl=self.fk0_ctl,
                                                     attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz",
                                                            "sx", "sy", "sz"],
                                                     m=fk1_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "width": offset * 2,
                                                         "height": height_depth,
                                                         "depth": height_depth,
                                                         "po": (po, 0, 0),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk1", "", "ctl", True))
        fk2_m = matrix.get_look_at_matrix(positions[2], positions[3], normal, "xz", self.component.negate)
        offset = ((positions[3] - positions[2]) / 2.0).length()
        po = offset * -1 if self.component.negate else offset
        height_depth *= 0.9
        self.fk2_ctl, self.fk2_loc = self.create_ctl(context=context,
                                                     parent=self.fk1_loc,
                                                     name=self.generate_name("fk2", "", "ctl"),
                                                     parent_ctl=self.fk1_ctl,
                                                     attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz",
                                                            "sx", "sy", "sz"],
                                                     m=fk2_m,
                                                     cns=False,
                                                     mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "cube",
                                                         "width": offset * 2,
                                                         "height": height_depth,
                                                         "depth": height_depth,
                                                         "po": (po, 0, 0),
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("fk2", "", "ctl", True))
        # ik jnt
        name = self.generate_name("SC%s", "", "jnt")
        self.ik_sc_jnts = joint.add_chain_joint(root, name, [positions[0], positions[-1]], normal, vis=False)
        name = self.generate_name("SC", "ikh", "jnt")
        self.ik_sc_ikh = joint.ikh(self.ik_loc, name, self.ik_sc_jnts, solver="ikSCsolver")

        # poleVec loc
        name = self.generate_name("SC", "space", "ctl")
        m = matrix.get_look_at_matrix(positions[0], positions[-1], normal, "xz", negate=False)
        self.sc_space_grp = matrix.transform(root, name, m, True)
        name = self.generate_name("poleVec", "loc", "ctl")
        pole_vec_pos = data["offset_pole_vec_matrix"][12:-1]
        pole_vec_m = matrix.set_matrix_translate(fk1_m, pole_vec_pos)
        self.pole_vec_obj = matrix.transform(self.sc_space_grp, name, pole_vec_m, offset_parent_matrix=True)

        # ik jnt
        name = self.generate_name("ik%s", "", "jnt")
        self.ik_jnts = joint.add_chain_joint(root,
                                             name,
                                             positions[:-1],
                                             normal,
                                             last_orient=fk2_m,
                                             negate=self.component.negate,
                                             vis=False)

        m = matrix.set_matrix_translate(m, positions[-1])
        name = self.generate_name("RPRotTarget", "loc", "ctl")
        rp_rot_loc_target = matrix.transform(self.sc_space_grp, name, m, True)
        mc.aimConstraint(self.ik_jnts[-1],
                         rp_rot_loc_target,
                         offset=(0, 0, 0),
                         aimVector=(-1, 0, 0),
                         upVector=(0, 1, 0),
                         worldUpType="none",
                         skip=["x", "y"])
        self.rp_rot_default_rz = mc.getAttr(rp_rot_loc_target + ".rz")
        mc.delete(rp_rot_loc_target)

        name = self.generate_name("RPAutoRot", "loc", "ctl")
        self.rp_auto_rot_loc = matrix.transform(self.sc_space_grp, name, m, True)
        name = self.generate_name("RPRot", "loc", "ctl")
        self.rp_rot_loc = matrix.transform(self.rp_auto_rot_loc, name, m, False)
        name = self.generate_name("RP", "ikh", "jnt")
        self.ik_ikh = joint.ikh(self.rp_rot_loc, name, self.ik_jnts, pole_vector=self.pole_vec_obj)

        # refs
        self.refs = []
        for i, obj in enumerate((self.fk0_loc, self.fk1_loc, self.fk2_loc)):
            name = self.generate_name(str(i), "ref", "ctl")
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
                name = self.generate_name(str(i), "", "jnt")
                m = matrix.get_matrix(ref, world_space=True)
                parent = self.create_jnt(context=context,
                                         parent=parent,
                                         name=name,
                                         description=str(i),
                                         ref=ref,
                                         m=m,
                                         leaf=False,
                                         uni_scale=uni_scale)

    def attributes(self, context):
        super().attributes(context)

        self.auto_rot_attr = attribute.add_attr(self.ik_ctl,
                                                longName="auto_rot",
                                                type="double",
                                                minValue=0,
                                                maxValue=1,
                                                defaultValue=1,
                                                keyable=True)
        self.rot_attr = attribute.add_attr(self.ik_ctl,
                                           longName="rot",
                                           type="double",
                                           defaultValue=0,
                                           keyable=True)
        self.roll_attr = attribute.add_attr(self.ik_ctl,
                                            longName="roll",
                                            type="double",
                                            defaultValue=0,
                                            keyable=True)

    def operators(self, context):
        super().operators(context)
        data = self.component.data["value"]
        host = self.host

        mc.connectAttr(self.ik_sc_jnts[0] + ".matrix", self.sc_space_grp + ".offsetParentMatrix")
        mc.connectAttr(self.ik_sc_jnts[1] + ".matrix", self.rp_auto_rot_loc + ".offsetParentMatrix")
        mc.pointConstraint(self.ik_loc, self.rp_auto_rot_loc)
        if self.component.negate:
            md = mc.createNode("multiplyDivide")
            mc.setAttr(md + ".input1X", -1)
            mc.connectAttr(self.rp_auto_rot_loc + ".tx", md + ".input2X")
            mc.connectAttr(md + ".outputX", self.pole_vec_obj + ".tx")
        else:
            mc.connectAttr(self.rp_auto_rot_loc + ".tx", self.pole_vec_obj + ".tx")
        mc.aimConstraint(self.rp_auto_rot_loc,
                         self.ik_jnts[-1],
                         maintainOffset=True,
                         aimVector=(1, 0, 0),
                         upVector=(0, 1, 0),
                         worldUpType="objectrotation",
                         worldUpVector=(0, 1, 0),
                         worldUpObject=self.rp_auto_rot_loc)

        pma = mc.createNode("plusMinusAverage")
        mc.setAttr(pma + ".input1D[0]", mc.getAttr(self.ik_sc_jnts[-1] + ".tx"))
        mc.connectAttr(self.rp_auto_rot_loc + ".tx", pma + ".input1D[1]")

        md = mc.createNode("multiplyDivide")
        mc.setDrivenKeyframe(md + ".input1X",
                             currentDriver=pma + ".output1D",
                             driverValue=mc.getAttr(pma + ".output1D"),
                             value=0,
                             inTangentType="linear",
                             outTangentType="linear")
        mc.setDrivenKeyframe(md + ".input1X",
                             currentDriver=pma + ".output1D",
                             driverValue=self.distance0,
                             value=-90 - self.rp_rot_default_rz,
                             inTangentType="linear",
                             outTangentType="linear")
        mc.setDrivenKeyframe(md + ".input1X",
                             currentDriver=pma + ".output1D",
                             driverValue=self.distance0 + self.distance1 + self.distance2,
                             value=-1 * self.rp_rot_default_rz,
                             inTangentType="linear",
                             outTangentType="linear")
        mc.connectAttr(self.auto_rot_attr, md + ".input2X")
        mc.connectAttr(md + ".outputX", self.rp_auto_rot_loc + ".rz")

        mc.connectAttr(self.rot_attr, md + ".input1Y")
        mc.setAttr(md + ".input2Y", -1)
        mc.connectAttr(md + ".outputY", self.rp_rot_loc + ".rz")

        if not self.component.negate:
            md = mc.createNode("multiplyDivide")
            mc.setAttr(md + ".input1X", -1)
            mc.connectAttr(self.roll_attr, md + ".input2X")
            self.roll_attr = md + ".outputX"
        mc.connectAttr(self.roll_attr, self.sc_space_grp + ".rx")

        fk0_npo = hierarchy.get_parent(self.fk0_ctl)
        if mc.controller(fk0_npo, query=True):
            fk0_npo = hierarchy.get_parent(fk0_npo)
        fk1_npo = hierarchy.get_parent(self.fk1_ctl)
        if mc.controller(fk1_npo, query=True):
            fk1_npo = hierarchy.get_parent(fk1_npo)
        fk2_npo = hierarchy.get_parent(self.fk2_ctl)
        if mc.controller(fk2_npo, query=True):
            fk2_npo = hierarchy.get_parent(fk2_npo)
        mc.connectAttr(self.ik_jnts[0] + ".matrix", fk0_npo + ".offsetParentMatrix")
        mc.connectAttr(self.ik_jnts[1] + ".matrix", fk1_npo + ".offsetParentMatrix")
        mc.connectAttr(self.ik_jnts[2] + ".matrix", fk2_npo + ".offsetParentMatrix")

        # space switch
        if data["ik_space_switch_array"]:
            source_ctls = self.find_ctls(context, data["ik_space_switch_array"])
            operators.space_switch(source_ctls, self.ik_ctl, host, attr_name="ik_space_switch")
            script_node = callback.space_switch(source_ctls,
                                                self.ik_ctl,
                                                host,
                                                switch_attr_name="ik_space_switch")
            context["callbacks"].append(script_node)

    def connections(self, context):
        super().connections(context)

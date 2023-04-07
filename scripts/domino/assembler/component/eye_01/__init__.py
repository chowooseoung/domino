# domino
from domino.lib import matrix, vector
from domino.lib.rigging import nurbs, operators, callback
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
    name = "eye"
    side = "C"
    index = 0
    description = "눈 입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "mirror_behaviour": {"type": "bool"},
        "aim_space_switch_array": {"type": "string"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))
        m2 = matrix.set_matrix_translate(m, (0, 0, 3))
        m3 = matrix.set_matrix_translate(m, (0, 1, 0))
        return m1, m2, m3

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "mirror_behaviour": False,
    })
    return common_preset


def guide_recipe():
    return {
        "position": [
            (0, "aim"),
            (0, "up"),  # parent node index, extension
        ],
        "display_curve": [
            ((0, 1), "aimDpCrv"),  # source node indexes, extension
            ((0, 2), "upDpCrv"),  # source node indexes, extension
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

        positions = [om2.MVector(list(x)[12:-1]) for x in [m0, m1, m2]]
        normal = vector.get_plane_normal(*positions) * -1

        root = self.create_root(context)
        fk_color = self.generate_color("fk")
        ik_color = self.generate_color("ik")

        m = matrix.get_look_at_matrix(positions[0], positions[1], normal, "xy", False)

        length = vector.get_distance(positions[0], positions[1])

        aim_m = matrix.set_matrix_translate(m, positions[1])
        self.aim_ctl, self.aim_loc = self.create_ctl(context=context,
                                                     parent=None,
                                                     name=self.generate_name("aim", "", "ctl"),
                                                     parent_ctl=None,
                                                     attrs=["tx", "ty", "tz"],
                                                     m=aim_m,
                                                     cns=True,
                                                     mirror_config=(0, 1, 0, 0, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "circle3",
                                                         "width": length / 5,
                                                         "color": ik_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("aim", "", "ctl", True))

        name = self.generate_name("aim", "target", "ctl")
        self.aim_target = matrix.transform(root, name, m, True)

        name = self.generate_name("aim", "orient", "ctl")
        self.aim_orient = matrix.transform(root, name, m, True)

        negate = False
        if data["mirror_behaviour"] and self.component.negate:
            negate = True
        m = matrix.get_look_at_matrix(positions[0], positions[1], normal, "xz", negate)
        self.eye_ctl, self.eye_loc = self.create_ctl(context=context,
                                                     parent=self.aim_target,
                                                     name=self.generate_name("", "", "ctl"),
                                                     parent_ctl=self.aim_ctl,
                                                     attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz", "ro",
                                                            "sx", "sy", "sz"],
                                                     m=m,
                                                     cns=False,
                                                     mirror_config=(0, 1, 1, 1, 0, 0, 0, 0, 0),
                                                     shape_args={
                                                         "shape": "circle3",
                                                         "width": length / 3,
                                                         "color": fk_color
                                                     },
                                                     mirror_ctl_name=self.generate_name("", "", "ctl", True))

        m = matrix.get_look_at_matrix(positions[0], positions[1], normal, "xz", self.component.negate)
        name = self.generate_name("ref", "source", "ctl")
        self.ref_source = matrix.transform(self.eye_loc, name, m)

        name = self.generate_name("display", "crv", "ctl")
        display_crv = nurbs.create(parent=root,
                                   name=name,
                                   degree=1,
                                   positions=[(0, 0, 0), (0, 0, 0)],
                                   vis=True,
                                   inherits=False,
                                   display_type=2)
        nurbs.constraint(display_crv, [self.aim_loc, self.ref_source])

        # refs
        name = self.generate_name("", "ref", "ctl")
        ref = self.create_ref(context=context, name=name, anchor=True, m=self.ref_source)

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True
            jnt = self.create_jnt(context=context,
                                  parent=None,
                                  name=self.generate_name("", "", "jnt"),
                                  description="0",
                                  ref=ref,
                                  m=mc.xform(ref, query=True, matrix=True, worldSpace=True),
                                  leaf=False,
                                  uni_scale=uni_scale)

    def attributes(self, context):
        super().attributes(context)

    def operators(self, context):
        super().operators(context)

        data = self.component.data["value"]
        host = self.host

        mc.aimConstraint(self.aim_loc,
                         self.aim_target,
                         aimVector=(1, 0, 0),
                         upVector=(0, 1, 0),
                         worldUpType="objectrotation",
                         worldUpObject=self.aim_orient)

        if data["aim_space_switch_array"]:
            source_ctls = self.find_ctls(context, data["aim_space_switch_array"])
            operators.space_switch(source_ctls, self.aim_ctl, host, attr_name="aim_space_switch")
            script_node = callback.space_switch(source_ctls,
                                                self.aim_ctl,
                                                host,
                                                switch_attr_name="aim_space_switch")
            context["callbacks"].append(script_node)

    def connections(self, context):
        super().connections(context)

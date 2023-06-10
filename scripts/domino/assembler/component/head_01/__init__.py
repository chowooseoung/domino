# domino
from domino.lib import matrix, vector
from domino.lib.rigging import operators, callback
from domino import assembler

# built-ins
import os
import uuid

# maya
from maya.api import OpenMaya as om2


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "head"
    side = "C"
    index = 0
    description = "머리 입니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "aim_space_switch_array": {"type": "string"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))
        m2 = matrix.set_matrix_translate(m, (0, 2, 0))
        m3 = matrix.set_matrix_translate(m, (0, 0, 0.2))
        return m1, m2, m3

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
    })
    return common_preset


def guide_recipe():
    return {
        "position": [
            (0, "tip"),
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

        root = self.create_root(context)
        fk_color = self.generate_color("fk")

        root_pos = om2.MVector(list(m0)[12:-1])
        up_pos = om2.MVector(list(m1)[12:-1])
        aim_pos = om2.MVector(list(m2)[12:-1])

        normal = up_pos - root_pos
        distance = vector.get_distance(root_pos, up_pos)
        m = matrix.get_look_at_matrix(root_pos, aim_pos, normal, "-yx", self.component.negate)
        self.ctl, self.loc = self.create_ctl(context=context,
                                             parent=None,
                                             name=self.generate_name("", "", "ctl"),
                                             parent_ctl=None,
                                             attrs=["tx", "ty", "tz",
                                                    "rx", "ry", "rz",
                                                    "sx", "sy", "sz"],
                                             m=m,
                                             cns=False,
                                             mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                             shape_args={
                                                 "shape": "cube",
                                                 "width": distance,
                                                 "height": 1,
                                                 "depth": 1,
                                                 "po": (distance / 3.0, 0, 0),
                                                 "color": fk_color
                                             },
                                             mirror_ctl_name=self.generate_name("", "", "ctl", True))

        # refs
        self.ref = self.create_ref(context=context,
                                   name=self.generate_name("", "ref", "ctl"),
                                   anchor=True,
                                   m=self.loc)

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True

            self.jnt = self.create_jnt(context=context,
                                       parent=None,
                                       name=self.generate_name("", "", "jnt"),
                                       description="",
                                       ref=self.ref,
                                       m=m,
                                       leaf=False,
                                       uni_scale=uni_scale)

    def attributes(self, context):
        super().attributes(context)

    def operators(self, context):
        super().operators(context)

        data = self.component.data["value"]
        host = self.host

        if data["aim_space_switch_array"]:
            source_ctls = self.find_ctls(context, data["aim_space_switch_array"])
            m = matrix.get_matrix(self.ctl)
            up_object = matrix.transform(self.root, self.generate_name("upVec", "", "ctl"), m)
            self.ik_ctl_cons = operators.space_switch(source_ctls, self.ctl, host, attr_name="aim_space_switch",
                                                      constraint="aim", aimVector=(0, -1, 0), upVector=(1, 0, 0),
                                                      worldUpType="object", worldUpObject=up_object)
            self.ik_ctl_script_node = callback.space_switch(source_ctls,
                                                            self.ctl,
                                                            host,
                                                            switch_attr_name="aim_space_switch")
            context["callbacks"].append(self.ik_ctl_script_node)

    def connections(self, context):
        super().connections(context)

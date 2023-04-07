# domino
from domino.lib import matrix, vector
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
    name = "clavicle"
    side = "C"
    index = 0
    description = "사람의 빗장뼈 입니다. arm_2jnt_01는 clavicle_01과 연결될 수 있습니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset": {"type": "doubleAngle"},
        "offset_matrix": {"type": "matrix"},
    })

    def _anchors():
        m = om2.MMatrix()
        m1 = matrix.set_matrix_translate(m, (0, 0, 0))
        m2 = matrix.set_matrix_translate(m, (2, 0, 0))
        m3 = matrix.set_matrix_translate(m, (3, 0, 0))
        return m1, m2, m3

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(x) for x in _anchors()],
        "offset": 0,
        "offset_matrix": list(om2.MMatrix()),
    })
    return common_preset


def guide_recipe():
    return {
        "position": [
            (0, "aim"),
            (1, "orbit"),  # parent node index, extension
        ],
        "orientation": (1, "ori"),  # target node index, extension
        "display_curve": [
            ((0, 1), "aimDpCrv"),  # source node indexes, extension
            ((0, 2), "orbitDpCrv")  # source node indexes, extension
        ],
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        fk_color = self.generate_color("fk")

        orient_xyz = vector.OrientXYZ(data["offset_matrix"])
        normal = orient_xyz.z

        start_pos, look_at_pos = [om2.MVector(x[12:-1]) for x in data["anchors"][:-1]]
        orbit_pos = om2.MVector(data["anchors"][-1][12:-1])

        root = self.create_root(context)

        look_at_m = matrix.get_look_at_matrix(start_pos, look_at_pos, normal, "xz", self.component.negate)
        orbit_m = matrix.set_matrix_translate(look_at_m, orbit_pos)

        distance = vector.get_distance(start_pos, orbit_pos)
        offset = distance / -2 if self.component.negate else distance / 2
        self.clavicle_ctl, self.clavicle_loc = self.create_ctl(context=context,
                                                               parent=None,
                                                               name=self.generate_name("", "", "ctl"),
                                                               parent_ctl=None,
                                                               attrs=["tx", "ty", "tz",
                                                                      "rx", "ry", "rz", "ro",
                                                                      "sx", "sy", "sz"],
                                                               m=look_at_m,
                                                               cns=False,
                                                               mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                               shape_args={
                                                                   "shape": "cube",
                                                                   "color": fk_color,
                                                                   "width": distance,
                                                                   "height": distance / 3,
                                                                   "depth": distance / 3,
                                                                   "po": (offset, 0, 0)
                                                               },
                                                               mirror_ctl_name=self.generate_name("", "", "ctl", True))
        name = self.generate_name("", "ref", "ctl")
        self.clavicle_ref = self.create_ref(context=context, name=name, anchor=False, m=self.clavicle_loc)

        self.orbit_ctl, self.orbit_loc = self.create_ctl(context=context,
                                                         parent=self.clavicle_loc,
                                                         name=self.generate_name("orbit", "", "ctl"),
                                                         parent_ctl=self.clavicle_ctl,
                                                         attrs=["tx", "ty", "tz",
                                                                "rx", "ry", "rz",
                                                                "sx", "sy", "sz"],
                                                         m=orbit_m,
                                                         cns=False,
                                                         mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                         shape_args={
                                                             "shape": "circle3",
                                                             "color": fk_color,
                                                             "width": distance / 2
                                                         },
                                                         mirror_ctl_name=self.generate_name("orbit", "", "ctl", True))
        name = self.generate_name("orbit", "ref", "ctl")
        self.orbit_ref = self.create_ref(context=context, name=name, anchor=True, m=self.orbit_loc)

        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True
            self.clavicle_jnt = self.create_jnt(context=context,
                                                parent=None,
                                                name=self.generate_name("", "", "jnt"),
                                                description="",
                                                ref=self.clavicle_ref,
                                                m=look_at_m,
                                                leaf=False,
                                                uni_scale=uni_scale)

    def attributes(self, context):
        super().attributes(context)

    def operators(self, context):
        super().operators(context)

    def connections(self, context):
        super().connections(context)

        host = self.host
        if "auto_clavicle" not in context:
            context["auto_clavicle"] = {}
        context["auto_clavicle"][self.identifier] = [self.clavicle_ctl, self.root, host]

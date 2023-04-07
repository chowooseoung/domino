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
    name = "chain"
    side = "C"
    index = 0
    description = "fk chain."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset": {"type": "doubleAngle"},
        "offset_matrix": {"type": "matrix"},
        "guide_orientation": {"type": "bool"},
    })

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [om2.MMatrix()],
        "offset": 0,
        "offset_matrix": list(om2.MMatrix()),
        "guide_orientation": False,
    })
    return common_preset


def guide_recipe():
    return {
        "position": [],
        "orientation": (1, "ori"),  # target node index, extension
        "flexible_position": (1, "pos%s", (1, 0, 0))  # anchor min value, extension
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        negate = self.component.negate

        fk_color = self.generate_color("fk")

        orient_xyz = vector.OrientXYZ(data["offset_matrix"])
        normal = orient_xyz.z

        root = self.create_root(context)

        matrices = [om2.MMatrix(x) for x in data["anchors"]]
        positions = [om2.MVector(list(m)[12:-1]) for m in matrices]
        if not data["guide_orientation"]:
            matrices = matrix.get_chain_matrix(positions, normal, negate)
            matrices.append(matrix.set_matrix_translate(matrices[-1], positions[-1]))

        total_length = 0
        div_length = 0
        for i, p in enumerate(positions):
            if i == len(positions) - 1:
                break
            l = vector.get_distance(p, positions[i + 1])
            total_length += l
            if i == 0:
                div_length += l

        self.ctls = []
        self.locs = []
        loc = root
        ctl = None
        for i, m in enumerate(matrices):
            index = i - 1 if i == len(matrices) - 1 else i + 1
            distance = vector.get_distance(positions[i], positions[index])
            ctl, loc = self.create_ctl(context=context,
                                       parent=loc,
                                       name=self.generate_name(str(i), "", "ctl"),
                                       parent_ctl=ctl,
                                       attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                       m=m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "color": fk_color,
                                           "width": distance,
                                           "height": distance * div_length / total_length * 2,
                                           "depth": distance * div_length / total_length * 2,
                                           "po": (distance / -2 if negate else distance / 2, 0, 0)
                                       },
                                       mirror_ctl_name=self.generate_name(str(i), "", "ctl", True))
            self.ctls.append(ctl)
            self.locs.append(loc)

        # refs
        self.refs = []
        for i, loc in enumerate(self.locs):
            name = self.generate_name(str(i), "ref", "ctl")
            ref = self.create_ref(context=context, name=name, anchor=True, m=loc)
            self.refs.append(ref)

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True
            self.jnts = []
            jnt = None
            for i, ref in enumerate(self.refs):
                name = self.generate_name(str(i), "", "jnt")
                jnt = self.create_jnt(context=context,
                                      parent=jnt,
                                      name=name,
                                      description=str(i),
                                      ref=ref,
                                      m=matrices[i],
                                      leaf=False,
                                      uni_scale=uni_scale)
                self.jnts.append(jnt)

    def attributes(self, context):
        super().attributes(context)

    def operators(self, context):
        super().operators(context)

    def connections(self, context):
        super().connections(context)

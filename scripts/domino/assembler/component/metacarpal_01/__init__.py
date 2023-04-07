# built-ins
import os
import uuid

# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# domino
from domino.lib import matrix, vector, hierarchy
from domino import assembler


class Author:
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    component = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "metacarpal"
    side = "C"
    index = 0
    description = "손바닥뼈입니다. 원하는 관절의 수를 지정할 수 있습니다."


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset": {"type": "doubleAngle"},
        "offset_matrix": {"type": "matrix"}
    })

    common_preset["value"].update({
        "component": Author.component,
        "component_id": str(uuid.uuid4()),
        "component_version": ". ".join([str(x) for x in Author.version]),
        "name": Author.name,
        "side": Author.side,
        "index": Author.index,
        "anchors": [list(om2.MMatrix())],
        "offset": 0,
        "offset_matrix": list(om2.MMatrix())
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

        ik_color = self.generate_color("ik")
        fk_color = self.generate_color("fk")

        orient_xyz = vector.OrientXYZ(data["offset_matrix"])
        normal = orient_xyz.z

        root = self.create_root(context)

        negate = self.component.negate

        matrices = [om2.MMatrix(x) for x in data["anchors"]]
        positions = [om2.MVector(list(m)[12:-1]) for m in matrices]
        matrices = matrix.get_chain_matrix(positions, normal, negate)
        matrices.append(matrix.set_matrix_translate(matrices[-1], positions[-1]))

        distance = vector.get_distance(positions[0], positions[1])
        self.main_ctl, self.main_loc = self.create_ctl(context=context,
                                                       parent=root,
                                                       name=self.generate_name("main", "", "ctl"),
                                                       parent_ctl=None,
                                                       attrs=["tx", "ty", "tz",
                                                              "rx", "ry", "rz",
                                                              "sx", "sy", "sz"],
                                                       m=matrices[0],
                                                       cns=False,
                                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                       shape_args={
                                                           "shape": "circle3",
                                                           "width": distance * 2,
                                                           "color": ik_color
                                                       },
                                                       mirror_ctl_name=self.generate_name("main", "", "ctl", True))

        self.ctls = []
        self.locs = []
        ctl = self.main_ctl
        for i, m in enumerate(matrices):
            index = i - 1 if i == len(matrices) - 1 else i + 1
            distance = vector.get_distance(positions[i], positions[index])
            ctl, loc = self.create_ctl(context=context,
                                       parent=root,
                                       name=self.generate_name(str(i), "", "ctl"),
                                       parent_ctl=ctl,
                                       attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                       m=m,
                                       cns=False,
                                       mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                       shape_args={
                                           "shape": "cube",
                                           "width": distance,
                                           "height": distance,
                                           "depth": distance,
                                           "color": fk_color
                                       },
                                       mirror_ctl_name=self.generate_name(str(i), "", "ctl", True))
            self.ctls.append(ctl)
            self.locs.append(loc)

        ratio = 1.0 / len(self.ctls)
        value = 0
        for i, ctl in enumerate(self.ctls):
            npo = hierarchy.get_parent(ctl)
            blend_m = mc.createNode("blendMatrix")
            mc.setAttr(blend_m + ".envelope", value)
            mc.connectAttr(self.main_ctl + ".matrix", blend_m + ".target[0].targetMatrix")
            decom_m = mc.createNode("decomposeMatrix")
            mc.connectAttr(blend_m + ".outputMatrix", decom_m + ".inputMatrix")
            mc.connectAttr(decom_m + ".outputTranslate", npo + ".t")
            mc.connectAttr(decom_m + ".outputRotate", npo + ".r")
            mc.connectAttr(decom_m + ".outputScale", npo + ".s")

            value += ratio

        # refs
        self.refs = []
        for i, loc in enumerate(self.locs):
            ref = self.create_ref(context=context,
                                  name=self.generate_name(str(i), "ref", "ctl"),
                                  anchor=True,
                                  m=loc)
            self.refs.append(ref)

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True
            self.jnts = []
            jnt = None
            for i, ref in enumerate(self.refs):
                jnt = self.create_jnt(context=context,
                                      parent=jnt,
                                      name=self.generate_name(str(i), "", "jnt"),
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

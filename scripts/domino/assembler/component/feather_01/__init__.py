# domino
from domino.lib import matrix, vector, hierarchy
from domino.lib.rigging import nurbs, joint
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
    name = "feather"
    side = "C"
    index = 0
    description = ("새의 날개 깃털입니다. wing_01 과 연결될수있습니다. "
                   "wing output mesh 에 proximity Pin 되어있는 간단한 splineIk 입니다."
                   "깃털 길이를 유지하기 위해 splineIk가 사용되었습니다.")


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "primary": {"type": "bool"},
        "primary_coverts": {"type": "bool"},
        "primary_under": {"type": "bool"},
        "secondary": {"type": "bool"},
        "secondary_coverts": {"type": "bool"},
        "secondary_under": {"type": "bool"},
        "tertiary": {"type": "bool"},
        "offset": {"type": "doubleAngle"},
        "offset_matrix": {"type": "matrix"},
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
        "offset_matrix": list(om2.MMatrix()),
    })
    return common_preset


def guide_recipe():
    return {
        "position": [],
        "orientation": (1, "ori"),  # target node index, extension
        "flexible_position": (1, "pos%s", (0, 0, -1))  # anchor min value, extension
    }


class Rig(assembler.Rig):

    def objects(self, context):
        super().objects(context)

        data = self.component.data["value"]
        assembly_data = self.component.get_parent(generations=-1).data["value"]

        negate = self.component.negate

        fk_color = self.generate_color("fk")
        ik_color = self.generate_color("ik")

        orient_xyz = vector.OrientXYZ(data["offset_matrix"])
        normal = orient_xyz.z

        root = self.create_root(context)

        matrices = [om2.MMatrix(x) for x in data["anchors"]]
        positions = [om2.MVector(list(m)[12:-1]) for m in matrices]
        matrices = matrix.get_chain_matrix(positions, normal, negate)

        total_length = 0
        div_length = 0
        for i, p in enumerate(positions):
            if i == len(positions) - 1:
                break
            l = vector.get_distance(p, positions[i + 1])
            total_length += l
            if i == 0:
                div_length += l

        self.fk_ctls = []
        self.fk_locs = []
        self.ik_ctls = []
        self.ik_locs = []
        fk_loc = root
        fk_ctl = None
        self.ik_jnts = []
        parent_jnt = root
        for i, p in enumerate(positions[:-1]):
            distance = vector.get_distance(positions[i], positions[i + 1])
            fk_ctl, fk_loc = self.create_ctl(context=context,
                                             parent=fk_loc,
                                             name=self.generate_name("fk" + str(i), "", "ctl"),
                                             parent_ctl=fk_ctl,
                                             attrs=["tx", "ty", "tz", "rx", "ry", "rz"],
                                             m=matrices[i],
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
                                             mirror_ctl_name=self.generate_name("fk" + str(i), "", "ctl", True))
            self.fk_ctls.append(fk_ctl)
            self.fk_locs.append(fk_loc)
            ik_ctl, ik_loc = self.create_ctl(context=context,
                                             parent=fk_loc,
                                             name=self.generate_name("ik" + str(i), "", "ctl"),
                                             parent_ctl=fk_ctl,
                                             attrs=["tx", "ty", "tz"],
                                             m=matrices[i],
                                             cns=False,
                                             mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                             shape_args={
                                                 "shape": "square",
                                                 "color": ik_color,
                                                 "width": distance * div_length / total_length * 3,
                                                 "height": distance * div_length / total_length * 3,
                                                 "up": "x"
                                             },
                                             mirror_ctl_name=self.generate_name("ik" + str(i), "", "ctl", True))
            self.ik_ctls.append(ik_ctl)
            self.ik_locs.append(ik_loc)

            parent_jnt = joint.add_joint(parent=parent_jnt,
                                         name=self.generate_name("ik" + str(i), "jnt", "ctl"),
                                         m=matrices[i],
                                         vis=False)
            self.ik_jnts.append(parent_jnt)

            if i == len(positions) - 2:
                m = matrix.set_matrix_translate(matrices[i], positions[-1])
                ik_ctl, ik_loc = self.create_ctl(context=context,
                                                 parent=fk_loc,
                                                 name=self.generate_name("ik" + str(i + 1), "", "ctl"),
                                                 parent_ctl=fk_ctl,
                                                 attrs=["tx", "ty", "tz"],
                                                 m=m,
                                                 cns=False,
                                                 mirror_config=(1, 1, 1, 0, 0, 0, 0, 0, 0),
                                                 shape_args={
                                                     "shape": "square",
                                                     "color": ik_color,
                                                     "width": distance * div_length / total_length * 3,
                                                     "height": distance * div_length / total_length * 3,
                                                     "up": "x"
                                                 },
                                                 mirror_ctl_name=self.generate_name("ik" + str(i + 1), "", "ctl", True))
                parent_jnt = joint.add_joint(parent=parent_jnt,
                                             name=self.generate_name("ik" + str(i + 1), "jnt", "ctl"),
                                             m=m,
                                             vis=False)
                self.ik_jnts.append(parent_jnt)
                self.ik_ctls.append(ik_ctl)
                self.ik_locs.append(ik_loc)
                matrices.append(m)

        self.crv = nurbs.create(parent=root,
                                name=self.generate_name("ik", "crv", "ctl"),
                                degree=1,
                                positions=((0, 0, 0) for _ in range(len(positions))),
                                inherits=False,
                                display_type=2)
        nurbs.constraint(self.crv, self.ik_locs)

        ikh = joint.sp_ikh(parent=root,
                           name=self.generate_name("SP", "ikh", "ctl"),
                           chain=self.ik_jnts,
                           curve=self.crv)
        mc.setAttr(ikh + ".dTwistControlEnable", 1)
        mc.setAttr(ikh + ".dWorldUpType", 4)
        mc.connectAttr(self.fk_locs[0] + ".worldMatrix[0]", ikh + ".dWorldUpMatrix")
        mc.connectAttr(self.fk_locs[-1] + ".worldMatrix[0]", ikh + ".dWorldUpMatrixEnd")

        # refs
        self.refs = []
        for i, ik_jnt in enumerate(self.ik_jnts):
            name = self.generate_name(str(i), "ref", "ctl")
            ref = self.create_ref(context=context, name=name, anchor=True, m=ik_jnt)
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

        data = self.component.data["value"]
        parent_data = self.parent.component.data["value"]
        parent_context = context[self.parent.identifier]

        # ---  wing_01 connector --- #
        mesh_index = None
        if parent_data["component"] == "wing_01":
            # connect proximity pin
            if data["primary"]:
                mesh_index = 0
            elif data["primary_coverts"]:
                mesh_index = 1
            elif data["primary_under"]:
                mesh_index = 2
            elif data["secondary"]:
                mesh_index = 3
            elif data["secondary_coverts"]:
                mesh_index = 4
            elif data["secondary_under"]:
                mesh_index = 5
            elif data["tertiary"]:
                mesh_index = 6

            if mesh_index is None:
                return

            # get pin node, last index
            pin, index = parent_context["proximity_pin"][mesh_index]
            orig_m = om2.MMatrix()
            parent = self.root
            for i, ctl in enumerate(self.fk_ctls):
                m = matrix.get_matrix(ctl)

                mult_m = mc.createNode("multMatrix")
                mc.connectAttr(pin + ".outputMatrix[{0}]".format(index), mult_m + ".matrixIn[0]")
                mc.connectAttr(parent + ".worldInverseMatrix[0]", mult_m + ".matrixIn[1]")

                decom_m = mc.createNode("decomposeMatrix")
                mc.connectAttr(mult_m + ".matrixSum", decom_m + ".inputMatrix")

                mc.setAttr(pin + ".inputMatrix[{0}]".format(index), m, type="matrix")

                parent = matrix.transform(parent=parent,
                                          name=self.generate_name("fk" + str(i), "source", "ctl"),
                                          m=orig_m)
                npo = hierarchy.get_parent(ctl)
                mc.setAttr(npo + ".offsetParentMatrix", orig_m, type="matrix")
                mc.connectAttr(decom_m + ".outputTranslate", parent + ".t")
                mc.connectAttr(decom_m + ".outputRotate", parent + ".r")
                mc.connectAttr(decom_m + ".outputTranslate", npo + ".t")
                mc.connectAttr(decom_m + ".outputRotate", npo + ".r")
                index += 1
            parent_context["proximity_pin"][mesh_index][1] = index
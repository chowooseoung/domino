# domino
from domino.lib import matrix, vector, attribute, hierarchy
from domino.lib.rigging import joint, nurbs
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
    name = "chain"
    side = "C"
    index = 0
    description = ""


def component_preset():
    common_preset = assembler.common_component_preset()
    common_preset["attributes"].update({
        "offset": {"type": "doubleAngle"},
        "offset_matrix": {"type": "matrix"},
        "guide_orientation": {"type": "bool"},
        "degree": {"type": "enum", "enumName": "1:3"},
        "master_a": {"type": "string"},
        "master_b": {"type": "string"},
        "blend": {"type": "double"},
        "division": {"type": "long", "minValue": 2}
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
        "guide_orientation": False,
        "degree": 3,
        "division": 4
    })
    return common_preset


def guide_recipe():
    return {
        "position": [],
        "orientation": (1, "ori"),  # target node index, extension
        "flexible_position": (1, "pos%s", (1, 0, 0)),  # anchor min value, extension, direction vector
        "display_curve": [
            ((), "dpCrv", 3, 2)
        ]  # source node indexes, extension, degree, thickness
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
        if not data["guide_orientation"]:
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
                self.ik_ctls.append(ik_ctl)
                self.ik_locs.append(ik_loc)
                if not data["guide_orientation"]:
                    matrices.append(m)

        self.crv = nurbs.create(parent=root,
                                name=self.generate_name("ik", "crv", "ctl"),
                                degree=int(data["degree"]),
                                positions=((0, 0, 0) for _ in range(len(positions))),
                                inherits=False,
                                display_type=2)
        nurbs.constraint(self.crv, self.ik_locs)
        length = mc.arclen(self.crv)

        self.ik_jnts = []
        div_length = length / data["division"]
        parent = root
        orig_m = om2.MMatrix()
        for i in range(data["division"] + 1):
            m = om2.MTransformationMatrix(orig_m)
            m = m.setTranslation(om2.MVector(div_length * i, 0, 0), om2.MSpace.kWorld).asMatrix()
            parent = joint.add_joint(parent=parent,
                                     name=self.generate_name("ik" + str(i), "jnt", "ctl"),
                                     m=m,
                                     vis=False)
            self.ik_jnts.append(parent)

        ikh = joint.sp_ikh(parent=root,
                           name=self.generate_name("SP", "ikh", "ctl"),
                           chain=self.ik_jnts,
                           curve=self.crv)
        mc.setAttr(ikh + ".dTwistControlEnable", 1)
        mc.setAttr(ikh + ".dWorldUpType", 4)
        mc.connectAttr(self.fk_locs[0] + ".worldMatrix[0]", ikh + ".dWorldUpMatrix")
        mc.connectAttr(self.fk_locs[-1] + ".worldMatrix[0]", ikh + ".dWorldUpMatrixEnd")
        for j in self.ik_jnts:
            mc.setAttr(j + ".jointOrient", *mc.getAttr(j + ".r")[0])

        context[self.identifier]["fk_ctls"] = self.fk_ctls
        context[self.identifier]["ik_ctls"] = self.ik_ctls

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
                                      m=matrix.get_matrix(ref),
                                      leaf=False,
                                      uni_scale=uni_scale)
                self.jnts.append(jnt)

    def attributes(self, context):
        super().attributes(context)

        host = self.host
        data = self.component.data["value"]

        if data["master_a"] or data["master_a"]:
            self.blend_attr = attribute.add_attr(host,
                                                 longName="blend",
                                                 type="float",
                                                 keyable=True,
                                                 minValue=0,
                                                 maxValue=1,
                                                 defaultValue=data["blend"])

    def operators(self, context):
        super().operators(context)

        data = self.component.data["value"]
        master_a_comp = self.find_component(data["master_a"])
        if master_a_comp:
            master_a_identifier = "_".join([str(x) for x in master_a_comp.identifier])
        master_b_comp = self.find_component(data["master_b"])
        if master_b_comp:
            master_b_identifier = "_".join([str(x) for x in master_b_comp.identifier])

        if not master_a_comp or not master_b_comp:
            return

        master_a_fk_ctls = context[master_a_identifier]["fk_ctls"]
        master_a_ik_ctls = context[master_a_identifier]["ik_ctls"]

        master_b_fk_ctls = context[master_b_identifier]["fk_ctls"]
        master_b_ik_ctls = context[master_b_identifier]["ik_ctls"]

        for i in range(max(len(master_a_fk_ctls), len(master_b_fk_ctls))):
            if i >= len(self.fk_ctls):
                break
            if i >= len(master_a_fk_ctls):
                master_a_fk_ctl = None
            else:
                master_a_fk_ctl = master_a_fk_ctls[i]
            if i >= len(master_b_fk_ctls):
                master_b_fk_ctl = None
            else:
                master_b_fk_ctl = master_b_fk_ctls[i]

            pb = mc.createNode("pairBlend")
            mc.setAttr(pb + ".rotInterpolation", 1)
            mc.connectAttr(self.blend_attr, pb + ".weight")
            if master_a_fk_ctl:
                mc.connectAttr(master_a_fk_ctl + ".t", pb + ".inTranslate1")
                mc.connectAttr(master_a_fk_ctl + ".r", pb + ".inRotate1")
            if master_b_fk_ctl:
                mc.connectAttr(master_b_fk_ctl + ".t", pb + ".inTranslate2")
                mc.connectAttr(master_b_fk_ctl + ".r", pb + ".inRotate2")
            npo = hierarchy.get_parent(self.fk_ctls[i])
            mc.connectAttr(pb + ".outTranslate", npo + ".t")
            mc.connectAttr(pb + ".outRotate", npo + ".r")

        for i in range(max(len(master_a_ik_ctls), len(master_b_ik_ctls))):
            if i >= len(self.ik_ctls):
                break
            if i >= len(master_a_ik_ctls):
                master_a_ik_ctl = None
            else:
                master_a_ik_ctl = master_a_ik_ctls[i]
            if i >= len(master_b_ik_ctls):
                master_b_ik_ctl = None
            else:
                master_b_ik_ctl = master_b_ik_ctls[i]

            pb = mc.createNode("pairBlend")
            mc.setAttr(pb + ".rotInterpolation", 1)
            mc.connectAttr(self.blend_attr, pb + ".weight")
            if master_a_ik_ctl:
                mc.connectAttr(master_a_ik_ctl + ".t", pb + ".inTranslate1")
                mc.connectAttr(master_a_ik_ctl + ".r", pb + ".inRotate1")
            if master_b_ik_ctl:
                mc.connectAttr(master_b_ik_ctl + ".t", pb + ".inTranslate2")
                mc.connectAttr(master_b_ik_ctl + ".r", pb + ".inRotate2")
            npo = hierarchy.get_parent(self.ik_ctls[i])
            mc.connectAttr(pb + ".outTranslate", npo + ".t")
            mc.connectAttr(pb + ".outRotate", npo + ".r")

    def connections(self, context):
        super().connections(context)

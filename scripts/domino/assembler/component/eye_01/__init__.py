# domino
from domino.lib import matrix, vector, polygon, attribute, hierarchy
from domino.lib.rigging import nurbs, operators, callback
from domino import assembler

# built-ins
import os
import uuid
import math

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
        "spherical_iris_pupil_rig": {"type": "bool"},
        "eyeball_mesh": {"type": "string"},
        "center_edge_index": {"type": "string"},
        "limbus_edge_index": {"type": "string"},
        "pupil_edge_index": {"type": "string"},
        "last_edge_index": {"type": "string"}
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
        "spherical_iris_pupil_rig": False
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
                                                            "rx", "ry", "rz",
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
        context[self.identifier]["line_of_sight"] = hierarchy.get_parent(self.eye_ctl)

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
        self.refs = [self.create_ref(context=context, name=name, anchor=True, m=self.ref_source)]
        self.names = [""]

        if data["spherical_iris_pupil_rig"]:
            mesh = data["eyeball_mesh"]
            center_edge_index = int(data["center_edge_index"])
            limbus_edge_index = int(data["limbus_edge_index"])
            pupil_edge_index = int(data["pupil_edge_index"])
            last_edge_index = int(data["last_edge_index"])

            center_edge_loop = mc.polySelect(mesh, query=True, edgeLoop=center_edge_index)[:-1]
            center_edge_to_vertices = polygon.convert_component(
                [mesh + ".vtx[" + str(x) + "]" for x in center_edge_loop], vertex=True)
            center_average_vector = vector.get_average_position(center_edge_to_vertices)

            self.radius = vector.get_distance(center_average_vector, vector.get_position(center_edge_to_vertices[0]))

            edge_ring_path = mc.polySelect(mesh, query=True, edgeRingPath=(center_edge_index, last_edge_index))[1:]
            self.locs = []
            n = 0
            name_format = "sclera{0}"
            for i, edge in enumerate(edge_ring_path):
                if edge == limbus_edge_index:
                    n = 0
                    name_format = "iris{0}"
                    self.limbus_edge_index = i
                elif edge == pupil_edge_index:
                    n = 0
                    name_format = "pupil{0}"
                    self.pupil_edge_index = i
                name = name_format.format(n)
                edge_loop = [mesh + ".vtx[" + str(x) + "]" for x in mc.polySelect(mesh, query=True, edgeLoop=edge)[:-1]]
                average_vector = vector.get_average_position(polygon.convert_component(edge_loop, vertex=True))
                distance = vector.get_distance(average_vector, center_average_vector)

                loc = matrix.transform(parent=self.ref_source,
                                       name=self.generate_name(name, "loc", "ctl"),
                                       m=m)
                mc.setAttr(loc + ".tx", distance)
                self.locs.append(loc)
                n += 1
                self.names.append(name)

            for i, loc in enumerate(self.locs):
                name = self.generate_name(self.names[i + 1], "ref", "ctl")
                self.refs.append(self.create_ref(context=context, name=name, anchor=True, m=loc))

        # jnts
        if data["create_jnt"]:
            uni_scale = False
            if assembly_data["force_uni_scale"]:
                uni_scale = True
            parent = None
            self.jnts = []
            for i, ref in enumerate(self.refs):
                jnt = self.create_jnt(context=context,
                                      parent=parent,
                                      name=self.generate_name(self.names[i], "", "jnt"),
                                      description=name,
                                      ref=ref,
                                      m=mc.xform(ref, query=True, matrix=True, worldSpace=True),
                                      leaf=False,
                                      uni_scale=uni_scale)
                if i == 0:
                    parent = jnt
                self.jnts.append(jnt)

    def attributes(self, context):
        super().attributes(context)
        host = self.host

        data = self.component.data["value"]
        if data["spherical_iris_pupil_rig"]:
            limbus_length = mc.getAttr(self.locs[self.limbus_edge_index] + ".tx") / self.radius
            limbus_dv = math.degrees(math.asin(limbus_length) * 2) / 180
            self.limbus_line_attr = attribute.add_attr(host,
                                                       longName="limbus_line",
                                                       type="float",
                                                       minValue=0,
                                                       maxValue=1,
                                                       defaultValue=limbus_dv,
                                                       keyable=True)
            pupil_length = mc.getAttr(self.locs[self.pupil_edge_index] + ".tx") / self.radius
            pupil_dv = math.degrees(math.asin(pupil_length) * 2) / 180
            self.pupil_line_attr = attribute.add_attr(host,
                                                      longName="pupil_line",
                                                      type="float",
                                                      minValue=0,
                                                      maxValue=1,
                                                      defaultValue=pupil_dv,
                                                      keyable=True)
            last_length = mc.getAttr(self.locs[-1] + ".tx") / self.radius
            last_dv = math.degrees(math.asin(last_length) * 2) / 180
            self.end_line_attr = attribute.add_attr(host,
                                                    longName="end_line",
                                                    type="float",
                                                    minValue=0,
                                                    maxValue=1,
                                                    defaultValue=last_dv,
                                                    keyable=False)

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

        if data["spherical_iris_pupil_rig"]:
            # setup limbus, pupil, last
            for attr, i in zip([self.limbus_line_attr, self.pupil_line_attr, self.end_line_attr],
                               [self.limbus_edge_index, self.pupil_edge_index, -1]):
                mp_180 = mc.createNode("multiplyDivide")
                mc.connectAttr(attr, mp_180 + ".input1X")
                mc.setAttr(mp_180 + ".input2X", 180)

                euler_to_quat = mc.createNode("eulerToQuat")
                mc.connectAttr(mp_180 + ".outputX", euler_to_quat + ".inputRotateX")

                radius_mp = mc.createNode("multiplyDivide")
                mc.connectAttr(euler_to_quat + ".outputQuatX", radius_mp + ".input1X")
                mc.setAttr(radius_mp + ".input2X", self.radius)

                mc.connectAttr(radius_mp + ".outputX", self.locs[i] + ".tx")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sx")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sy")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sz")

            # center - limbus
            limbus_value = mc.getAttr(self.limbus_line_attr)
            for i in range(self.limbus_edge_index):
                length = mc.getAttr(self.locs[i] + ".tx") / self.radius
                value = math.degrees(math.asin(length) * 2) / 180
                ratio = value / limbus_value

                mp = mc.createNode("multiplyDivide")
                mc.setAttr(mp + ".input1X", ratio)
                mc.connectAttr(self.limbus_line_attr, mp + ".input2X")

                mp_180 = mc.createNode("multiplyDivide")
                mc.connectAttr(mp + ".outputX", mp_180 + ".input1X")
                mc.setAttr(mp_180 + ".input2X", 180)

                euler_to_quat = mc.createNode("eulerToQuat")
                mc.connectAttr(mp_180 + ".outputX", euler_to_quat + ".inputRotateX")

                radius_mp = mc.createNode("multiplyDivide")
                mc.connectAttr(euler_to_quat + ".outputQuatX", radius_mp + ".input1X")
                mc.setAttr(radius_mp + ".input2X", self.radius)

                mc.connectAttr(radius_mp + ".outputX", self.locs[i] + ".tx")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sx")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sy")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sz")

            # limbus - pupil
            pupil_value = mc.getAttr(self.pupil_line_attr) - limbus_value
            for i in range(self.limbus_edge_index + 1, self.pupil_edge_index):
                length = mc.getAttr(self.locs[i] + ".tx") / self.radius
                value = math.degrees(math.asin(length) * 2) / 180 - limbus_value
                ratio = value / pupil_value

                r_v = mc.createNode("remapValue")
                mc.setAttr(r_v + ".inputValue", ratio)
                mc.connectAttr(self.limbus_line_attr, r_v + ".outputMin")
                mc.connectAttr(self.pupil_line_attr, r_v + ".outputMax")

                mp_180 = mc.createNode("multiplyDivide")
                mc.connectAttr(r_v + ".outValue", mp_180 + ".input1X")
                mc.setAttr(mp_180 + ".input2X", 180)

                euler_to_quat = mc.createNode("eulerToQuat")
                mc.connectAttr(mp_180 + ".outputX", euler_to_quat + ".inputRotateX")

                radius_mp = mc.createNode("multiplyDivide")
                mc.connectAttr(euler_to_quat + ".outputQuatX", radius_mp + ".input1X")
                mc.setAttr(radius_mp + ".input2X", self.radius)

                mc.connectAttr(radius_mp + ".outputX", self.locs[i] + ".tx")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sx")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sy")
                mc.connectAttr(euler_to_quat + ".outputQuatW", self.locs[i] + ".sz")

            # pupil - last
            end_value = mc.getAttr(self.end_line_attr) - pupil_value - limbus_value
            for loc in self.locs[self.pupil_edge_index + 1:-1]:
                length = mc.getAttr(loc + ".tx") / self.radius
                value = math.degrees(math.asin(length) * 2) / 180 - pupil_value - limbus_value
                ratio = value / end_value

                r_v = mc.createNode("remapValue")
                mc.setAttr(r_v + ".inputValue", ratio)
                mc.connectAttr(self.pupil_line_attr, r_v + ".outputMin")
                mc.connectAttr(self.end_line_attr, r_v + ".outputMax")

                mp_180 = mc.createNode("multiplyDivide")
                mc.connectAttr(r_v + ".outValue", mp_180 + ".input1X")
                mc.setAttr(mp_180 + ".input2X", 180)

                euler_to_quat = mc.createNode("eulerToQuat")
                mc.connectAttr(mp_180 + ".outputX", euler_to_quat + ".inputRotateX")

                radius_mp = mc.createNode("multiplyDivide")
                mc.connectAttr(euler_to_quat + ".outputQuatX", radius_mp + ".input1X")
                mc.setAttr(radius_mp + ".input2X", self.radius)

                mc.connectAttr(radius_mp + ".outputX", loc + ".tx")
                mc.connectAttr(euler_to_quat + ".outputQuatW", loc + ".sx")
                mc.connectAttr(euler_to_quat + ".outputQuatW", loc + ".sy")
                mc.connectAttr(euler_to_quat + ".outputQuatW", loc + ".sz")

            # scale default 1
            for loc, ref in zip(self.locs, self.refs[1:]):
                scale = mc.xform(loc, query=True, scale=True, worldSpace=True)[0]
                for s in [".sx", ".sy", ".sz"]:
                    mc.setAttr(ref + s, lock=False)
                    mc.setAttr(ref + s, 1 / scale)
                    mc.setAttr(ref + s, lock=True)

            # auto skinning
            mesh = data["eyeball_mesh"]
            center_edge_index = int(data["center_edge_index"])
            last_edge_index = int(data["last_edge_index"])
            sc = mc.skinCluster(self.jnts,
                                mesh,
                                name=self.generate_name("", "sc", "ctl"),
                                toSelectedBones=True,
                                bindMethod=1,
                                normalizeWeights=1,
                                weightDistribution=1)[0]
            mc.skinPercent(sc, mesh, transformValue=((self.jnts[0], 1)))
            edges = mc.polySelect(mesh, query=True, edgeRingPath=(center_edge_index, last_edge_index))[1:]
            for jnt, edge in zip(self.jnts[1:], edges):
                loop = [mesh + ".e[" + str(x) + "]" for x in mc.polySelect(mesh, query=True, edgeLoop=edge)[1:]]
                mc.skinPercent(sc, loop, transformValue=((jnt, 1)))

    def connections(self, context):
        super().connections(context)

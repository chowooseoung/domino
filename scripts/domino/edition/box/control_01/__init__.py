# domino
from domino.core import matrix, operators, callback
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Control01Identifier(piece.Identifier):
    madeBy = "Chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "control"
    side = "C"
    index = 0
    description = "controller와 joint를 선택적(controller만 joint만 혹은 둘 다)으로 추가할 수 있습니다. UI로 사용할 수도 있습니다."


class Control01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))

    def __init__(self, node=None, data=None):
        self._identifier = Control01Identifier(self)
        super(Control01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Control01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1],
                        "multi": True},
            "nothing": {"typ": "bool", "value": False},
            "jnt_rig": {"typ": "bool", "value": True},
            "leaf_jnt": {"typ": "bool", "value": False},
            "uni_scale": {"typ": "bool", "value": False},
            "neutral_rotation": {"typ": "bool", "value": False},
            "mirror_behaviour": {"typ": "bool", "value": False},
            "icon": {"typ": "string", "value": "cube"},
            "k_tx": {"typ": "bool", "value": True},
            "k_ty": {"typ": "bool", "value": True},
            "k_tz": {"typ": "bool", "value": True},
            "k_rx": {"typ": "bool", "value": True},
            "k_ry": {"typ": "bool", "value": True},
            "k_rz": {"typ": "bool", "value": True},
            "k_ro": {"typ": "bool", "value": True},
            "k_sx": {"typ": "bool", "value": True},
            "k_sy": {"typ": "bool", "value": True},
            "k_sz": {"typ": "bool", "value": True},
            "default_rotate_order": {"typ": "enum",
                                     "enumName": ["xyz",
                                                  "yzx",
                                                  "zxy",
                                                  "xzy",
                                                  "yxz",
                                                  "zyx"],
                                     "value": "xyz"},
            "space_switch_array": {"typ": "string", "value": ""},
            "ctl_size": {"typ": "double", "value": 1}
        })
        return preset


class Control01Guide(piece.Guide):

    def guide(self):
        super(Control01Guide, self).guide()


class Control01Rig(piece.Rig):

    def objects(self, context):
        super(Control01Rig, self).objects(context)

        data = self.data(Control01Data.SELF)
        assembly_data = self.data(Control01Data.ASSEMBLY)

        m = dt.Matrix(data["anchors"][0])
        if data["neutral_rotation"]:
            m = matrix.get_matrix_from_pos(m.translate)
        else:
            scl = [1, 1, -1] if data["mirror_behaviour"] and self.ddata.negate else [1, 1, 1]
            m = matrix.set_matrix_scale(m, scl)

        root = self.create_root(context, m.translate)
        color = self.get_ik_ctl_color()

        if data["nothing"]:
            name = self.naming("", "ref", "ctl")
            ref = self.create_ref(context=context,
                                  name=name,
                                  anchor=True,
                                  m=None)
            return None

        uni_scale = True if data["uni_scale"] else False
        if assembly_data["force_uni_scale"]:
            uni_scale = True
        if not data["leaf_jnt"]:
            mul_size = dt.Matrix(data["anchors"][0]).scale[2]
            attrs = ["tx", "ty", "tz",
                     "rx", "ry", "rz", "ro",
                     "sx", "sy", "sz"]
            key_attrs = [attr for attr in attrs if data["k_" + attr]]
            name = self.naming("", "", "ctl")
            self.ctl, loc = self.create_ctl(context=context, parent=root, name=name, parent_ctl=None, color=color,
                                            keyable_attrs=key_attrs, m=m, shape=data["icon"],
                                            cns=True if data["space_switch_array"] else False,
                                            width=data["ctl_size"] * mul_size, height=data["ctl_size"] * mul_size,
                                            depth=data["ctl_size"] * mul_size)
            self.create_host(context, self.ctl)
            name = self.naming("", "ref", "ctl")
            ref = self.create_ref(context=context,
                                  name=name,
                                  anchor=True,
                                  m=loc)

            if data["jnt_rig"]:
                name = self.naming("", "", "jnt")
                self.create_jnt(context=context,
                                parent=None,
                                name=name,
                                description="",
                                ref=ref,
                                m=m,
                                leaf=False,
                                uni_scale=uni_scale)
        else:
            name = self.naming("", "", "jnt")
            self.create_jnt(context=context,
                            parent=None,
                            name=name,
                            description="",
                            ref=None,
                            m=m,
                            leaf=True,
                            uni_scale=uni_scale)

    def attributes(self, context):
        super(Control01Rig, self).attributes(context)

    def operators(self, context):
        super(Control01Rig, self).operators(context)
        data = self.data(Control01Data.SELF)

        if data["nothing"]:
            return None

        host = self.host()
        if data["space_switch_array"] and not data["leaf_jnt"]:
            source_ctls = self.find_ctls(data["space_switch_array"])
            operators.space_switch(source_ctls, self.ctl, host)
            script_node = callback.space_switch(source_ctls, self.ctl, host)
            if script_node:
                context["callbacks"].append(script_node)

    def connections(self, context):
        super(Control01Rig, self).connections(context)


class Control01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Control01Data(node=node, data=data)
        self._guide = Control01Guide(self._ddata)
        self._rig = Control01Rig(self._ddata)

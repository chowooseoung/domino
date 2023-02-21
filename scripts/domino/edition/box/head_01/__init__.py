# domino
from domino.core.api import matrix, vector
from domino.edition.api import piece

# built-ins
import os

# maya
from pymel import core as pm

dt = pm.datatypes


class Head01Identifier(piece.Identifier):
    madeBy = "chowooseung"
    contact = "main.wooseung@gmail.com"
    piece = os.path.split(os.path.dirname(__file__))[-1]
    version = (1, 0, 0)
    name = "head"
    side = "C"
    index = 0
    description = "머리 입니다."


class Head01Data(piece.DData):
    _m1 = matrix.get_matrix_from_pos((0, 0, 0))  # root
    _m2 = matrix.get_matrix_from_pos((0, 2, 0))  # end
    _m3 = matrix.get_matrix_from_pos((0, 0, 0.2))  # aim

    def __init__(self, node=None, data=None):
        self._identifier = Head01Identifier(self)
        super(Head01Data, self).__init__(node=node, data=data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def preset(self):
        preset = super(Head01Data, self).preset
        preset.update({
            "anchors": {"typ": "matrix",
                        "value": [self._m1, self._m2, self._m3],
                        "multi": True},
            "head_aim_array": {"typ": "string",
                               "value": ""},
        })
        return preset


class Head01Guide(piece.Guide):

    def guide(self):
        data = self.data(Head01Data.SELF)
        root = super(Head01Guide, self).guide()
        pos = self.create_position(root, data["anchors"][1])
        pos1 = self.create_position(root, data["anchors"][2])
        self.create_display_crv(root, [root, pos])
        self.create_display_crv(root, [root, pos1])


class Head01Rig(piece.Rig):

    def objects(self, context):
        super(Head01Rig, self).objects(context)

        data = self.data(Head01Data.SELF)
        assembly_data = self.data(Head01Data.ASSEMBLY)

        uni_scale = False
        if assembly_data["force_uni_scale"]:
            uni_scale = True

        m0 = dt.Matrix(data["anchors"][0])
        m1 = dt.Matrix(data["anchors"][1])
        m2 = dt.Matrix(data["anchors"][2])

        root = self.create_root(context, m0.translate)
        fk_color = self.get_fk_ctl_color()

        normal = m1.translate - m0.translate
        distance = vector.get_distance(m0.translate, m1.translate)
        m = matrix.get_matrix_look_at(m0.translate, m2.translate, normal, "-yx", self.ddata.negate)
        name = self.naming(_s="ctl")
        self.ctl, self.loc = self.create_ctl(context=context,
                                             parent=None,
                                             name=name,
                                             parent_ctl=None,
                                             color=fk_color,
                                             keyable_attrs=["tx", "ty", "tz",
                                                            "rx", "ry", "rz", "ro",
                                                            "sx", "sy", "sz"],
                                             m=m,
                                             shape="cube",
                                             cns=False,
                                             width=distance,
                                             po=(distance / 3.0, 0, 0))

        name = self.naming("", "ref", _s="ctl")
        self.ref = self.create_ref(context=context,
                                   name=name,
                                   anchor=True,
                                   m=self.loc)
        name = self.naming(_s="jnt")
        self.jnt = self.create_jnt(context=context,
                                   parent=None,
                                   name=name,
                                   description="",
                                   ref=self.ref,
                                   m=m,
                                   leaf=False,
                                   uni_scale=uni_scale)

    def attributes(self, context):
        super(Head01Rig, self).attributes(context)

    def operators(self, context):
        super(Head01Rig, self).operators(context)

    def connections(self, context):
        super(Head01Rig, self).connections(context)


class Head01Piece(piece.AbstractPiece):

    def __init__(self, node=None, data=None):
        self._ddata = Head01Data(node=node, data=data)
        self._guide = Head01Guide(self._ddata)
        self._rig = Head01Rig(self._ddata)

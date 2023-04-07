# maya
from maya import cmds as mc
from maya.api import OpenMaya as om2

# domino
from domino.lib import vector, matrix


def reset(node, attrs):
    for attr in attrs:
        default_value = mc.attributeQuery(attr, node=node, listDefault=True)[0]
        try:
            mc.setAttr(f"{node}.{attr}", default_value)
        except:
            pass


def reset_published_attr(containers):
    for container in containers:
        publish_attrs = [x[0] for x in mc.container(container, query=True, bindAttr=True)]
        for attr in publish_attrs:
            node, attr_name = attr.split(".")
            reset(node, [attr_name])


def reset_all(nodes):
    for node in nodes:
        keyable_attrs = mc.listAttr(node, keyable=True) or []
        nonkeyable_attrs = mc.listAttr(node, channelBox=True) or []
        attrs = keyable_attrs + nonkeyable_attrs
        reset(node, list(set(attrs)))


def reset_SRT(nodes, attributes=("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")):
    for node in nodes:
        reset(node, attributes)


def fk_to_ik(source, target, host, offset):
    pole_vec_pos = vector.calculate_pole_vector(*source[:3], offset)
    pole_vec_m = matrix.set_matrix_translate(om2.MMatrix(), pole_vec_pos)
    ik_ctl_m = matrix.get_matrix(source[-1])

    mc.setAttr(host + ".fk_ik", 1)
    ik_ctl, pole_vec_ctl = target
    mc.xform(pole_vec_ctl, matrix=pole_vec_m, worldSpace=True)
    mc.xform(ik_ctl, matrix=ik_ctl_m, worldSpace=True)


def ik_to_fk(source, target, host):
    mc.setAttr(host + ".fk_ik", 0)
    [mc.matchTransform(t, source[i], rotation=True) for i, t in enumerate(target)]


def fix_auto_clavicle(shoulder_ctl, shoulder_position):
    aim_node = mc.createNode("transform", name="MATCHCLAVICLETEMP")
    mc.setAttr(aim_node + ".t", *shoulder_position)

    cons = mc.aimConstraint(aim_node, shoulder_ctl, maintainOffset=True)
    return cons, aim_node


def switch_fk_ik(host, frame_range=(), set_key=False):
    clavicle_ctl = None
    if mc.attributeQuery("clavicle_ctl", node=host, exists=True):
        clavicle_ctl = mc.listConnections(host + ".clavicle_ctl", source=True, destination=False)[0]

    current_state = round(mc.getAttr(host + ".fk_ik"), 0)
    if current_state:
        source = mc.listConnections(host + ".fk_match_source", source=True, destination=False)
        target = mc.listConnections(host + ".fk_match_target", source=True, destination=False)
    else:
        source = mc.listConnections(host + ".ik_match_source", source=True, destination=False)
        target = mc.listConnections(host + ".ik_match_target", source=True, destination=False)

    if not frame_range:
        frame_range = [mc.currentTime(query=True), mc.currentTime(query=True) + 1]

    next_shoulder_rotate = []
    if clavicle_ctl:
        for f in range(int(frame_range[0]), int(frame_range[1])):
            next_shoulder_rotate.append(mc.getAttr(clavicle_ctl + ".r", time=f)[0])

    for i, f in enumerate(range(int(frame_range[0]), int(frame_range[1]))):
        mc.currentTime(f)

        cons = aim_node = None
        if clavicle_ctl:
            if current_state:
                mc.setAttr(host + ".fk_ik", 1)
            else:
                mc.setAttr(host + ".fk_ik", 0)
            mc.setAttr(clavicle_ctl + ".r", *next_shoulder_rotate[i])
            cons, aim_node = fix_auto_clavicle(clavicle_ctl, vector.get_position(source[0]))

        if current_state:
            ik_to_fk(source=source, target=target, host=host)
        else:
            component_root = mc.listConnections(host + ".component_root", source=True, destination=False)[0]
            offset = mc.getAttr(component_root + ".offset_pole_vec")
            fk_to_ik(source=source, target=target, host=host, offset=offset)

        if set_key:
            mc.setKeyframe([host] + target + [clavicle_ctl], attribute=["tx", "ty", "tz", "rx", "ry", "rz", "fk_ik"])

        if clavicle_ctl:
            mc.delete(cons)
            mc.delete(aim_node)


def calculate_mirror_data(src, target, flip=False):
    transform_attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    transform_attrs = [attr for attr in transform_attrs if not mc.getAttr(src + "." + attr, lock=True)]

    user_attrs = [attr for attr in mc.listAttr(src, userDefined=True, keyable=True) or []]
    user_attrs = [attr for attr in user_attrs
                  if mc.attributeQuery(attr, node=src, attributeType=True) not in ["message", "string", "enum"]
                  and not mc.getAttr(src + "." + attr, lock=True)]

    data = []
    for attr in list(transform_attrs) + list(user_attrs):
        inv_value = 1

        inv_check_attr = "inv" + attr.capitalize()
        if mc.attributeQuery(inv_check_attr, node=src, exists=True) and mc.getAttr(src + "." + inv_check_attr):
            inv_value = -1

        # if flip, add self
        if flip:
            val = mc.getAttr(target + "." + attr)
            data.append(
                {"target": src, "attr": attr, "value": val * inv_value}
            )
        val = mc.getAttr(src + "." + attr)
        data.append(
            {"target": target, "attr": attr, "value": val * inv_value}
        )
    return data


def apply_mirror_pose(data):
    node = data["target"]
    attr = data["attr"]
    value = data["value"]

    try:
        if mc.attributeQuery(attr, node=node, exists=True) and not mc.getAttr(node + "." + attr, lock=True):
            mc.setAttr(node + "." + attr, value)
    except RuntimeError as e:
        import traceback

        traceback.print_exc()
        print(e)


def mirror_pose(nodes=None, flip=False):
    if not nodes:
        nodes = mc.ls(selection=True, long=True)

    if not nodes:
        return None

    mc.undoInfo(openChunk=True)
    namespace = mc.ls(nodes[0], showNamespace=True)[1]
    try:
        mirror_data = []
        for node in nodes:
            target = namespace + mc.getAttr(node + ".mirror_ctl_name")

            # target ctl data
            mirror_data.extend(calculate_mirror_data(node, target))

            # selected ctl flip data
            if target not in nodes and flip:
                mirror_data.extend(calculate_mirror_data(target, node))

        for data in mirror_data:
            apply_mirror_pose(data)
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(e)
    finally:
        mc.undoInfo(closeChunk=True)

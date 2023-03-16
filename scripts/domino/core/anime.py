# maya
from pymel import core as pm

# domino
from domino.core import matrix


def reset(obj, attrs):
    for attr in attrs:
        default_value = pm.attributeQuery(attr, node=obj, listDefault=True)[0]
        try:
            pm.setAttr(f"{obj}.{attr}", default_value)
        except:
            pass


def reset_published_attr(containers):
    for container in containers:
        publish_attrs = [x[0] for x in pm.container(container, query=True, bindAttr=True)]
        for attr in publish_attrs:
            reset(attr.node(), [attr.attrName()])


def reset_all(objs):
    for obj in objs:
        keyable_attrs = pm.listAttr(obj, keyable=True) or []
        nonkeyable_attrs = pm.listAttr(obj, channelBox=True) or []
        attrs = keyable_attrs + nonkeyable_attrs
        reset(obj, list(set(attrs)))


def reset_SRT(objs, attributes=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]):
    for obj in objs:
        reset(obj, attributes)


def fk_to_ik(source, target, host):
    pole_vec_pos = matrix.get_pole_vec_position([x.getTranslation(worldSpace=True) for x in source], 2)
    pole_match_obj = pm.createNode("transform", name="MATCHFKTOIKPOLEVECTEMP")
    pole_match_obj.attr("t").set(pole_vec_pos)
    ik_ctl_match_obj = pm.createNode("transform", name="MATCHTOIKCTLTEMP")
    pm.matchTransform(ik_ctl_match_obj, source[-1], position=True, rotation=True)

    pm.setAttr(host.attr("fk_ik"), 1)
    ik_ctl, pole_vec_ctl = target
    pm.matchTransform(pole_vec_ctl, pole_match_obj, position=True)
    pm.matchTransform(ik_ctl, ik_ctl_match_obj, position=True, rotation=True)
    pm.delete([pole_match_obj, ik_ctl_match_obj])


def ik_to_fk(source, target, host):
    pm.setAttr(host.attr("fk_ik"), 0)
    [pm.matchTransform(t, source[i], rotation=True) for i, t in enumerate(target)]


def fix_auto_clavicle(shoulder_ctl, shoulder_position):
    aim_obj = pm.createNode("transform", name="MATCHCLAVICLETEMP")
    aim_obj.attr("t").set(shoulder_position)

    cons = pm.aimConstraint(aim_obj, shoulder_ctl, maintainOffset=True)
    return cons, aim_obj


def switch_fk_ik(host, frame_range=[], set_key=False):
    if not isinstance(host, pm.PyNode):
        host = pm.PyNode(host)

    shoulder_ctl = None
    if host.hasAttr("shoulder_ctl"):
        shoulder_ctl = host.attr("shoulder_ctl").inputs()[0]

    current_state = round(host.attr("fk_ik").get(), 0)
    if current_state:
        source = host.attr("fk_match_source").inputs()
        target = host.attr("fk_match_target").inputs()
    else:
        source = host.attr("ik_match_source").inputs()
        target = host.attr("ik_match_target").inputs()

    current_frame = pm.currentTime(query=True)
    if not frame_range:
        frame_range = [current_frame, current_frame + 1]

    next_shoulder_rotate = []
    if shoulder_ctl:
        for f in range(int(frame_range[0]), int(frame_range[1])):
            next_shoulder_rotate.append(pm.getAttr(shoulder_ctl.attr("r"), time=f))

    for i, f in enumerate(range(int(frame_range[0]), int(frame_range[1]))):
        pm.currentTime(f)

        cons = aim_obj = None
        if shoulder_ctl:
            if current_state:
                pm.setAttr(host.attr("fk_ik"), 1)
            else:
                pm.setAttr(host.attr("fk_ik"), 0)
            pm.setAttr(shoulder_ctl.attr("r"), next_shoulder_rotate[i])
            cons, aim_obj = fix_auto_clavicle(shoulder_ctl, source[0].getTranslation(worldSpace=True))

        if current_state:
            ik_to_fk(source=source, target=target, host=host)
        else:
            fk_to_ik(source=source, target=target, host=host)

        if set_key:
            pm.setKeyframe([host] + target + [shoulder_ctl], attribute=["tx", "ty", "tz", "rx", "ry", "rz", "fk_ik"])

        if shoulder_ctl:
            pm.delete(cons)
            pm.delete(aim_obj)

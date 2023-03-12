# maya
from pymel import core as pm

# built-ins
import os
import uuid
import json
import inspect
import traceback
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

# domino
from . import utils
from .piece import AbstractSubPiece, Rig
from ...core import log, matrix
from .utils import DOMINO_SUB_PIECE_DIR

dt = pm.datatypes


def create_guide(module=None, datas=None, parent=None):
    if module is None and datas is None:
        msg = f"module : {module!r}, datas : {datas!r}"
        raise RuntimeError(f"{create_guide.__name__!r} {msg}")
    elif module and datas:
        msg = f"module : {module!r}, ddatas : {datas!r}"
        raise RuntimeError(f"{create_guide.__name__!r} {msg}")

    if datas:
        pieces = utils.collect_piece(guide=None, rig=None, datas=datas)
        for p in pieces:
            p.guide.guide()
        for p in pieces:
            p.ddata.sync(True)
        pm.select(pieces[0].ddata.node)
        return 0

    selection = pm.ls(selection=True)
    if not selection and parent is None:
        pieces = []
        for m in ["assembly_01", module]:
            mod = utils.import_piece_module(m)
            new_piece = utils.get_piece_attr(mod)
            if new_piece is None:
                msg = f"Empty Module {mod}"
                raise RuntimeError(f"{mod.__name__!r} {msg}")
            p = new_piece()
            guide = p.guide
            if guide.guide() is False:
                pm.delete(pm.ls(selection=True)[0].getParent(generations=-1))
                return 0
            pieces.append(p.ddata.node)
        pm.parent(pieces[1], pieces[0])
        pm.select(pieces[1])
        pieces[1].attr("t").set(0, 0, 0)
        return 0

    if not selection[0].hasAttr("is_domino_guide"):
        return None
    if selection[0].attr("hiddenInOutliner").get():
        selection[0] = selection[0].getParent()
    parent = parent if parent else selection[0]
    parent_root = pm.listConnections(parent.attr("worldMatrix")[0],
                                     destination=True,
                                     source=False,
                                     type="dagContainer")[0]
    side = None
    if parent_root.attr("piece").get() != "assembly_01":
        side = parent_root.attr("side").get(asString=True)
    top_node = parent.getParent(generations=-1)
    pieces = utils.collect_piece(guide=top_node, rig=None, datas=None)

    mod = utils.import_piece_module(module)
    new_piece = utils.get_piece_attr(mod)
    if new_piece is None:
        msg = f"Empty Module {mod}"
        raise RuntimeError(f"{create_guide.__name__!r} {msg}")
    p = new_piece()
    guide = p.guide
    if side:
        p.ddata._data["side"] = side
    guide.set_suitable_index(pieces)
    if guide.guide() is False:
        return 0
    guide.ddata.sync(True)
    pm.parent(p.ddata.node, parent)
    pm.select(p.ddata.node)
    p.ddata.node.attr("t").set(0, 0, 0)
    return 0


def copy_guide(guide):
    if not guide.hasAttr("d_id"):
        return None
    with pm.UndoChunk():
        new = pm.duplicate(guide,
                           returnRootsOnly=True,
                           upstreamNodes=True,
                           renameChildren=True)
        root = guide.getParent(generations=-1)
        pieces = utils.collect_piece(guide=root, rig=None, datas=None)
        new_containers = pm.ls(new, dagObjects=True, type="dagContainer")
        new_pieces = utils.collect_piece(guide=new, rig=None, datas=None)
        for index, _ in enumerate(new_containers):
            new_pieces[index].ddata.sync()
            new_pieces[index].guide.set_suitable_index(pieces)
            new_pieces[index].ddata.sync(True)
            new_pieces[index].ddata.node.attr("d_id").set(str(uuid.uuid4()))


def mirror_guide(guide):
    if not guide.hasAttr("d_id"):
        return None
    if guide.attr("piece").get() == "assembly_01":
        return None
    child_pieces = pm.ls(guide, dagObjects=True, type="dagContainer")
    for child in child_pieces:
        if child.attr("side").get(asString=True) == "C":
            raise RuntimeError("Mirror Copy must not have 'C' side")
    with pm.UndoChunk():
        orig_containers = pm.ls(guide, dagObjects=True, type="dagContainer")
        root = guide.getParent(generations=-1)
        pieces = utils.collect_piece(guide=root, rig=None, datas=None)
        new = pm.duplicate(guide,
                           returnRootsOnly=True,
                           upstreamNodes=True,
                           renameChildren=True)
        new_containers = pm.ls(new, dagObjects=True, type="dagContainer")
        new_pieces = utils.collect_piece(guide=new, rig=None, datas=None)
        for index, container in enumerate(new_containers):
            side = container.attr("side").get(asString=True)
            mirror_side = "R" if side == "L" else "L"
            en = pm.attributeQuery("side", node=container, listEnum=True)
            i = en[0].split(":").index(mirror_side)
            container.attr("side").set(i)
            container.attr("d_id").set(str(uuid.uuid4()))
            host = container.attr("host").get()
            if host:
                host_side = host.split("_")[-1][0]
                if host_side != "C":
                    mirror_host_side = "R" if host_side == "L" else "L"
                    mirror_host = host.replace(f"_{host_side}", f"_{mirror_host_side}")
                    container.attr("host").set(mirror_host)

            for i in pm.listAttr(container, userDefined=True):
                if "space_switch_array" in i:
                    mirror_data = []
                    data = container.attr(i).get()
                    if data:
                        data = data.split(",")
                        ctl_index = [x.split(" | ")[0] for x in data]
                        identifier = [x.split(" | ")[1] for x in data]
                        for _i, _id in zip(ctl_index, identifier):
                            if "_" in _id:
                                _name, _side_index = _id.split("_")
                                _side = _side_index[0]
                                _index = _side_index[1:]
                            else:
                                mirror_data.append(" | ".join([_i, _id]))
                                continue
                            if _side == "C":
                                mirror_data.append(" | ".join([_i, _id]))
                            else:
                                mirror_side = "R" if _side == "L" else "L"
                                replace_id = f"{_name}_{mirror_side}{_index}"
                                mirror_data.append(" | ".join([_i, replace_id]))
                        container.attr(i).set(",".join(mirror_data))

            orig_anchors_inputs = pm.listConnections(orig_containers[index].attr("anchors"),
                                                     destination=False,
                                                     source=True)
            anchors_inputs = pm.listConnections(f"{container}.anchors",
                                                destination=False,
                                                source=True)
            for orig_t, new_t in zip(orig_anchors_inputs, anchors_inputs):
                m = orig_t.getMatrix(worldSpace=True)
                m_m = matrix.get_mirror_matrix(dt.Matrix(m))
                new_t.setMatrix(m_m, worldSpace=True)
            new_pieces[index].ddata.sync()
            new_pieces[index].guide.set_suitable_index(pieces)
            new_pieces[index].ddata.sync(True)
    return 0


def run_sub_pieces(context, sub_pieces):
    if not context["run_sub_pieces"]:
        return 0
    for _p in sub_pieces.copy():
        if _p in ["objects", "attributes", "operators", "connections", "cleanup"]:
            break
        name, path = _p.split(" | ")
        if not os.path.exists(path):
            sub_piece_dir = os.path.abspath(os.getenv(DOMINO_SUB_PIECE_DIR, None))
            if sub_piece_dir:
                path = os.path.join(sub_piece_dir, path[1:])
        if name.startswith("*"):
            log.Logger.info(f"Skip Sub Piece[{name[1:]} {path}]...")
            continue
        elif not os.path.isfile(path) or not os.path.splitext(path)[-1] == ".py":
            log.Logger.info(f"Plz confirm [{name[1:]} {path}]...")
            continue
        n = f"domino.sub_piece.{name}"
        spec = spec_from_loader(n, SourceFileLoader(n, path))
        if spec:
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            utils.reload_module(module)
        _cls = False
        if module:
            log.Logger.info(f"Run Sub Piece[{name} {path}]...")
            for a in dir(module):
                sub_piece = getattr(module, a)
                if inspect.isclass(sub_piece):
                    if issubclass(sub_piece, AbstractSubPiece):
                        _cls = sub_piece()
                        _cls.run(context)
                        break
        if not _cls:
            log.Logger.error(f"Sub Piece[{name} {path}]...")
        sub_pieces.pop(0)
    if sub_pieces:
        sub_pieces.pop(0)


def create_rig(guide=None, rig=None, datas=None, context=None):
    if context is None:
        context = dict()

    if guide:
        if pm.nodeType(guide) != "dagContainer":
            raise RuntimeError(f"guide arg must be 'dagContainer'")
    roots_grp = None
    if rig:
        root = rig.getParent(generations=-1)
        asset_container = pm.container(query=True, findContainer=root)
        roots_grp_index = pm.containerPublish(asset_container, query=True, bindNode=True).index("roots")
        roots_grp = pm.containerPublish(asset_container, query=True, bindNode=True)[roots_grp_index + 1]
        if not roots_grp:
            raise RuntimeError(f"rig arg must be rigging dag node")

    # collect
    pieces = utils.collect_piece(guide=guide,
                                 rig=roots_grp,
                                 datas=datas,
                                 include_assembly=True)
    context["pieces"] = pieces

    log.Logger.info("{: ^50}".format("- domino -"))
    try:
        with pm.UndoChunk():
            # domino #
            assembly_data = pieces[0].ddata.data(pieces[0].ddata.ASSEMBLY)
            subs = [x for x in assembly_data["sub_pieces"].split(",")]

            context["run_sub_pieces"] = assembly_data["run_sub_pieces"]
            run_sub_pieces(context, subs)

            pieces[0].rig.create_asset(context)
            for p in pieces:
                p.rig.create_container(context)

            # objects
            for p in pieces:
                log.Logger.info(f"Objects[{str(p.identifier)}]...")
                p.rig.set_current_container()
                p.rig.objects(context)
                p.rig.sub_jnt(context)
            assert assembly_data["end_point"] != "objects", AssertionError("End Point : objects")

            run_sub_pieces(context, subs)

            # attributes
            for p in pieces:
                log.Logger.info(f"Attributes[{str(p.identifier)}]...")
                p.rig.set_current_container()
                p.rig.attributes(context)
            assert assembly_data["end_point"] != "attributes", AssertionError("End Point : attributes")

            run_sub_pieces(context, subs)

            # operators
            for p in pieces:
                log.Logger.info(f"Operators[{str(p.identifier)}]...")
                p.rig.set_current_container()
                p.rig.operators(context)
            assert assembly_data["end_point"] != "operators", AssertionError("End Point : operators")

            run_sub_pieces(context, subs)

            # connections
            for p in pieces:
                log.Logger.info(f"Connections[{str(p.identifier)}]...")
                p.rig.set_current_container()
                p.rig.connections(context)
            assert assembly_data["end_point"] != "connections", AssertionError("End Point : connections")

            pm.mel.eval("ClearCurrentContainer;")

            run_sub_pieces(context, subs)

            # cleanup
            log.Logger.info(f"Clean up...")
            Rig.create_sets(context)
            Rig.setup_host(context)
            Rig.setup_ctl(context)
            Rig.setup_jnt(context)
            Rig.callback(context)

            assert assembly_data["end_point"] != "cleanup", AssertionError("End Point : cleanup")

            run_sub_pieces(context, subs)

    except AssertionError as e:
        log.Logger.info(e)
    except:
        log.Logger.error(traceback.format_exc())
    finally:
        pm.mel.eval("ClearCurrentContainer;")
        if context["mode"] == "DEBUG":
            log.Logger.info("Debug mode. all contents remove from asset")
            Rig.debug_mode(context)
        elif context["mode"] == "PUB":
            log.Logger.info("Publish mode. all assets not publish attribute lock")
            Rig.blackbox(context)

        # select
        if context["asset"][1].hasAttr("sets"):
            sets = context["asset"][1].attr("sets").inputs()
            if sets:
                pm.select(sets, noExpand=True, replace=True)
        if pm.objExists(context["asset"][0]):
            pm.select(context["asset"][0], add=True)
        if pm.objExists(context["asset"][1]):
            pm.select(context["asset"][1], add=True)

        log.Logger.info("{:+^50}".format("CONTEXT"))
        for key, value in context.items():
            log.Logger.info(f"{key}: {value}")
        log.Logger.info("{:=^50}".format(""))
        del context


def add_blended_jnt():
    selected = pm.ls(selection=True, type="joint")
    if not selected:
        return None
    plugs = pm.listConnections(selected[0].attr("message"),
                               plugs=True,
                               type="transform",
                               destination=True,
                               source=False)
    if not plugs:
        return None
    plug = [x for x in plugs if "jnts" in x.attrName()]
    if not plug:
        return None

    index = plug[0].index()
    selected_root = plug[0].node()

    asset = selected[0].getParent(generations=-1)
    container = pm.container(query=True, findContainer=asset)
    if container:
        selected_container = pm.container(query=True, findContainer=selected_root)
        pm.container(selected_container, edit=True, current=True)

    roots_grp = [x for x in asset.getChildren() if "roots" in x.name()][0]
    pieces = utils.collect_piece(guide=None, rig=roots_grp, datas=None)
    d_id = selected_root.attr("d_id").get()
    piece = [p for p in pieces if p.ddata._data["d_id"] == d_id][0]
    piece.rig.root = selected_root
    jnt = piece.rig.create_blended_jnt(name="", index=index)

    if jnt is not None:
        pm.select(jnt)
        sets = pm.listConnections(asset.attr("jnt_sets"), type="objectSet", destination=False, source=True)
        if sets:
            child_sets = [x for x in pm.sets(sets[0], query=True) if x.type() == "objectSet"]
            sets.extend(child_sets)
            for s in sets:
                if pm.sets(s, isMember=selected[0]):
                    pm.sets(s, addElement=jnt)
        ssc = selected[0].attr("segmentScaleCompensate").get()
        jnt.attr("segmentScaleCompensate").set(ssc)
    else:
        pm.select(selected)
    if container:
        pm.mel.eval("ClearCurrentContainer;")
    return jnt


def add_support_jnt():
    selected = pm.ls(selection=True, type="joint")
    if not selected:
        return None
    plugs = pm.listConnections(selected[0].attr("message"),
                               plugs=True,
                               type="transform",
                               destination=True,
                               source=False)
    if not plugs:
        return None
    plug = [x for x in plugs if "blended_jnts" in x.attrName()]
    if not plug:
        return None

    result = pm.promptDialog(title="Add support jnt Dialog",
                             message="Enter description :",
                             button=("Ok", "Cancel"),
                             defaultButton="OK",
                             cancelButton="Cancel",
                             dismissString="")
    if not result:
        return None
    description = pm.promptDialog(query=True, text=True)

    index = plug[0].index()
    selected_root = plug[0].node()

    count = 0
    while pm.listConnections(selected_root.attr("support_jnts")[count], source=True, destination=False):
        count += 1

    asset = selected[0].getParent(generations=-1)
    container = pm.container(query=True, findContainer=asset)
    if container:
        selected_container = pm.container(query=True, findContainer=selected_root)
        pm.container(selected_container, edit=True, current=True)

    roots_grp = [x for x in asset.getChildren() if "roots" in x.name()][0]
    pieces = utils.collect_piece(guide=None, rig=roots_grp, datas=None)
    d_id = selected_root.attr("d_id").get()
    piece = [p for p in pieces if p.ddata._data["d_id"] == d_id][0]
    m = selected[0].getMatrix(worldSpace=True)
    piece.rig.root = selected_root
    jnt = piece.rig.create_support_jnt(name="",
                                       description=description,
                                       blended_index=index,
                                       count=count,
                                       m=dt.Matrix(m))
    if jnt is not None:
        pm.select(jnt)
        sets = pm.listConnections(asset.attr("jnt_sets"), type="objectSet", destination=False, source=True)
        if sets:
            child_sets = [x for x in pm.sets(sets[0], query=True) if x.type() == "objectSet"]
            sets.extend(child_sets)
            for s in sets:
                if pm.sets(s, isMember=selected[0]):
                    pm.sets(s, addElement=jnt)
        ssc = selected[0].attr("segmentScaleCompensate").get()
        selected[0].attr("segmentScaleCompensate").set(ssc)
    else:
        pm.select(selected)
    if container:
        pm.mel.eval("ClearCurrentContainer;")
    return jnt


def extract_ctl_shapes(ctls):
    for ctl in ctls:
        if not ctl.hasAttr("is_domino_ctl"):
            continue
        plugs = pm.listConnections(f"{ctl}.message", destination=True, source=False, plugs=True, type="transform")[0]
        if plugs.attrName() != "ctls":
            continue
        index = plugs.index()
        root = plugs.node()
        pm.disconnectAttr(root.attr("ncurve_ctls_shapes")[index])
        pm.connectAttr(ctl.attr("message"), root.attr("ncurve_ctls_shapes")[index], force=True)


def save(dotfile):
    selected = pm.ls(selection=True)
    if not selected:
        return None
    if selected[0].type() == "container":
        selected = [pm.container(selected[0],
                                 query=True,
                                 publishAsRoot=True)]

    root = selected[0].getParent(generations=-1)
    is_guide = root.hasAttr("is_domino_guide")
    is_rig = root.hasAttr("is_domino_asset")
    if not is_guide and not is_rig:
        raise RuntimeError("select domino guide or rig")
    if is_rig:
        root = [x for x in root.getChildren() if "roots" in x.name()][0]
    argument = {"guide": root if is_guide else None,
                "rig": root if is_rig else None,
                "datas": None}
    pieces = utils.collect_piece(**argument)
    datas = [p.ddata._data for p in pieces]
    with open(dotfile, "w") as f:
        json.dump(datas, f, indent=2)


def load(dotfile, guide=False, rig=True):
    if not os.path.exists(dotfile):
        raise RuntimeError(f"Don't exists {dotfile}")
    with open(dotfile, "r") as f:
        datas = json.load(f)
    if guide:
        create_guide(datas=datas)
    if rig:
        create_rig(guide=None, rig=None, datas=datas)

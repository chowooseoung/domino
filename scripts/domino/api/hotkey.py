# maya
import pymel.core as pm


def set_key_to_character_set():
    selected = pm.selected()
    if not selected:
        pm.mel.eval("SetKey;")
        return 0
    
    not_domino_ctls = []
    character_sets = []
    for sel in selected:
        if not sel.hasAttr("is_domino_ctl"):
            not_domino_ctls.append(sel)
            continue

        char = sel.attr("character_set_name").get()
        namespace = sel.namespace()

        if namespace:
            char = namespace + char
        character_sets.append(char)
    if not_domino_ctls:
        pm.select(not_domino_ctls)    
        pm.mel.eval("SetKey;")
    for c_set in list(set(character_sets)):
        pm.mel.eval("setCurrentCharacters({{\"{}\"}});".format(c_set))
        pm.mel.eval("SetKey;")
        pm.mel.eval("setCurrentCharacters({});")
    pm.select(selected)

"""
전체 상태 확인 + Use_AlphaComp 13으로 복구
"""
import unreal
import re

asset_path = "/Game/Material/_define/FX/M_FX_01"
material = unreal.EditorAssetLibrary.load_asset(asset_path)
mel = unreal.MaterialEditingLibrary
num_exprs = mel.get_num_material_expressions(material)

all_param_types = []
for attr in dir(unreal):
    if "Parameter" in attr and "MaterialExpression" in attr:
        cls = getattr(unreal, attr, None)
        if cls is not None:
            all_param_types.append(cls)

groups = {}
for cls in all_param_types:
    class_name = cls.__name__
    for i in range(300):
        obj_name = f"{class_name}_{i}"
        expr = unreal.find_object(material, obj_name)
        if expr is None:
            if i > num_exprs + 50:
                break
            continue
        try:
            group = str(expr.get_editor_property("group"))
            param_name = str(expr.get_editor_property("parameter_name"))
        except Exception:
            continue
        if not group:
            group = "(None)"
        if group not in groups:
            groups[group] = []
        groups[group].append(f"{param_name} [{class_name}]")

        # Use_AlphaComp 복구: 12 -> 13
        if param_name == "Use_AlphaComp" and group == "12_AlphaComposite":
            expr.set_editor_property("group", "13_AlphaComposite")
            print(f"FIX: {param_name}: 12_AlphaComposite -> 13_AlphaComposite")
            groups.setdefault("13_AlphaComposite", [])
            groups["13_AlphaComposite"].append(f"{param_name} [{class_name}] (FIXED)")
            groups["12_AlphaComposite"] = [x for x in groups.get("12_AlphaComposite", []) if param_name not in x]

unreal.EditorAssetLibrary.save_loaded_asset(material)

print("\n=== Final Group State ===")
for g in sorted(groups.keys()):
    items = groups[g]
    if not items:
        continue
    print(f"\n[{g}] ({len(items)})")
    for p in items:
        print(f"  - {p}")

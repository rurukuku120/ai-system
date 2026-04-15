"""
M_FX_01 - 그룹별 파라미터 목록 조회
모든 MaterialExpression*Parameter 타입 자동 탐색
"""
import unreal

asset_path = "/Game/Material/_define/FX/M_FX_01"
material = unreal.EditorAssetLibrary.load_asset(asset_path)
mel = unreal.MaterialEditingLibrary

num_exprs = mel.get_num_material_expressions(material)
print(f"Expression count: {num_exprs}")

# 모든 Parameter Expression 타입 자동 수집
all_param_types = []
for attr in dir(unreal):
    if "Parameter" in attr and "MaterialExpression" in attr:
        cls = getattr(unreal, attr, None)
        if cls is not None:
            all_param_types.append(cls)

groups = {}
found_total = 0

for cls in all_param_types:
    class_name = cls.__name__
    type_label = class_name.replace("MaterialExpression", "")
    for i in range(300):
        obj_name = f"{class_name}_{i}"
        expr = unreal.find_object(material, obj_name)
        if expr is None:
            if i > num_exprs + 50:
                break
            continue

        try:
            param_name = expr.get_editor_property("parameter_name")
            group = expr.get_editor_property("group")
            sort_pri = expr.get_editor_property("sort_priority")
        except Exception:
            continue

        found_total += 1
        group_str = str(group) if group else "(None)"
        if group_str not in groups:
            groups[group_str] = []
        groups[group_str].append(f"{param_name} [{type_label}] (sort: {sort_pri})")

print(f"Found parameters: {found_total}")
print("\n=== Groups ===")
for g in sorted(groups.keys()):
    print(f"\n[{g}] ({len(groups[g])})")
    for p in groups[g]:
        print(f"  - {p}")

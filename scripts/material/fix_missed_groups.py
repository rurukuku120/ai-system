"""
누락된 Parameter 타입 포함하여 02_ 이하 잔여 그룹 시프트
모든 MaterialExpression*Parameter 타입을 스캔
"""
import unreal
import re

asset_path = "/Game/Material/_define/FX/M_FX_01"
material = unreal.EditorAssetLibrary.load_asset(asset_path)
mel = unreal.MaterialEditingLibrary
num_exprs = mel.get_num_material_expressions(material)

# 모든 Parameter Expression 타입 수집
all_param_types = []
for attr in dir(unreal):
    if "Parameter" in attr and "MaterialExpression" in attr:
        cls = getattr(unreal, attr, None)
        if cls is not None:
            all_param_types.append(cls)

targets = []
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
            continue
        match = re.match(r'^(\d+)(_.+)$', group)
        if match:
            num = int(match.group(1))
            suffix = match.group(2)
            # 아직 시프트 안 된 02_ 이하 찾기 (이미 시프트된 건 03_ 이상)
            if num >= 2 and num <= 12:
                targets.append((num, suffix, expr, param_name, group, class_name))

targets.sort(key=lambda x: x[0], reverse=True)

modified = 0
for num, suffix, expr, param_name, old_group, cls_name in targets:
    new_group = f"{num + 1:02d}{suffix}"
    if old_group != new_group:
        expr.set_editor_property("group", new_group)
        print(f"  {param_name} [{cls_name}]: {old_group} -> {new_group}")
        modified += 1

if modified > 0:
    unreal.EditorAssetLibrary.save_loaded_asset(material)
    print(f"\nFixed! {modified} missed parameters shifted")
else:
    print("No missed parameters found")

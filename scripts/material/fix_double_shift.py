"""
이중 시프트 수정 - 원래 6개 타입은 2번 시프트됨, -1 복구
StaticComponentMaskParameter는 1번만 시프트되어 정상 → 건드리지 않음
"""
import unreal
import re

asset_path = "/Game/Material/_define/FX/M_FX_01"
material = unreal.EditorAssetLibrary.load_asset(asset_path)
mel = unreal.MaterialEditingLibrary
num_exprs = mel.get_num_material_expressions(material)

# 이중 시프트된 6개 타입 (첫 번째 스크립트에서 이미 처리된 것들)
double_shifted_types = [
    unreal.MaterialExpressionScalarParameter,
    unreal.MaterialExpressionVectorParameter,
    unreal.MaterialExpressionStaticSwitchParameter,
    unreal.MaterialExpressionStaticBoolParameter,
    unreal.MaterialExpressionTextureSampleParameter2D,
    unreal.MaterialExpressionTextureObjectParameter,
]

targets = []
for cls in double_shifted_types:
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
            # 이중 시프트된 범위: 현재 04~13 (원래 02~11 → +1 → +1)
            # 13_AlphaComposite(원래 12→13)는 2번째에서 안 밀렸으므로 정상
            if num >= 4 and num <= 13:
                targets.append((num, suffix, expr, param_name, group, class_name))

# 높은 번호부터 -1
targets.sort(key=lambda x: x[0])

modified = 0
for num, suffix, expr, param_name, old_group, cls_name in targets:
    new_group = f"{num - 1:02d}{suffix}"
    expr.set_editor_property("group", new_group)
    print(f"  {param_name}: {old_group} -> {new_group}")
    modified += 1

if modified > 0:
    unreal.EditorAssetLibrary.save_loaded_asset(material)
    print(f"\nFixed! {modified} double-shifted parameters corrected")
else:
    print("No double-shifted parameters found")

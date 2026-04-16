"""
HTTP 전송용 - M_FX_01 머티리얼 그룹 넘버링 시프트
02_XXX → 03_XXX, 03_XXX → 04_XXX ... (02 이상 전부 +1)
find_object 방식으로 Expression 접근
"""
import unreal
import re

asset_path = "/Game/Material/_define/FX/M_FX_01"
material = unreal.EditorAssetLibrary.load_asset(asset_path)
mel = unreal.MaterialEditingLibrary
num_exprs = mel.get_num_material_expressions(material)

expr_classes = [
    unreal.MaterialExpressionScalarParameter,
    unreal.MaterialExpressionVectorParameter,
    unreal.MaterialExpressionStaticSwitchParameter,
    unreal.MaterialExpressionStaticBoolParameter,
    unreal.MaterialExpressionTextureSampleParameter2D,
    unreal.MaterialExpressionTextureObjectParameter,
]

targets = []

for expr_class in expr_classes:
    class_name = expr_class.__name__
    for i in range(200):
        obj_name = f"{class_name}_{i}"
        expr = unreal.find_object(material, obj_name)
        if expr is None:
            if i > num_exprs + 50:
                break
            continue
        try:
            group = expr.get_editor_property("group")
            param_name = expr.get_editor_property("parameter_name")
        except Exception:
            continue
        if not group:
            continue
        group = str(group)
        match = re.match(r'^(\d+)(_.+)$', group)
        if match:
            num = int(match.group(1))
            suffix = match.group(2)
            if num >= 2:
                targets.append((num, suffix, expr, param_name, group))

targets.sort(key=lambda x: x[0], reverse=True)

modified = 0
for num, suffix, expr, param_name, old_group in targets:
    new_group = f"{num + 1:02d}{suffix}"
    expr.set_editor_property("group", new_group)
    print(f"  {param_name}: {old_group} -> {new_group}")
    modified += 1

if modified > 0:
    unreal.EditorAssetLibrary.save_loaded_asset(material)
    print(f"\nDone! {modified} parameters shifted")
else:
    print("No targets found")

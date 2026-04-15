"""
[Step 2] M_FX_01 머티리얼 그룹 넘버링 시프트
02_XXX → 03_XXX, 03_XXX → 04_XXX ... (02 이상 전부 +1)
01_ 이하는 건드리지 않음

모든 MaterialExpression*Parameter 타입 자동 탐색
언리얼 에디터 Python 콘솔 또는 HTTP 서버를 통해 실행
"""
import unreal
import re

asset_path = "/Game/Material/_define/FX/M_FX_01"
material = unreal.EditorAssetLibrary.load_asset(asset_path)
mel = unreal.MaterialEditingLibrary

if not material:
    print("ERROR: cannot load " + asset_path)
else:
    num_exprs = mel.get_num_material_expressions(material)

    # 모든 Parameter Expression 타입 자동 수집
    all_param_types = []
    for attr in dir(unreal):
        if "Parameter" in attr and "MaterialExpression" in attr:
            cls = getattr(unreal, attr, None)
            if cls is not None:
                all_param_types.append(cls)

    # 변경 대상 수집
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
                if num >= 2:
                    targets.append((num, suffix, expr, param_name, group))

    # 높은 번호부터 처리 (역순, 충돌 방지)
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

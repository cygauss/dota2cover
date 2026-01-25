import vdf
import toml
import os

def apply_modifications(vdf_path, toml_path, output_path):
    # 检查文件是否存在
    if not os.path.exists(vdf_path):
        print(f"[错误] 未找到 VDF 文件: {vdf_path}")
        return
    if not os.path.exists(toml_path):
        print(f"[错误] 未找到 TOML 文件: {toml_path}")
        return

    # 1. 加载 VDF (保持顺序)
    print(f"正在读取 VDF: {vdf_path}...")
    with open(vdf_path, 'r', encoding='utf-8-sig') as f:
        data = vdf.load(f, mapper=vdf.VDFDict)

    # 2. 加载 TOML 配置
    print(f"正在读取 TOML 配置: {toml_path}...")
    try:
        with open(toml_path, 'r', encoding='utf-8') as f:
            config = toml.load(f)
    except Exception as e:
        print(f"[TOML 错误] 配置文件格式有误: {e}")
        return

    if 'changes' not in config:
        print("TOML 中未找到 'changes' 节点。")
        return

    # 3. 执行修改
    for change in config['changes']:
        path_str = change.get('path', '')
        raw_content = change.get('content', '')
        keys = path_str.strip('/').split('/')
        
        # 解析子 VDF 内容，确保强制换行防止第一行解析失败
        try:
            wrapped_vdf = f'"temp"\n{{\n{raw_content.strip()}\n}}'
            new_value = vdf.loads(wrapped_vdf)['temp']
            
            # 调试信息
            first_key = list(new_value.keys())[0] if new_value else "EMPTY"
            print(f"[解析成功] 路径: {path_str} | 首项: {first_key}")
        except Exception as e:
            print(f"[解析失败] {path_str} 的内容 VDF 语法有误: {e}")
            continue

        # 定位父节点
        curr = data
        found_parent = True
        for key in keys[:-1]:
            if key in curr:
                curr = curr[key]
            else:
                print(f"[跳过] 路径节点不存在: {key}")
                found_parent = False
                break
        
        # 执行原地替换
        if found_parent:
            target_key = keys[-1]
            if target_key in curr:
                # 核心逻辑：记录原始顺序并重排
                items_list = list(curr.items())
                target_idx = -1
                for i, (k, v) in enumerate(items_list):
                    if k == target_key:
                        target_idx = i
                        break
                
                if target_idx != -1:
                    items_list[target_idx] = (target_key, new_value)
                    curr.clear()
                    curr.update(items_list)
                    print(f"[成功] 已在原位更新: {path_str}")
            else:
                # 原本不存在则追加
                curr[target_key] = new_value
                print(f"[新增] 目标不存在，已追加至末尾: {path_str}")

    # 4. 保存文件
    print(f"正在保存至: {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        vdf.dump(data, f, pretty=True)
    print("完成！")

if __name__ == "__main__":
    apply_modifications(
        vdf_path='items_game.txt', 
        toml_path='config.toml', 
        output_path='items_game_mod.txt'
    )
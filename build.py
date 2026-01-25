import os
import vpk
import shutil
import subprocess

# --- 路径配置 ---
MOD_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_VPK = os.path.normpath(os.path.join(MOD_DIR, "..", "dota", "pak01_dir.vpk"))
TARGET_FILE_PATH = "scripts/items/items_game.txt"
MOD_SCRIPT = "modify.py"
MODDED_FILE = "items_game_mod.txt"
OUTPUT_VPK_NAME = "pak01_dir.vpk"
TEMP_ROOT = os.path.join(MOD_DIR, "temp_build")

def main():
    # 1. 解包原始文件
    print(f"[*] 正在从原始 VPK 提取: {TARGET_FILE_PATH}")
    if not os.path.exists(SOURCE_VPK):
        print(f"错误: 找不到原始 VPK 文件: {SOURCE_VPK}")
        return

    try:
        pak = vpk.open(SOURCE_VPK)
        file_data = pak.get_file(TARGET_FILE_PATH)
        with open(os.path.join(MOD_DIR, "items_game.txt"), "wb") as f:
            f.write(file_data.read())
        print("成功提取 items_game.txt")
    except Exception as e:
        print(f"解包失败: {e}")
        return

    # 2. 执行你的修改脚本 modify.py
    print(f"[*] 正在执行修改脚本: {MOD_SCRIPT}...")
    if os.path.exists(os.path.join(MOD_DIR, MOD_SCRIPT)):
        # 运行 modify.py，这应该会生成 items_game_mod.txt
        result = subprocess.run(["python", MOD_SCRIPT], cwd=MOD_DIR)
        if result.returncode != 0:
            print("错误: modify.py 执行失败")
            return
    else:
        print(f"错误: 找不到 {MOD_SCRIPT}")
        return

    # 3. 准备 VPK 打包目录结构
    print("[*] 正在准备打包目录结构...")
    # 创建目录: mod/temp_build/scripts/items/
    vpk_internal_dir = os.path.join(TEMP_ROOT, "scripts", "items")
    if os.path.exists(TEMP_ROOT):
        shutil.rmtree(TEMP_ROOT)
    os.makedirs(vpk_internal_dir)

    # 将生成的 items_game_mod.txt 重命名并移入
    modded_source = os.path.join(MOD_DIR, MODDED_FILE)
    if os.path.exists(modded_source):
        shutil.copy2(modded_source, os.path.join(vpk_internal_dir, "items_game.txt"))
    else:
        print(f"错误: modify.py 未生成 {MODDED_FILE}")
        return

    # 4. 生成新的 VPK
    print(f"[*] 正在生成新的 VPK: {OUTPUT_VPK_NAME}")
    try:
        new_vpk = vpk.new(TEMP_ROOT)
        new_vpk.save(os.path.join(MOD_DIR, OUTPUT_VPK_NAME))
        print("恭喜！打包成功完成。")
    except Exception as e:
        print(f"打包失败: {e}")
    finally:
        # 清理临时文件夹
        shutil.rmtree(TEMP_ROOT)

if __name__ == "__main__":
    main()
import os
import vpk
import shutil

# ================= 配置 =================
MOD_DIR = os.getcwd()
MODDED_FILE_NAME = "items_game_mod.txt"
TEMP_BUILD_DIR = os.path.join(MOD_DIR, "temp_vpk_root")
OUTPUT_VPK = "pak01_dir.vpk"
# ========================================

def pack():
    modded_file = os.path.join(MOD_DIR, MODDED_FILE_NAME)

    if not os.path.exists(modded_file):
        print(f"❌ 未找到 {MODDED_FILE_NAME}")
        return

    # 准备 VPK 内部目录结构
    vpk_internal_path = os.path.join(
        TEMP_BUILD_DIR, "scripts", "items"
    )

    if os.path.exists(TEMP_BUILD_DIR):
        shutil.rmtree(TEMP_BUILD_DIR)

    os.makedirs(vpk_internal_path)

    # 放入修改后的文件（重命名为 items_game.txt）
    shutil.copy2(
        modded_file,
        os.path.join(vpk_internal_path, "items_game.txt")
    )

    print("📁 已准备 VPK 目录结构")

    # 创建 VPK
    output_path = os.path.join(MOD_DIR, OUTPUT_VPK)
    print(f"📦 正在生成 VPK: {output_path}")

    new_vpk = vpk.new(TEMP_BUILD_DIR)
    new_vpk.save(output_path)

    # 清理临时目录
    shutil.rmtree(TEMP_BUILD_DIR)

    print("✅ 打包完成！")


if __name__ == "__main__":
    pack()

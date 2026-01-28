import os
import vpk

# ================= 配置 =================
MOD_DIR = os.getcwd()
VPK_PATH = os.path.join(MOD_DIR, "..", "dota", "pak01_dir.vpk")
TARGET_FILE_PATH = "scripts/items/items_game.txt"
OUTPUT_FILE = "items_game.txt"
# ========================================

def unpack():
    print(f"📦 正在从 VPK 解包: {TARGET_FILE_PATH}")
    print(f"VPK 路径: {VPK_PATH}")

    if not os.path.exists(VPK_PATH):
        print("❌ 找不到 pak01_dir.vpk，请检查路径")
        return

    try:
        pak = vpk.open(VPK_PATH)
        file_data = pak.get_file(TARGET_FILE_PATH)

        if file_data is None:
            print("❌ VPK 中未找到目标文件")
            return

        with open(os.path.join(MOD_DIR, OUTPUT_FILE), "wb") as f:
            f.write(file_data.read())

        print(f"✅ 解包成功: {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ 解包失败: {e}")


if __name__ == "__main__":
    unpack()

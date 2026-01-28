import vdf
import tomllib
from pathlib import Path
import re

# ================= 配置区 =================
INPUT_VDF = "game_settings.vdf"
OUTPUT_VDF = "game_settings_modified.vdf"
CONFIGS_DIR = "configs"
# ==========================================


def load_vdf_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_vdf(text: str) -> dict:
    return vdf.loads(text)


def find_block_range(text: str, key_path: list[str]) -> tuple[int, int] | None:
    """
    在原始 VDF 文本中定位某个 key 对应的 { ... } 块
    返回 (start, end) 的字符区间
    """
    pattern = r'"{}"\s*\{{'.format(key_path[-1])
    matches = list(re.finditer(pattern, text))
    if not matches:
        return None

    # 简单假设 key 唯一（游戏配置一般成立）
    start = matches[0].start()

    brace = 0
    i = matches[0].end()
    while i < len(text):
        if text[i] == "{":
            brace += 1
        elif text[i] == "}":
            if brace == 0:
                return start, i + 1
            brace -= 1
        i += 1

    return None


def apply_patch(text: str, key_path: str, vdf_fragment: str) -> str:
    keys = key_path.split(".")
    block = find_block_range(text, keys)
    if not block:
        raise ValueError(f"未找到路径: {key_path}")

    start, end = block

    replacement = f'"{keys[-1]}" {vdf_fragment}'
    return text[:start] + replacement + text[end:]


def merge_and_apply():
    original_text = load_vdf_text(INPUT_VDF)

    config_path = Path(CONFIGS_DIR)
    toml_files = sorted(config_path.glob("*.toml"))

    print(f"🔍 找到 {len(toml_files)} 个配置文件，开始应用")

    text = original_text

    for toml_file in toml_files:
        print(f"  -> 应用 {toml_file.name}")
        with open(toml_file, "rb") as f:
            config = tomllib.load(f)

        mods = config.get("modifications", {})
        for key_path, vdf_text in mods.items():
            try:
                text = apply_patch(text, key_path, vdf_text)
            except Exception as e:
                print(f"    ⚠️ {key_path} 失败: {e}")

    with open(OUTPUT_VDF, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\n✅ 完成！输出文件: {OUTPUT_VDF}")


if __name__ == "__main__":
    merge_and_apply()

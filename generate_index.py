import os
import json
import zipfile
import io
import tomllib

PLUGINS_SRC_DIR = "plugins"
POOL_DIR = "pool/main"
OUTPUT_JSON = "Packages.json"
MAGIC_HEADER = b'TWMP'
STANDARD_ZIP_HEADER = b'PK\x03\x04'

def build_and_archive_plugin(source_dir):
    toml_path = os.path.join(source_dir, "twmpxpem-project.toml")
    if not os.path.exists(toml_path):
        return None
        
    with open(toml_path, "rb") as f:
        config = tomllib.load(f)
        
    proj = config.get("project", {})
    pkg_name = proj.get("name")
    version = proj.get("version", "0.0.0")
    
    if not pkg_name:
        return None

    # 内存打包
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zf.write(file_path, arcname)
                
    # TWMP 加壳
    zip_data = zip_buffer.getvalue()
    if zip_data.startswith(STANDARD_ZIP_HEADER):
        final_wvwhl_data = MAGIC_HEADER + zip_data[4:]
    else:
        final_wvwhl_data = zip_data

    # 归档到 pool
    first_letter = pkg_name[0].lower() if pkg_name[0].isalpha() else "0"
    target_dir = os.path.join(POOL_DIR, first_letter, pkg_name)
    os.makedirs(target_dir, exist_ok=True)
    
    new_filename = f"{pkg_name}_{version}_all.wvwhl"
    target_path = os.path.join(target_dir, new_filename)
    
    with open(target_path, 'wb') as f:
        f.write(final_wvwhl_data)
        
    print(f"[+] 自动打包并加壳: {target_path}")
    return {
        "name": pkg_name,
        "version": version,
        "category": proj.get("category", "default"),
        "description": proj.get("description", "暂无描述"),
        "author": proj.get("author", "匿名开发者"),
        "filename": new_filename,
        "path": target_path.replace("\\", "/")
    }

def main():
    packages = []
    os.makedirs(POOL_DIR, exist_ok=True)
    os.makedirs(PLUGINS_SRC_DIR, exist_ok=True)

    for item in os.listdir(PLUGINS_SRC_DIR):
        source_dir = os.path.join(PLUGINS_SRC_DIR, item)
        if os.path.isdir(source_dir):
            pkg_info = build_and_archive_plugin(source_dir)
            if pkg_info:
                packages.append(pkg_info)
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"packages": packages}, f, indent=4, ensure_ascii=False)
    print(f"✅ 成功生成 {OUTPUT_JSON}，共收录 {len(packages)} 个插件。")

if __name__ == "__main__":
    main()

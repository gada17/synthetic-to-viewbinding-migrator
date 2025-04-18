import getpass
import os
import re
import pathlib
from openai import OpenAI
import xml.etree.ElementTree as ET


# === INTERACTIVE CONFIG ===
print("\n🔧 Kotlin Fragment ViewBinding Converter\n")

default_root = str(pathlib.Path.cwd())
default_converted = str(pathlib.Path.cwd())

ROOT_DIR = input(f"📁 Enter project root directory [{default_root}]: ").strip() or default_root

CONVERTED_DIR = pathlib.Path(ROOT_DIR) / "converted"
print(f"Converted directory {CONVERTED_DIR}")

ROOT_DIR = pathlib.Path(ROOT_DIR) / "app" / "src" / "main" 

MODE = input("⚙️  Choose mode: [overwrite / skip_existing] (default: skip_existing): ").strip().lower() or "skip_existing"
if not os.path.exists(ROOT_DIR):
    print("❌ Invalid root directory path!")
    exit(1)

# === OPENAI CONFIG ===
print("\n📘 To use this tool, you'll need an OpenAI API key.")
print("🔗 Get it here: https://platform.openai.com/account/api-keys")
print("\n⚠️ IMPORTANT:")
print(" - Do NOT share your API key with anyone.")
print(" - Treat it like a password. Anyone with your key can access your OpenAI account.")
print(" - If exposed, you can revoke it anytime and create a new one.")
print("\n🔒 When you paste your key below, it will NOT be shown on the screen for your safety.\n")
print("   (Note: some terminals may momentarily show pasted input — be cautious in public or recorded screens.)\n")

openai_api_key = getpass.getpass("🔐 Enter your OpenAI API key: ")

if not openai_api_key.startswith("sk-"):
    print("❌ Invalid API key format. It should start with 'sk-'.")
    exit(1)

MODEL_NAME = "gpt-4-turbo"
client = OpenAI(api_key=openai_api_key)

# === UTILS ===
def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def find_dirs(root_dir):
    src_dir = None
    layout_dir = None
    for root, dirs, _ in os.walk(root_dir):
        if 'java' in dirs:
            src_dir = os.path.join(root, 'java')
        if 'res' in dirs:
            layout_dir = os.path.join(root, 'res', 'layout')
        if src_dir and layout_dir:
            break
    return src_dir, layout_dir

def get_layout_file_for_fragment(content):
    # Find all synthetic imports like: import kotlinx.android.synthetic.main.layout_name.*
    synthetic_imports = re.findall(r'import\s+kotlinx\.android\.synthetic\.main\.([a-zA-Z0-9_]+)\..*', content)

    # Remove duplicates just in case
    layout_names = list(set(synthetic_imports))
   
    return layout_names  # list of layout names this fragment uses

def get_all_fragments(src_dir):
    fragment_map = {}
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".kt"):
                path = os.path.join(root, file)
                content = read_file(path)
                if not content or 'kotlinx.android.synthetic' not in content:
                    continue
                class_match = re.search(r'class\s+(\w+)', content)
                parent_match = re.search(r'class\s+\w+\s*:\s*([\w<>]+)', content)

                if class_match:
                    class_name = class_match.group(1)
                    parent = parent_match.group(1) if parent_match else None
                    layout_names = get_layout_file_for_fragment(content)
                    fragment_map[class_name] = {
                        "path": path,
                        "content": content,
                        "layout_names": layout_names,
                        "parent": parent
                    }
                    
    return fragment_map

def build_fragment_hierarchy(fragment_map):
    # Find the hierarchy from the target fragment upwards to BaseFragment
    hierarchy = []
    while class_name and class_name in fragment_map:
        data = fragment_map[class_name]
        hierarchy.insert(0, (class_name, data["path"], data["content"], data["layout_names"], data["parent"]))
        class_name = data["parent"]
    return hierarchy

def get_layout_code(layout_dir, layout_name):
    if layout_name:
        layout_file = os.path.join(layout_dir, f"{layout_name}.xml")
        return read_file(layout_file)
    return None

def extract_layout_includes(layout_name, layout_code):
    includes = []
    try:
        root = ET.fromstring(layout_code)
        for include in root.findall(".//include"):
            layout_file = include.attrib.get("layout", "").replace("@layout/", "")
            layout_id = include.attrib.get("{http://schemas.android.com/apk/res/android}id", "")
            if layout_file and layout_id:
                id_clean = layout_id.replace("@+id/", "").replace("@id/", "")
                includes.append((layout_file, id_clean))
    except ET.ParseError:
        pass
    return includes

def collect_layouts_recursively(layout_name, layout_dir, visited=None):
    if visited is None:
        visited = set()

    collected = []
    if layout_name in visited:
        return collected  # Prevent circular includes

    visited.add(layout_name)

    layout_code = get_layout_code(layout_dir, layout_name)
    if layout_code:
        collected.append((layout_name, layout_code))
        includes = re.findall(r'<include[^>]*layout="@layout/([^"]+)"', layout_code)
        for include in includes:
            collected += collect_layouts_recursively(include, layout_dir, visited)

    return collected

def build_layout_relations(layouts_data):
    relations = {}
    for name, code in layouts_data:
        includes = extract_layout_includes(name, code)
        if includes:
            relations[name] = includes
    if not relations:
        return ""

    rel_txt = "The layout relationships are as follows:\n"
    for parent, includes in relations.items():
        rel_txt += f"{parent}.xml includes:\n"
        for included, view_id in includes:
            rel_txt += f"- {included}.xml (as @{view_id})\n"
        rel_txt += "\n"
    return rel_txt

import re

def collect_layout_relations(layout_name, layout_dir, visited=None):
    if visited is None:
        visited = set()

    relations = {}
    if layout_name in visited:
        return relations

    visited.add(layout_name)

    layout_code = get_layout_code(layout_dir, layout_name)
    if layout_code:
        includes = []
        for match in re.finditer(r'<include[^>]*>', layout_code):
            tag = match.group()
            layout_match = re.search(r'layout="@layout/([^"]+)"', tag)
            id_match = re.search(r'android:id="@\+id/([^"]+)"', tag)
            if layout_match and id_match:
                includes.append((layout_match.group(1), id_match.group(1)))

        relations[layout_name] = includes

        for include_name, _ in includes:
            relations.update(collect_layout_relations(include_name, layout_dir, visited))

    return relations


def format_layout_relations(layout_relations):
    output = "The layout relationships are as follows:\n"
    for layout, includes in layout_relations.items():
        if includes:
            output += f"{layout}.xml includes:\n"
            for include, include_id in includes:
                output += f"- {include}.xml (as @+id/{include_id})\n"
    return output


def call_chatgpt_for_hierarchy(hierarchy, layout_dir):
    from collections import defaultdict

    fragments_by_file = defaultdict(list)
    layouts = []
    used_layout_names = set()

    # Group all fragments by the .kt file they came from
    for class_name, path, content, layout_names, _ in hierarchy:
        fragments_by_file[path].append(content)
        for layout_name in layout_names:
            used_layout_names.add(layout_name)

    # Build fragment source blocks per file
    fragments = []
    for path, fragment_contents in fragments_by_file.items():
        combined_content = "\n\n".join(fragment_contents)
        print(os.path.basename(path))
        fragments.append(f"📄 Fragment file: {os.path.basename(path)}\n--- KOTLIN ---\n{combined_content}")

    # Recursively collect all included layouts
    visited_layouts = set()
    all_layouts = set(used_layout_names)
    for layout_name in used_layout_names:
        included = collect_layouts_recursively(layout_name, layout_dir, visited_layouts)
        all_layouts.update(name for name, _ in included)
        for name, code in included:
            # print(f"{name}.xml")
            layouts.append(f"🗾 Layout file: {name}.xml\n--- XML ---\n{code}")

    # Collect layout relationships
    layout_relations = {}
    for layout_name in used_layout_names:
        layout_relations.update(collect_layout_relations(layout_name, layout_dir))

    layout_relations_text = format_layout_relations(layout_relations)
    
    user_msg = (
         "Convert the following Kotlin Fragments to use ViewBinding. Replace all synthetic imports and access views properly.\n\n"
         + layout_relations_text
         + "\n\n"
         + "\n\n".join(fragments)
         + "\n\n"
         + "\n\n".join(layouts)
         + "\n\nReturn only the updated Kotlin code."
    )

    response = client.chat.completions.create(
         model=MODEL_NAME,
         messages=[{"role": "system", "content": (
             "You are a Kotlin Android expert helping convert Fragments using synthetic imports to ViewBinding. Do not import any synthetic syntax. "+

             "When a layout is included using the `<include>` tag, its views should be accessed through the corresponding binding property generated for that included layout (e.g., `binding.includedLayoutId.viewId`)."+ 

             "To reference the entire included layout view (e.g., for visibility, click listeners), use `binding.includedLayoutId.root`."+

             "Only access views directly from the root binding if they are declared in the root layout itself."+

             "Do not prefix child view IDs with the layout name unless it is included. Use `android:id` attributes in XML to ensure the include tag generates a binding field."+

             "Avoid adding any explanations — return only the updated Kotlin code."

         )},
         {"role": "user", "content": user_msg}],
         temperature=0.3
    )
    return response.choices[0].message.content


def clean_chatgpt_response(raw_response: str) -> str:
    cleaned = re.sub(r"^```kotlin\\s*", "", raw_response)
    cleaned = re.sub(r"\\s*```$", "", cleaned)

    lines = cleaned.strip().splitlines()
    start_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith(("package", "import", "class", "object", "@", "fun", "val", "var")):
            start_index = i
            break
    lines = lines[start_index:]

    end_index = len(lines) - 1
    for i in reversed(range(len(lines))):
        if '}' in lines[i]:
            end_index = i + 1
            break
    lines = lines[:end_index]

    return "\n".join(lines)

def save_output(hierarchy, converted_code):
    for class_name, path, *_ in hierarchy:
        relative_path = os.path.relpath(path, ROOT_DIR)
        converted_path = os.path.join(CONVERTED_DIR, relative_path)

        os.makedirs(os.path.dirname(converted_path), exist_ok=True)
        with open(converted_path, 'w', encoding='utf-8') as f:
            f.write(converted_code)
        print(f"✅ Saved: {converted_path}")

# === MAIN ===
src_dir, layout_dir = find_dirs(ROOT_DIR)

# === MAIN ===
src_dir, layout_dir = find_dirs(ROOT_DIR)

if src_dir and layout_dir:
    fragment_map = get_all_fragments(src_dir)
    
    # Creating all_fragments as a list of tuples
    all_fragments = [
        (class_name, data['path'], data['content'], data['layout_names'], data['parent'])
        for class_name, data in fragment_map.items() if data['layout_names']
    ]

    if all_fragments:
        total_fragments = len(all_fragments)
        print("\n🚧 Preparing fragments and layouts for conversion...")

        for i in range(total_fragments):
            class_name, path, content, layout_names, parent = all_fragments[i]

            # Build the same converted path used in save_output
            relative_path = os.path.relpath(path, ROOT_DIR)
            converted_path = os.path.join(CONVERTED_DIR, relative_path)

            # Skip conversion if file already exists and MODE is skip_existing
            if MODE == "skip_existing" and os.path.exists(converted_path):
               print(f"⏩ Skipping {class_name} (already converted at {converted_path})")
               continue

            print(f"⚙️  Converting fragment {i+1}/{total_fragments}: {class_name}")
            raw_result = call_chatgpt_for_hierarchy([all_fragments[i]], layout_dir)
            print("✅ Conversion complete. Saving output...")

            cleaned_result = clean_chatgpt_response(raw_result)
            save_output([all_fragments[i]], cleaned_result)

        print("✅ All Conversion complete.")
    else:
       print("⚠️ No fragments with layout names found. Nothing to convert.")


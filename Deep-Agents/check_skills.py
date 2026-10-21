
from pathlib import Path
import re
import yaml

root = Path(__file__).resolve().parent / "skills"

for folder in ["aws", "langgraph", "python", "report-generator"]:
    path = root / folder / "SKILL.md"
    print(f"\n--- {path} ---")

    if not path.exists():
        print("ERROR: File does not exist")
        continue

    content = path.read_text(encoding="utf-8-sig")
    print("File begins with:", repr(content[:100]))

    match = re.match(
        r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n",
        content,
        re.DOTALL,
    )

    if not match:
        print("FAIL: YAML frontmatter is not at the beginning")
        continue

    try:
        metadata = yaml.safe_load(match.group(1))
        print("Parsed metadata:", metadata)

        if not isinstance(metadata, dict):
            print("FAIL: Metadata must be a YAML mapping")
            continue

        print("Name:", metadata.get("name"))
        print("Description:", metadata.get("description"))

    except yaml.YAMLError as exc:
        print("FAIL: Invalid YAML:", exc)

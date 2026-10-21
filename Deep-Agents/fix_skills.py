
from pathlib import Path

skills_dir = Path(__file__).resolve().parent / "skills"

skill_names = [
    "aws",
    "langgraph",
    "python",
    "report-generator",
]

for name in skill_names:
    file_path = skills_dir / name / "SKILL.md"

    if not file_path.exists():
        print(f"NOT FOUND: {file_path}")
        continue

    # Remove leading blank lines and UTF-8 BOM
    content = file_path.read_text(encoding="utf-8-sig")
    content = content.lstrip("\r\n \t")

    # Ensure the YAML frontmatter starts at character zero
    if not content.startswith("---\n") and not content.startswith("---\r\n"):
        print(f"ERROR: Missing frontmatter in {name}")
        continue

    file_path.write_text(content, encoding="utf-8")
    print(f"FIXED: {name}/SKILL.md")

print("\nDone. Now run: python check_skills.py")

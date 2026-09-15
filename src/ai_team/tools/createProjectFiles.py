from pathlib import Path
import shutil

from langchain_core.tools import tool


OUTPUT_DIR = Path("./Output")


@tool
def create_project_files(files: list[dict[str, str]], clean_output: bool = True) -> str:
    """Create the generated project files inside the repository Output directory."""
    if clean_output and OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    created_files: list[str] = []
    output_root = OUTPUT_DIR.resolve()

    for file in files:
        relative_path = Path(file["path"])
        file_path = (output_root / relative_path).resolve()
        if file_path != output_root and output_root not in file_path.parents:
            raise ValueError(f"File path escapes the Output directory: {relative_path}")

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file["code"], encoding="utf-8")
        created_files.append(str(file_path.relative_to(output_root)))

    return f"Created {len(created_files)} files in {output_root}: {', '.join(created_files)}"
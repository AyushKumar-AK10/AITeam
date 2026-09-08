from .graph import graph
import json
from pathlib import Path
import shutil

def main() -> None:
    result = graph.graph.invoke({"userReq": "Create a website to play handcricket. The website will show buttons to play the game and will show the score of the game. The website will have a home page, a game page, and a score page. The home page will have a button to start the game. The game page will have buttons to play the game and will show the score of the game. The score page will show the final score of the game. I want the code to be written in HTML, CSS, and JavaScript. The code should be well structured and organized. The code should be well commented. The code should be easy to understand and modify. The code should be responsive and work on all devices. The code should be optimized for performance. The code should follow best practices and coding standards. The code should be secure and protect against common vulnerabilities. The code should be tested and debugged."})
    parsed_response = json.loads(result['developerResponse'].content)
    files = parsed_response['response']

    ## Delete the Output folder if it exists
    folder = Path("./Output")
    if folder.exists():
        shutil.rmtree(folder)
        print("Output folder deleted")

    print(f'The number of files generated: {len(files)}')
    for file in files:
    # Build the complete file path
        file_path = Path("./Output") / file["path"]

        # Create the parent folder + all required subfolders
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create the file and write the generated code
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file["code"])
        print(f"Created: {file_path.resolve()}")

if __name__ == "__main__":
    main()
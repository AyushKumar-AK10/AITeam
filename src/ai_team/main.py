from .graph import graph
from dotenv import load_dotenv

def main() -> None:
    request = {"userReq": "Create a basic College attendance management system using HTML,CSS, javascript and local sqllite for storage"}

    for update in graph.graph.stream(request, stream_mode="updates"):
        for node_name, node_update in update.items():
            print(f"[{node_name}]")

            if node_name != "toolNode":
                continue

            for message in node_update.get("messages", []):
                print(message.content)

if __name__ == "__main__":
    load_dotenv()
    main()
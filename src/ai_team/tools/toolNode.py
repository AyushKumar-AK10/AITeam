import json
from pathlib import Path

from langchain_core.messages import HumanMessage

from .executeTerminal import run_terminal
from .createProjectFiles import create_project_files


def tool_node(state):
	"""Create the developer's files, then validate the generated project."""
	developer_response = json.loads(state["developerResponse"].content)
	attempts = state.get("toolAttempts", 0) + 1
	file_result = create_project_files.invoke({
		"files": developer_response["response"],
		"clean_output": attempts == 1,
	})

	output_dir = Path("./Output")
	if (output_dir / "package.json").exists():
			command = (
				"cd Output && npm install && npm run build --if-present && "
				"(lsof -ti tcp:3000 | xargs kill 2>/dev/null || true; "
				"nohup npm start > /tmp/ai-team-project.log 2>&1 & "
				"echo $! > /tmp/ai-team-project.pid; "
				"curl --retry 20 --retry-delay 1 --retry-connrefused -fsS "
				"http://127.0.0.1:3000 >/dev/null 2>/tmp/ai-team-health.log; "
				"health_code=$?; "
				"if [ $health_code -ne 0 ]; then cat /tmp/ai-team-health.log; fi; "
				"echo PROJECT_URL=http://localhost:3000; exit $health_code)"
			)
	else:
			command = (
				"cd Output && "
				"(lsof -ti tcp:3000 | xargs kill 2>/dev/null || true; "
				"nohup python3 -m http.server 3000 > /tmp/ai-team-project.log 2>&1 & "
				"echo $! > /tmp/ai-team-project.pid; "
				"curl --retry 20 --retry-delay 1 --retry-connrefused -fsS "
				"http://127.0.0.1:3000 >/dev/null 2>/tmp/ai-team-health.log; "
				"health_code=$?; "
				"if [ $health_code -ne 0 ]; then cat /tmp/ai-team-health.log; fi; "
				"echo PROJECT_URL=http://localhost:3000; exit $health_code)"
			)

	terminal_result = run_terminal(command)
	return {
		"toolAttempts": attempts,
		"messages": [
			HumanMessage(
				content=(
					f"{file_result}\n"
					f"Terminal execution report:\n{terminal_result}"
				)
			)
		]
	}


def tool_result_condition(state):
	"""Retry development after a failed validation, up to three attempts."""
	latest_message = state["messages"][-1].content
	if "STATUS: FAILED" in latest_message and state.get("toolAttempts", 0) < 3:
		return "retry"
	return "done"

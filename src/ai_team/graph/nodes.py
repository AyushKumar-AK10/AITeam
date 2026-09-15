from langchain_core.messages import HumanMessage, SystemMessage
from .state import State
from ..models import gemini
from ..config import baPrompt
from ..config import architectPrompt
from ..config import devPrompt


def baNode(state: State):
    userReq = state['userReq']
    prompt = SystemMessage(content=baPrompt.prompt)
    userMessage = HumanMessage(content=userReq)
    response = gemini.llm.invoke([prompt, userMessage])
    return {
        "baResponse": HumanMessage(content=response.content),
    }

def architectNode(state: State):
    prompt = SystemMessage(content=architectPrompt.prompt)
    response = gemini.llm.invoke([prompt, state['baResponse']])
    return {
        "architectResponse": HumanMessage(content=response.content),
        "messages":[HumanMessage(content=response.content)]
    }

def developerNode(state: State):
    prompt = SystemMessage(content=devPrompt.prompt)
    messages = [state["architectResponse"]]
    if state.get("toolAttempts", 0) > 0:
        messages.append(state["messages"][-1])

    response = gemini.dev_llm.invoke([prompt, *messages])
    response_content = response.model_dump_json()
    return {
        "developerResponse": HumanMessage(content=response_content),
    }

from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage

class State(MessagesState):
    userReq : str
    baResponse :HumanMessage
    architectResponse : HumanMessage
    developerResponse : HumanMessage
    testerResponse : HumanMessage


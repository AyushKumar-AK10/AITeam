from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from .output import DevOutputList
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)


dev_llm = llm.with_structured_output(DevOutputList)
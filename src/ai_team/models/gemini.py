from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from .output import DevOutputList
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)


dev_llm = llm.with_structured_output(DevOutputList)
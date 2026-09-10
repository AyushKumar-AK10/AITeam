from fastapi import FastAPI
from pydantic import BaseModel
from .graph import graph
import json

class InputFormat(BaseModel):
    description: str

api = FastAPI()

@api.post("/generate")
async def generate_project(inputData: InputFormat):
    description = inputData.description
    result = graph.graph.invoke({"userReq": description})
    parsed_response = json.loads(result['developerResponse'].content)
    files = parsed_response['response']
    return files

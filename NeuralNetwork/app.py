import os
import uvicorn
from process import mainProcess
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://0.0.0.0:3333"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.post("/execute")
def execute():
    #手寫辨識
    result_array = mainProcess()
    response = {'trueNum': int(result_array[1]), 'predictNum': int(result_array[0]), 'index': int(result_array[2]), 'predictResult': int(result_array[3])}
    # response = {'test': 'Money'}
    return JSONResponse(content=response)

class image_model(BaseModel):
    index: Union[int, None] = None

#刪除圖片
@app.post("/deleteImage")
def deleteImage(model: image_model):
    index = str(model.index)
    image_path = '/app/img/num_' + index + '.png'
    if os.path.isfile(image_path):
        os.remove(image_path)

    return index

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=5000)
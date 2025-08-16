from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import process_image
import data
import os
from dotenv import load_dotenv
load_dotenv()
import uvicorn
app = FastAPI()
HOST = os.getenv("host")
PORT = os.getenv("port")

@app.post("/car/api/")
async def get_car_number_plate(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image provided")

    if image.filename == "":
        raise HTTPException(status_code=400, detail="No selected file")

    nummerplade = process_image.test(image.file)
    retrun_data = await data.exstract_data(nummerplade)

    return retrun_data

if __name__ == "__main__":
    print(HOST)
    uvicorn.run("app:app", host=HOST, port=int(PORT), reload=True)

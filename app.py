from insurancePrice.logger import logging
import sys
from insurancePrice.exception import InsuranceException

from fastapi import FastAPI, Request
from typing import Optional
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from insurancePrice.utils.main_utils import MainUtils

from insurancePrice.components.model_predictor import CostPredictor, insuranceData
from insurancePrice.constants import APP_HOST, APP_PORT
from insurancePrice.pipeline.training_pipeline import TrainPipeline


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
Data Form
"""
class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.age: Optional[str] = None
        self.sex: Optional[str] = None
        self.bmi: Optional[str] = None
        self.children: Optional[str] = None
        self.smoker: Optional[str] = None
        self.region: Optional[str] = None

    async def get_shipping_data(self):
        form = await self.request.form()
        self.age = form.get("age")
        self.sex = form.get("sex")
        self.bmi = form.get("bmi")
        self.children = form.get("children")
        self.smoker = form.get("smoker")
        self.region = form.get("region")



"""
train route
"""

@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")
    


@app.get("/predict")
async def predictGetRouteClient(request: Request):
    try:
        
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "context": "Rendering"},
        )

    except Exception as e:
        return Response(f"Error Occurred! {e}")



@app.post("/predict")
async def predictRouteClient(request: Request):
    try:

        form = DataForm(request)
        await form.get_shipping_data()

        shipping_data = insuranceData(
            age=form.age,
            sex=form.sex,
            bmi=form.bmi,
            children=form.children,
            smoker=form.smoker,
            region=form.region,   
        )

        cost_df = shipping_data.get_input_data_frame()
        cost_predictor = CostPredictor()
        cost_value = round(cost_predictor.predict(X=cost_df)[0], 2)

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "context": cost_value},
        )


    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)

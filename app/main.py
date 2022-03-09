from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from google.cloud import storage
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/prices")
def read_prices():
    sheet_id = "1DMq3BXT-GCerZiKhkBGvXn_nuJ8cRd-ZP8HrqPiiEc4"
    sheet_name = "prices"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    data = pd.read_csv(url)
    return data.to_dict(orient="records")

@app.get("/images")
def read_images():
    storage_client = storage.Client()
    bucket_name = "studio-huit-images"
    blobs = storage_client.list_blobs(bucket_name, prefix="Nouveau Test")
    images = [blob.name for blob in blobs if blob.name[-1] != "/"]
    
    return [f"https://storage.googleapis.com/studio-huit-images/{urllib.parse.quote(image)}" for image in images]
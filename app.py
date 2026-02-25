import torch
import torch.nn.functional as F
from fastapi import FastAPI
import joblib
import asyncio
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pydantic import BaseModel
from huggingface_hub import snapshot_download
import os

def download_model_folder():
    if not os.path.exists("ecommerce-classification-model") or not os.listdir("ecommerce-classification-model"):
        print("Chưa có thư mục chứa model, tiến hành tải thư mục ...")
        snapshot_download(
            repo_id="VietAnh-1027/ecommerce-classification-model",
            repo_type="model"
        )
        print("Tải thư mục thành công!")
    else:
        print("Đã có thư mục chứa model")

download_model_folder()
app = FastAPI(title="Hệ thống phân loại danh mục hàng hóa")

le = joblib.load(os.path.join("ecommerce-classification-model", "label_encoder.pkl"))
classes = le.classes_
tokenizer = AutoTokenizer.from_pretrained("ecommerce-classification-model")
model = AutoModelForSequenceClassification.from_pretrained("ecommerce-classification-model")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

class Information(BaseModel):
    user: str
    text: str

def classify_categorical(text):
    tokens = tokenizer(text, return_tensors='pt', padding="max_length", max_length=128, truncation=True).to(device)
    outputs = model(**tokens)
    probabilites = F.softmax(outputs.logits, dim=1)
    confidence, cls_id = torch.max(probabilites, dim=1)
    return round(confidence.item()*100, 2) , cls_id

@app.post("/predict")
async def predict(request: Information):
    conf_score, cls_id = await asyncio.to_thread(classify_categorical, request.text)
    return {
        "user": request.user,
        "category": classes[cls_id],
        "confidence": f"{conf_score}%"
    }
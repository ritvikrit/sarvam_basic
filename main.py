from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from sarvamai import SarvamAI
from dotenv import load_dotenv
import os
import base64

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI()

# -----------------------------
# Initialize Sarvam Client
# -----------------------------
client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)

# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "Sarvam Voice Assistant Running"}

# -----------------------------
# Text To Speech Route
# -----------------------------
from fastapi.responses import FileResponse

@app.post("/tts")
async def text_to_speech(data: dict):

    text = data.get("text")

    response = client.text_to_speech.convert(
        text=text,
        target_language_code="en-IN",
        speaker="priya",
        model="bulbul:v3"
    )

    audio_base64 = response.audios[0]

    with open("output.wav", "wb") as f:
        f.write(base64.b64decode(audio_base64))

    return FileResponse(
        "output.wav",
        media_type="audio/wav"
    )

# -----------------------------
# Speech To Text Route
# -----------------------------
@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):

    with open(file.filename, "wb") as f:
        f.write(await file.read())

    with open(file.filename, "rb") as audio_file:

        response = client.speech_to_text.transcribe(
            file=audio_file,
            model="saaras:v3"
        )

    return JSONResponse(content=response.dict())
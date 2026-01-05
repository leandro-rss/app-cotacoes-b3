from fastapi import FastAPI
from app.routes.cotacoes import router as cotacoes_router

app = FastAPI(
    title="API de Cotações",
    description="API para consulta de cotações da B3 com cache",
    version="1.0.0"
)

app.include_router(cotacoes_router)

@app.get("/")
def status():
    return {"status": "API rodando 🚀"}


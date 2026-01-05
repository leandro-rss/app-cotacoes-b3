from fastapi import APIRouter, Query
from app.services.cotacoes_service import obter_cotacoes

router = APIRouter(
    prefix="/cotacoes",
    tags=["Cotações"]
)

@router.get(
    "/",
    summary="Consultar cotações de ações",
    description="""
Consulta uma ou mais ações da B3.

🔹 Informe os ativos separados por vírgula  
🔹 Exemplo: PETR4,VALE3,ITUB4  
🔹 Os dados possuem atraso aproximado de 15 minutos
"""
)
def cotacoes(
    ativos: str = Query(
        ...,
        description="Lista de ativos separados por vírgula",
        examples={
            "exemplo": {
                "summary": "Exemplo padrão",
                "value": "PETR4,VALE3,ITUB4"
            }
        }
    )
):
    return obter_cotacoes(ativos)

from app.services.cotacoes_service import (
    obter_cotacoes,
    obter_cotacao_unica
)

@router.get(
    "/{ativo}",
    summary="Consultar cotação de uma ação",
    description="""
Consulta a cotação de um único ativo da B3.

📌 Exemplo:
- /cotacoes/PETR4
""",
)
def cotacao_unica(ativo: str):
    return obter_cotacao_unica(ativo)

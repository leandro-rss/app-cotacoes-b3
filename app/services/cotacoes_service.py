import time
import requests
from datetime import datetime

CACHE = {}
CACHE_TTL = 60  # segundos

def _get_cache(chave: str):
    registro = CACHE.get(chave)

    if not registro:
        return None

    dados, timestamp = registro

    if time.time() - timestamp > CACHE_TTL:
        del CACHE[chave]
        return None

    return dados


def _set_cache(chave: str, dados):
    CACHE[chave] = (dados, time.time())


def _normalizar_chave(valor: str) -> str:
    return valor.upper().strip()


API_URL = "https://brapi.dev/api/quote"

def _formatar_ativo(ativo: dict):
    timestamp = ativo.get("regularMarketTime")

    horario = (
        datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
        if isinstance(timestamp, (int, float))
        else "Horário indisponível"
    )

    return {
        "ativo": ativo.get("symbol"),
        "preco": f"R$ {ativo.get('regularMarketPrice'):,.2f}"
                 .replace(",", "X").replace(".", ",").replace("X", "."),
        "variacao": f"{ativo.get('regularMarketChangePercent'):+.2f}%",
        "minimo_dia": f"R$ {ativo.get('regularMarketDayLow'):,.2f}",
        "maximo_dia": f"R$ {ativo.get('regularMarketDayHigh'):,.2f}",
        "horario": horario,
        "observacao": "Cotação com atraso (≈15 minutos)"
    }


def obter_cotacoes(ativos: str):
    lista = ativos.split(",")
    resultados = []

    for ticker in lista:
        chave = _normalizar_chave(ticker)

        # 1️⃣ tenta cache
        cache = _get_cache(chave)
        if cache:
            resultados.append({
                **cache,
                "observacao": "Cotação em cache (≈60s)"
            })
            continue

        # 2️⃣ chama API
        response = requests.get(f"{API_URL}/{chave}", timeout=10)
        response.raise_for_status()

        dados = response.json().get("results")
        if not dados:
            continue

        resultado = _formatar_ativo(dados[0])

        # 3️⃣ salva no cache
        _set_cache(chave, resultado)

        resultados.append(resultado)

    return resultados


def obter_cotacao_unica(ticker: str):
    chave = _normalizar_chave(ticker)

    # 1️⃣ tenta cache
    cache = _get_cache(chave)
    if cache:
        return {
            **cache,
            "observacao": "Cotação em cache (≈60s)"
        }

    # 2️⃣ chama API
    response = requests.get(f"{API_URL}/{chave}", timeout=10)
    response.raise_for_status()

    dados = response.json().get("results")
    if not dados:
        return {"erro": "Ativo não encontrado"}

    resultado = _formatar_ativo(dados[0])

    # 3️⃣ salva no cache
    _set_cache(chave, resultado)

    return resultado




import httpx

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "llama3"

async def query_llama(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )
        data = response.json()
        return data.get("response", "[No response]")

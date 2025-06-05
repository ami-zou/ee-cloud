import requests
import os
import time

BASE_IP = os.getenv("EDGE_SERVER_IP", "localhost")
API = f"http://{BASE_IP}:8000"
OLLAMA = f"http://{BASE_IP}:11434"

def check_llama():
    print("🔍 Checking Llama...")
    resp = requests.post(
        f"{OLLAMA}/api/generate",
        headers={"Content-Type": "application/json"},
        json={"model": "llama3", "prompt": "Hello", "stream": False}
    )
    print(f"Llama status: {resp.status_code}")
    print(resp.text)
    return resp.ok

def check_health():
    print("🔍 Checking /health...")
    r1 = requests.get(f"{API}/health")
    r2 = requests.get(f"{API}/health/ollama")
    print(f"/health: {r1.status_code} -> {r1.text}")
    print(f"/health/ollama: {r2.status_code} -> {r2.text}")
    return r1.ok and r2.ok

def check_chat():
    print("🧠 Testing /chat...")
    resp = requests.post(
        f"{API}/chat",
        headers={"Content-Type": "application/json"},
        json={"prompt": "What is Edge Esmeralda?"}
    )
    print(f"/chat: {resp.status_code} -> {resp.text}")
    return resp.ok

def check_whisper():
    print("🎙️ Submitting fake audio file to /submit-whisper...")
    with open("test.txt", "w") as f:
        f.write("This is a test file pretending to be audio.")

    with open("test.txt", "rb") as f:
        resp = requests.post(
            f"{API}/submit-whisper",
            files={"audio_file": f}
        )
    print(f"/submit-whisper: {resp.status_code} -> {resp.text}")
    return resp.ok

if __name__ == "__main__":
    print(f"🚀 Starting tests against: {BASE_IP}")
    time.sleep(1)

    all_passed = (
        check_llama() and
        check_health() and
        check_chat() and
        check_whisper()
    )

    print("\n✅ All tests passed!" if all_passed else "\n❌ Some tests failed.")
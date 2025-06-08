# Edge Esmeralda Cloud
Mini cloud for [Edge Esmeralda 2025](https://www.edgeesmeralda.com) Solar-powered edge data center project

## Startup instructions for local development (macOS)
1. Install Brew, then install python

2. Set up python environment in `/cloud`
```
chmod +x setup_env.sh
./setup_env.sh
```
  or download dependencies directly 
```
pip install -r requirements.txt
```

3. Run the development server in `/cloud` directory with:
```
   source .venv/bin/activate && uvicorn main:app --reload
```

4. Run Llama
Run `docker compose up` at root directly. Or run it separately:

Run docker Llama (recommended): 
```
docker volume create ollama-data
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama-data:/root/.ollama \
  ollama/ollama
```
```
docker exec -it ollama ollama pull llama3
```
Once ready, Llama is up at `http://localhost:11434`

or Install Llama on MacOS
```
brew install ollama
ollama pull llama3
ollama run llama3
```

### Testing
In `/test`, run `python test_endpoints.py`

Manual testing: 
Query either `localhost` or `<edge-server-ip>`
1. Ensure Llama is running: 
```
curl http://<edge-server-ip>:11434/api/generate \
  -d '{
    "model": "llama3",
    "prompt": "Hello",
    "stream": true
  }' \
  -H "Content-Type: application/json"
```
and DeepSeek
```
curl http://localhost:11434/api/generate \
  -d '{
    "model": "deepseek-r1:7b",
    "prompt": "Hello",
    "stream": true
  }' \
  -H "Content-Type: application/json"
```
2. Ensure server is up & healthy:
```
curl http://localhost:8000/health
```

```
curl http://localhost:8000/health/ollama
```

2. Prompting `chat` API:
```
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello?"}'
```

2. Check submit whisper job from `test` directory:
```
curl -X POST "http://<edge-server-ip>:8000/submit-whisper" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@test.txt"
```

### Development notes
- Update dependencies with `pip freeze > requirements.txt`

- Build and push docker image in `/cloud`
```
docker build -t azou2020/ee-cloud:latest .
docker push azou2020/ee-cloud:latest
```

## Physical server (linux) deployment
0. Connect to the server via Tailscale & Cloudfare tunnel

1. Install Docker
```
sudo apt install docker.io
```

2. Run Llama
Run docker Llama (recommended): 
```
docker volume create ollama-data
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama-data:/root/.ollama \
  ollama/ollama
```

```
docker exec -it ollama ollama pull llama3
```
Once ready, Llama is up at `http://localhost:11434`

Or install Llama:
```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
ollama run llama3
```

### Exposing physical server
- Port 11434 is open on firewall, or use Cloudfare tunnel
- Public IP is reachable
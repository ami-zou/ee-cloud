# Edge Esmeralda Cloud
Mini cloud for [Edge Esmeralda 2025](https://www.edgeesmeralda.com) Solar-powered edge data center project

## Startup instructions for local development (macOS)
1. Install Brew, then install python

2. Set up python environment
```
chmod +x setup_env.sh
./setup_env.sh
```
  or download dependencies directly 
```
pip install -r requirements.txt
```

3. Run the development server in root directory with:
```
   source .venv/bin/activate && uvicorn cloud.main:app --reload
```

4. Run Llama
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
Query either `localhost` or `<edge-server-ip>`
1. Ensure Llama is running: 
```
curl http://<edge-server-ip>:11434/api/generate \
  -d '{
    "model": "llama3",
    "prompt": "What is Edge Esmeralda?",
    "stream": false
  }' \
  -H "Content-Type: application/json"
```
```
curl http://localhost:8000/health/ollama
```

2. Prompting `chat` API:
```
curl -X POST http://<edge-server-ip>:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Edge Esmeralda?"}'
```

2. Check submit whisper job from `test` directory:
```
curl -X POST "http://<edge-server-ip>:8000/submit-whisper" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@test.txt"
```

### Other notes
- Update dependencies with `pip freeze > requirements.txt`

## Physical server (linux) deployment
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
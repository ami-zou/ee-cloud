# Edge Esmeralda Cloud
Mini cloud for [Edge Esmeralda 2025](https://www.edgeesmeralda.com) Solar-powered edge data center project

## Startup instructions 
1. Install Python

2. Set up python environment
```
chmod +x setup_env.sh
./setup_env.sh
```
or 
```
pip install -r requirements.txt
```

3. Run the development server in `/cloud` with:
```
   source .venv/bin/activate && uvicorn main:app --reload
```

4. Submit a request from `/tests`
```
curl -X POST "http://127.0.0.1:8000/submit-whisper" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@test.txt"
```
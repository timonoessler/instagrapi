# instagrapi
Service to upload content to Instagram using username and password

### 1. Venv erstellen und anschließend wie folgt aktivieren:
```bash
source venv/bin/activate
```

Danach requirements.txt installieren. <br>
```bash    
pip install -r requirements.txt
`````
### 2. Starte Flask-Server
```bash
python src/main.py
```

### 3. Testen der API via Curl

#### Beispiel für den Upload eines Fotos:

```bash
curl -X POST http://127.0.0.1:58769/instapush \
     -H "Authorization: Bearer <your-static-jwt-token>" \
     -F "username=<your-instagram-username>" \
     -F "password=<your-instagram-password>" \
     -F "type=photo" \
     -F "caption=This is a test upload" \
     -F "file=@/path/to/image.jpg"
```

#### Beispiel für den Upload eines Videos:

```bash
curl -X POST http://127.0.0.1:58769/instapush \
     -H "Authorization: Bearer <your-static-jwt-token>" \
     -F "username=<your-instagram-username>" \
     -F "password=<your-instagram-password>" \
     -F "type=video" \
     -F "caption=This is a test video upload" \
     -F "file=@/path/to/video.mp4" \
     -F "thumbnail=@/path/to/thumbnail.jpg"
```
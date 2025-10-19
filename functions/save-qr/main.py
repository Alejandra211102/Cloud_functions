import io, time, os, qrcode
from flask import make_response
from google.cloud import storage

BUCKET_NAME = os.environ.get("BUCKET_NAME")

def _corsify(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

def save_qr(request):
    if request.method == "OPTIONS":
        return _corsify(make_response("", 204))
    try:
        if not BUCKET_NAME:
            return _corsify(make_response({"success": False, "error": "BUCKET_NAME no configurado"}, 500))

        data = request.get_json(silent=True) or {}
        text = data.get("text")
        uid = data.get("uid", "anon")
        if not text:
            return _corsify(make_response({"success": False, "error": "Campo 'text' es requerido."}, 400))

        img = qrcode.make(text)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        ts = int(time.time())
        object_name = f"qr/{uid}/qr_{ts}.png"

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(object_name)
        blob.upload_from_file(buf, content_type="image/png")

        blob.make_public()  # DEMO
        return _corsify(make_response({"success": True, "url": blob.public_url, "object_name": object_name}, 200))
    except Exception as e:
        return _corsify(make_response({"success": False, "error": str(e)}, 500))

import os
from flask import make_response
from google.cloud import storage

BUCKET_NAME = os.environ.get("BUCKET_NAME")

def _corsify(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

def get_qr_list(request):
    # Preflight CORS
    if request.method == "OPTIONS":
        return _corsify(make_response("", 204))

    try:
        # Validar variable de entorno
        if not BUCKET_NAME:
            return _corsify(make_response({"success": False, "error": "BUCKET_NAME no configurado"}, 500))

        # Obtener uid (por defecto 'anon')
        uid = request.args.get("uid", "anon")
        prefix = f"qr/{uid}/"

        # Conectar con Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)

        # Listar blobs bajo el prefijo del usuario
        items = []
        for blob in bucket.list_blobs(prefix=prefix):
            # Para la demo hacemos públicos los objetos.
            # En producción usa Signed URLs para seguridad.
            try:
                blob.make_public()
            except Exception:
                # Si ya era público o no se puede, seguimos igual
                pass

            items.append({
                "name": blob.name,
                "url": blob.public_url,
                "size": blob.size
            })

        return _corsify(make_response({"success": True, "items": items}, 200))

    except Exception as e:
        return _corsify(make_response({"success": False, "error": str(e)}, 500))

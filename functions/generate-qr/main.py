import base64, io, qrcode
from flask import make_response

def _corsify(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

def generate_qr(request):
    if request.method == "OPTIONS":
        return _corsify(make_response("", 204))
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text")
        as_base64 = bool(data.get("as_base64", True))
        if not text or not isinstance(text, str):
            return _corsify(make_response({"success": False, "error": "Campo 'text' es requerido."}, 400))

        img = qrcode.make(text)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        if as_base64:
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            return _corsify(make_response({"success": True, "mime": "image/png", "data_base64": b64}, 200))

        resp = make_response(buf.getvalue())
        resp.headers["Content-Type"] = "image/png"
        return _corsify(resp)
    except Exception as e:
        return _corsify(make_response({"success": False, "error": str(e)}, 500))

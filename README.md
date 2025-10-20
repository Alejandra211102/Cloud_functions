# 🌩️ Cloud Functions Project — Generador de Códigos QR (Serverless App)

Este proyecto demuestra cómo construir una **aplicación Serverless** en **Google Cloud Functions**, que genera, guarda y lista **códigos QR** sin administrar servidores.  
Se implementó usando **Python 3.11** y los servicios **Cloud Functions (Gen 2)** y **Cloud Storage**.

---

## 🧠 Objetivo General

Desarrollar y desplegar una aplicación web basada en funciones **Serverless**, demostrando los beneficios del modelo **FaaS (Function as a Service)**:  
- Escalado automático  
- Pago por ejecución  
- Despliegue rápido y sin gestión de servidores  

---

## ⚙️ Tecnologías utilizadas

| Categoría | Tecnología |
|------------|-------------|
| Lenguaje | **Python 3.11** |
| Cloud Provider | **Google Cloud Platform** |
| Backend | **Google Cloud Functions (Gen 2)** |
| Almacenamiento | **Google Cloud Storage** |
| Librerías | `qrcode`, `flask`, `google-cloud-storage`, `functions-framework` |
| Pruebas | **PowerShell / cURL / navegador** |
| Control de versiones | **Git + GitHub** |
| Frontend opcional | HTML / CSS / JS |

---

## 🧩 Arquitectura de la aplicación

```text
Frontend Web (HTML/JS)
       ↓
Cloud Function 1: generate-qr
       ↓
Cloud Function 2: save-qr
       ↓
Google Cloud Storage (Bucket)
       ↓
Cloud Function 3: get-qr-list

```
| Función         | Descripción                                                | Endpoint                                                                                                                                       |
| --------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **generate-qr** | Genera un código QR desde un texto enviado por el usuario. | [https://us-central1-actividad-cloud-qr.cloudfunctions.net/generate-qr](https://us-central1-actividad-cloud-qr.cloudfunctions.net/generate-qr) |
| **save-qr**     | Guarda el QR generado en un bucket de Cloud Storage.       | [https://us-central1-actividad-cloud-qr.cloudfunctions.net/save-qr](https://us-central1-actividad-cloud-qr.cloudfunctions.net/save-qr)         |
| **get-qr-list** | Lista los QRs almacenados por usuario desde Cloud Storage. | [https://us-central1-actividad-cloud-qr.cloudfunctions.net/get-qr-list](https://us-central1-actividad-cloud-qr.cloudfunctions.net/get-qr-list) |


## 🚀 Despliegue de funciones en Google Cloud Functions 

Ejecuta los siguientes comandos para desplegar cada función en la región `us-central1` usando **Python 3.11**.

### 1️⃣ Generar código QR
```bash
gcloud functions deploy generate-qr \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=functions/generate-qr \
  --entry-point=generate_qr \
  --trigger-http \
  --allow-unauthenticated
```
### 2️⃣ Guardar código QR en Cloud Storage
```bash
gcloud functions deploy save-qr \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=functions/save-qr \
  --entry-point=save_qr \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars=BUCKET_NAME=qr-assets-actividad-cloud-qr
```
### 3️⃣ Obtener lista de códigos QR
```bash
gcloud functions deploy get-qr-list \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=functions/get-qr-list \
  --entry-point=get_qr_list \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars=BUCKET_NAME=qr-assets-actividad-cloud-qr
```

### ✅ Pruebas realizadas

🧩 Función 1 — generate-qr
$body = @{ text = "https://davita.com"; as_base64 = $false } | ConvertTo-Json
Invoke-WebRequest -Method POST -Uri "https://us-central1-actividad-cloud-qr.cloudfunctions.net/generate-qr" -ContentType "application/json" -Body $body -OutFile "qr_test.png"
ii .\qr_test.png

💾 Función 2 — save-qr
$body = @{ text = "Hola Mundo desde Serverless"; uid = "lenovo" } | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri "https://us-central1-actividad-cloud-qr.cloudfunctions.net/save-qr" -ContentType "application/json" -Body $body

📂 Función 3 — get-qr-list
Invoke-RestMethod -Method GET -Uri "https://us-central1-actividad-cloud-qr.cloudfunctions.net/get-qr-list?uid=lenovo"

✔️ Devuelve un JSON con los archivos almacenados:
{
  "success": true,
  "items": [
    {
      "name": "qr/lenovo/qr_1729362104.png",
      "url": "https://storage.googleapis.com/qr-assets-actividad-cloud-qr/qr/lenovo/qr_1729362104.png",
      "size": 1240
    }
  ]
}


⚠️ Errores comunes y solución
| Error                                 | Causa                                    | Solución                                               |
| ------------------------------------- | ---------------------------------------- | ------------------------------------------------------ |
| `Billing account not found`           | El proyecto no tenía facturación activa  | Activar billing en la consola de Google Cloud          |
| `missing permissions: serviceAccount` | IAM sin permisos propagados              | Esperar unos minutos o reasignar la cuenta de servicio |
| `entryPoint not found`                | El nombre de la función no coincide      | Corregir `--entry-point` al nombre real en `main.py`   |
| `CORS policy error`                   | Falta configuración de CORS en el bucket | Aplicar `gsutil cors set cors.json gs://<BUCKET>`      |

💡 Ventajas del modelo Serverless observadas

Escalado automático: las funciones crecen o bajan en capacidad según la demanda.

Pago por uso: solo se cobra cuando la función se ejecuta.

Despliegue instantáneo: cada cambio se publica con un solo comando.

Integración nativa: Cloud Storage, IAM y otros servicios funcionan sin configuraciones extra.

Sin mantenimiento de servidores: Google Cloud administra la infraestructura.

🧪 Resultados

Se generaron y almacenaron múltiples códigos QR.

Todos los endpoints respondieron correctamente con estructuras JSON.

El bucket qr-assets-actividad-cloud-qr contiene los archivos creados.

Se verificó acceso público a las imágenes generadas.

🧭 Conclusiones

La arquitectura Serverless demostró ser una solución práctica y escalable para construir microservicios ligeros.
Con Google Cloud Functions se logra implementar un backend funcional sin servidores dedicados, reduciendo costos y complejidad.
El uso combinado de Cloud Storage y Cloud Functions permitió crear un flujo completo de generación, persistencia y consulta de datos con alto rendimiento y mínimo mantenimiento.

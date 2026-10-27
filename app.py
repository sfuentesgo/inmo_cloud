import time
import threading
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulación de Base de Datos en memoria
BASE_DE_DATOS = [
    {"id": 1, "titulo": "Apartamento en Usaquén", "precio": 350000000, "ciudad": "Bogotá"},
    {"id": 2, "titulo": "Casa campestre en Chía", "precio": 650000000, "ciudad": "Chía"}
]

# Simulación de Memoria Caché (Patrón Cache-Aside)
CACHE_MEMORIA = {}

def tarea_optimizar_imagenes(inmueble_id, nombre_archivo):
    """Simula el procesamiento en segundo plano (Worker)"""
    print(f"[WORKER] Iniciando optimización de: {nombre_archivo} para el inmueble {inmueble_id}...")
    time.sleep(5)  # Simula el trabajo pesado de cambiar tamaño de imágenes
    print(f"[WORKER] Imagen {nombre_archivo} optimizada y almacenada con éxito.")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "proyecto": "CompuVivienda - Prototipo Arquitectónico",
        "estado": "Operativo en la Nube",
        "patrones_implementados": [
            "Cache-Aside Pattern (/inmuebles)",
            "Queue / Background Worker Pattern (/inmuebles/publicar)"
        ]
    })

# DEMOSTRACIÓN PATRÓN: Cache-Aside
@app.route("/inmuebles", methods=["GET"])
def obtener_inmuebles():
    clave_cache = "listado_inmuebles"
    
    # 1. Verifica si ya está en caché
    if clave_cache in CACHE_MEMORIA:
        return jsonify({
            "origen": "MEMORIA CACHÉ (Cache Hit - Respuesta rápida)",
            "datos": CACHE_MEMORIA[clave_cache]
        }), 200

    # 2. Si no existe, simula latencia de consulta pesada a Base de Datos
    time.sleep(1.5)
    datos = BASE_DE_DATOS
    
    # 3. Guarda copia en caché para futuras peticiones
    CACHE_MEMORIA[clave_cache] = datos
    return jsonify({
        "origen": "BASE DE DATOS (Cache Miss - Consultado en disco y guardado en caché)",
        "datos": datos
    }), 200

# DEMOSTRACIÓN PATRÓN: Desacoplamiento / Asíncrono
@app.route("/inmuebles/publicar", methods=["POST"])
def publicar_inmueble():
    body = request.get_json() or {}
    titulo = body.get("titulo", "Inmueble de prueba")
    precio = body.get("precio", 200000000)
    imagen = body.get("imagen", "fachada.jpg")
    
    nuevo_id = len(BASE_DE_DATOS) + 1
    nuevo_inmueble = {"id": nuevo_id, "titulo": titulo, "precio": precio, "ciudad": "Bogotá"}
    BASE_DE_DATOS.append(nuevo_inmueble)
    
    # Invalida la caché para que el listado se refresque
    CACHE_MEMORIA.pop("listado_inmuebles", None)

    # Lanza la tarea pesada en segundo plano sin congelar al usuario
    hilo = threading.Thread(target=tarea_optimizar_imagenes, args=(nuevo_id, imagen))
    hilo.start()

    # Responde de inmediato (menos de 1 segundo)
    return jsonify({
        "mensaje": "Publicación registrada con éxito",
        "inmueble_id": nuevo_id,
        "estado_multimedia": "Procesamiento encolado en segundo plano"
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
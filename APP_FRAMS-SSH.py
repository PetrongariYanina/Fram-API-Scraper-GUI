import requests
import urllib3
from urllib.parse import urljoin
import os
import sys
import time
import random

#---------------------------------------
def resource_path(relative_path):
    """
    Obtiene la ruta absoluta de un recurso
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        # Si no se está ejecutando como ejecutable, la base es el directorio actual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- USO DE LA FUNCIÓN PARA EL CERTIFICADO ---
# Usamos esta función para obtener la ruta correcta en cualquier PC

            #Certificado oculto 

#---------------------------------------

# --- CONFIGURACIÓN ---

destinos_ids = {
    "Agadir": "1831", 
    "Senegal": "1610",
    "Fuerteventura": "1766",
    "Gran Canaria": "1764",
    "Lanzarote": "1763",
    "Tenerife": "1765",
    "Andalucía": "1767",
    "Baleares": "1773",
    "Ibiza": "1777",
    "Mallorca": "1774",
    "Menorca": "1775",
    "Marruecos": "1835"
}

ciudad_salida_dict = {
    "París": "1188",
    "Lyon": "1026",
    "Marsella": "1102",
    "Niza": "1138",
    "Toulouse": "1462",
    "Burdeos": "555",
    "Nantes": "1153",
    "Estrasburgo": "1435",
    "Lille": "988"
}

def buscar_hoteles_riu_api(destino_id, ciudad_id, fecha_salida, log_callback=None):
    
    # Permitir un callback para informar progreso (útil para GUI) usa print
    if log_callback is None:
        log_callback = print
    url_api = "https://www.fram.fr/api/ajax/search"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json" 
    }

    resultados = []
    
    # Probamos las primeras 6 páginas
    for pagina in range(1, 7):
        log_callback(f"📡 Consultando web FRAM - Página {pagina}...")

        params = {

            "departureCityIds": ciudad_id, #por api
            "destinationsZones": destino_id, #por url
            "activeEngineType": "voyage",
            "durationRangeMax": "99",
            "durationRangeMin": "0",
            "departureDate": fecha_salida,
            "flexi": "90",
            "themespace": "sejour-voyage",
            "pageNumber": pagina,
            "typeMoteur": "voyage"
        }

        try:
            # Retraso aleatorio entre 1 y 5 segundos para evitar peticiones demasiado seguidas
            time.sleep(random.uniform(1, 5))
            # Petición GET usando params
            response = requests.get(url_api, params=params, headers=headers, verify=CERTIFICADO_CA_EMPACADO)
            
            if response.status_code != 200:
                log_callback(f"⚠ Error en la API: {response.status_code}")
                break

            # 1. CONVERTIR RESPUESTA A JSON
            data = response.json()
            
            # lista de hoteles dentro del JSON
            lista_hoteles = data.get('items', []) 
            
            # Si la lista está vacía, es que se acabaron los resultados
            if not lista_hoteles:
                log_callback(f"   -> No hay más resultados. Página {pagina} no existe.")
                break

            # 2. ITERAR RESULTADOS
            posicion_local = 0
            for hotel in lista_hoteles:
                posicion_local += 1
                
                # Extraer datos del diccionario JSON
                title = hotel.get('alt', '').strip()
                link_relativo = hotel.get('url', '') 
                
                # Filtro RIU
                if "riu" in title.lower():
                    full_link = f"https://www.fram.fr{link_relativo}"
                    precio = hotel.get('minPrice', 'N/A')
                    resultados.append({
                        "titulo": title,
                        "url": full_link,
                        "posicion": posicion_local,
                        "pagina": pagina,
                        "precio": precio
                    })
                    # Informar progreso mediante el callback
                    try:
                        log_callback(f"✓ {title} | Precio: {precio} | Pág: {pagina} | Pos: {posicion_local}")
                    except Exception:
                        pass

        except Exception as e:
            log_callback(f"Error procesando página {pagina}: {e}")
            break

    return resultados

if __name__ == "__main__":
    # EJEMPLO DE USO 
    fecha = "30/01/2026"
    ciudad_nombre = "Lyon"
    destino_nombre = "Agadir"

    # Verificar si tenemos el ID
    if destino_nombre in destinos_ids and ciudad_nombre in ciudad_salida_dict:
        id_destino = destinos_ids[destino_nombre]
        id_ciudad = ciudad_salida_dict[ciudad_nombre]

        print(f"--- Iniciando búsqueda para {destino_nombre} desde {ciudad_nombre} en fecha {fecha} ---")

        hoteles_encontrados = buscar_hoteles_riu_api(id_destino, id_ciudad, fecha)

        # Guardar resultados en archivo txt en carpeta Web_FRAM
        safe_fecha = fecha.replace('/', '-')
        downloads_dir = "Web_FRAM"
        os.makedirs(downloads_dir, exist_ok=True)
        filename = os.path.join(downloads_dir, f"Web_FRAM_{destino_nombre}_{ciudad_nombre}_{safe_fecha}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"--- Búsqueda para {destino_nombre} desde {ciudad_nombre} en fecha {fecha} ---\n\n")
            f.write("=== RESULTADOS RIU ENCONTRADOS ===\n\n")
            if hoteles_encontrados:
                for h in hoteles_encontrados:
                    f.write(f"✓ {h['titulo']}\n")
                    f.write(f"  Precio: {h['precio']} | Pág: {h['pagina']} | Pos: {h['posicion']}\n")
                    f.write(f"  Link: {h['url']}\n\n")
            else:
                f.write("No se encontraron hoteles RIU.\n")

        print(f"\n✓ Resultados guardados en '{filename}'")
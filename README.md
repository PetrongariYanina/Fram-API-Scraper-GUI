# 🏨 Hotel Availability Monitor (FRAM & RIU)

> Una herramienta de escritorio eficiente y respetuosa para monitorizar el posicionamiento y disponibilidad de productos hoteleros en la web de partners.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

## 📋 Descripción

Este proyecto es una herramienta diseñada para facilitar la auditoría diaria de posicionamiento de hoteles (específicamente la cadena RIU) dentro del portal de viajes **FRAM**.

El objetivo es automatizar la búsqueda manual para verificar si los hoteles aparecen correctamente listados, en qué posición y a qué precio, permitiendo al equipo comercial reaccionar rápidamente ante discrepancias o falta de disponibilidad.

### ✨ Características Principales

* **🚀 Consumo Inteligente de API:** En lugar de realizar *web scraping* tradicional (parseando HTML pesado), la herramienta consulta directamente la API interna (`/api/ajax/search`), lo que la hace más rápida y ligera.
* **🛡️ Navegación "Educada":** Incluye retardos aleatorios (`random delays`) entre peticiones para no saturar el servidor del cliente y simular comportamiento humano.
* **🖥️ Interfaz Gráfica (GUI):** Construida con `Tkinter` (asistida por IA) para que cualquier miembro del equipo, independientemente de sus conocimientos técnicos, pueda usarla.
* **📂 Exportación de Datos:** Genera reportes automáticos en `.txt` organizados por destino y fecha en la carpeta `Web_FRAM`.
* **🧵 Multihilo:** La interfaz no se congela durante la búsqueda gracias a la implementación de `threading`.

## 🛠️ Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
    cd TU_REPOSITORIO
    ```

2.  **Instalar dependencias:**
    El proyecto utiliza librerías estándar de Python, pero requiere `requests`.
    ```bash
    pip install requests
    ```

3.  **Certificados SSL (Importante):**
    El script está configurado para manejar certificados personalizados (`.pem`). Asegúrate de tener el certificado necesario en la raíz o ajustar la ruta en el código si tu entorno de red lo requiere.

## 🚀 Uso

Puedes ejecutar el script directamente con Python:

```bash
python APP_FRAM_tk.py

```

1.  Selecciona el **Destino** (ej. Agadir, Tenerife).
2.  Selecciona la **Ciudad de Salida** (ej. París, Lyon).
3.  Introduce la **Fecha de viaje** (DD/MM/YYYY).
4.  Haz clic en **Ejecutar**.

Los resultados se mostrarán en la ventana de log y se guardarán automáticamente en un archivo de texto.

## 📦 Crear Ejecutable (.exe)

Si deseas distribuir esta herramienta a compañeros que no tienen Python instalado, puedes generar un ejecutable *standalone* usando **PyInstaller**.

**Comando de compilación:**

```bash
pyinstaller.exe --onefile --noconsole --add-data "APP_FRAMS-SSH.py;." "APP_FRAM_tk.py" --icon=icon.ico --name="Scrap-FRAM"


```
Nota: Asegúrate de tener un archivo icon.ico y el certificado .pem en la carpeta antes de compilar.

## ⚙️ Estructura del Proyecto
APP_FRAM_tk.py: Contiene la lógica de la interfaz gráfica (Frontend).

APP_FRAMS-SSH.py: Contiene la lógica de conexión con la API y procesamiento de datos (Backend/Scraper).

## 🤝 Contribución
Este es un proyecto de código abierto para uso interno y educativo. Las sugerencias para mejorar la eficiencia del código o la UI son bienvenidas.

## ⚠️ Disclaimer
Esta herramienta ha sido creada con fines de productividad interna y análisis de mercado legítimo. Úsala de manera responsable. No reduzcas los tiempos de espera (sleep) para evitar causar carga innecesaria en los servidores de terceros.

---
*Desarrollado con ❤️ y un poco de ayuda de IA.*

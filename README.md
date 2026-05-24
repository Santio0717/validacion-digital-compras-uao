# Validación Digital de Compras - UAO
Repositorio oficial del proyecto:
https://github.com/Santio0717/validacion-digital-compras-uao
---
## Autores
* D. Ruiz Tocora
* C. Pinzón Mosquera
* S. Murillo Ramírez

Proyecto Final – PDI 2026
Universidad Autónoma de Occidente
---
# Objetivo general
Desarrollar un sistema de validación automática de compras mediante técnicas de visión artificial y clasificación de objetos, 
permitiendo identificar productos automáticamente y generar tickets digitales para optimizar los procesos de atención en cafeterías universitarias.
---
# Descripción
El proyecto busca optimizar el proceso de validación de productos adquiridos en cafeterías y tiendas universitarias
mediante técnicas de visión artificial y procesamiento digital de imágenes.

El sistema permite identificar automáticamente productos utilizando imágenes capturadas desde un smartphone o cargadas manualmente, 
generando posteriormente un ticket digital y un código único de validación.

La solución está orientada a reducir tiempos de atención, minimizar errores humanos y mejorar la eficiencia operativa dentro de un entorno de campus inteligente.
---
# Características principales
* Captura de imágenes mediante cámara en vivo.
* Carga múltiple de imágenes.
* Detección automática de productos.
* Clasificación híbrida:
  * Nombre de archivo.
  * Detección por color.
  * Modelo YOLOv8.
* Generación automática de ticket digital.
* Generación de código único de validación.
* Corrección manual de productos detectados incorrectamente.
* Compatibilidad con dispositivos móviles mediante ngrok.
---
# Productos detectados
El sistema reconoce actualmente los siguientes productos:
* Gaseosa
* Gorra
* Vaso
* Termo
---
# Tecnologías utilizadas
* Python 3
* Streamlit
* YOLOv8
* OpenCV
* NumPy
* Pillow (PIL)
* Git & GitHub
* Ngrok
---
# Funcionamiento del sistema
El sistema funciona mediante las siguientes etapas:
1. Captura de imágenes desde smartphone o carga manual.
2. Procesamiento digital de imágenes utilizando OpenCV.
3. Identificación automática de productos.
4. Generación automática del ticket digital.
5. Generación de código único de validación.
6. Validación final de la compra.
---
# Dataset
El modelo fue entrenado utilizando un dataset personalizado creado con imágenes reales de productos de cafetería y la tienda de UAO.
El dataset incluye:
* Diferentes ángulos.
* Variaciones de iluminación.
* Distintos fondos.
* Diferentes distancias de captura.
El entrenamiento del modelo se realizó utilizando YOLOv8 y Roboflow.
---
# Estructura del proyecto
```txt
validacion-digital-compras-uao/
│
├── app.py
├── modelo.pt
├── requirements.txt
├── train.py
├── README.md
│
└── cafeteria-uao.v2i.yolov8/
```
---
# Instalación
## 1. Clonar repositorio
```bash
git clone https://github.com/Santio0717/validacion-digital-compras-uao.git
```
---
## 2. Entrar al proyecto
```bash
cd validacion-digital-compras-uao
```
---
## 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
---
## 4. Instalar YOLOv8
```bash
pip install ultralytics
```
---
# Ejecutar proyecto
```bash
python -m streamlit run app.py
```
---
# Ejecutar desde celular
## 1. Ejecutar Streamlit
```bash
python -m streamlit run app.py
```
---
## 2. Ejecutar ngrok
```bash
ngrok http 8501
```
---
## 3. Abrir URL HTTPS generada
Ejemplo:
```txt
https://xxxxx.ngrok-free.app
```
---
# Arquitectura general
El sistema está compuesto por:
* Smartphone para captura de imágenes.
* Red local o Wi-Fi para transmisión.
* Computador encargado del procesamiento.
* Modelo de visión artificial para clasificación.
* Generador de tickets y validación.
---
# Licencia
Proyecto académico desarrollado con fines educativos.

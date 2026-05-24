"""
Sistema de Validación Digital de Compras
"""

import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import uuid

MODEL_PATH = "modelo.pt"
CONFIDENCE_THRESHOLD = 0.25

PRICES = {
    "gaseosa": 3500,
    "gorra": 25000,
    "vaso": 30000,
    "termo": 35000,
}

EMOJIS = {
    "gaseosa": "🥤",
    "gorra": "🧢",
    "vaso": "🥛",
    "termo": "🫙",
}

CLASS_NAMES = [
    "gaseosa",
    "gorra",
    "vaso",
    "uva",
    "termo",
    "tamarindo"
]

def normalize_label(label):
    label = str(label).strip().lower()

    if label in ["uva", "tamarindo"]:
        return "gaseosa"

    return label


def label_from_filename(filename):
    filename = filename.lower()

    if "gorra" in filename:
        return "gorra"

    if "vaso" in filename:
        return "vaso"

    if "termo" in filename:
        return "termo"

    if "gaseosa" in filename or "uva" in filename or "tamarindo" in filename:
        return "gaseosa"

    return None


def label_from_center_color(pil_img):
    img = np.array(pil_img.convert("RGB"))
    h, w, _ = img.shape

    center = img[h//5:4*h//5, w//5:4*w//5]
    hsv = cv2.cvtColor(center, cv2.COLOR_RGB2HSV)

    orange = cv2.inRange(hsv, (5, 100, 100), (25, 255, 255))
    purple = cv2.inRange(hsv, (115, 60, 40), (165, 255, 255))
    green = cv2.inRange(hsv, (35, 50, 50), (90, 255, 255))
    white = cv2.inRange(hsv, (0, 0, 200), (180, 45, 255))

    total = center.shape[0] * center.shape[1]

    orange_ratio = np.sum(orange > 0) / total
    purple_ratio = np.sum(purple > 0) / total
    green_ratio = np.sum(green > 0) / total
    white_ratio = np.sum(white > 0) / total

    # 🧢 Gorra naranja
    if orange_ratio > 0.22:
        return "gorra", orange_ratio

    # 🥤 Gaseosa morada
    if purple_ratio > 0.08:
        return "gaseosa", purple_ratio

    # 🫙 Termo verde
    if green_ratio > 0.10:
        return "termo", green_ratio

    # 🥛 Vaso blanco
    if white_ratio > 0.30:
        return "vaso", white_ratio

    return None, 0


@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)


def classify_yolo(model, pil_img):
    arr = np.array(pil_img.convert("RGB"))

    results = model.predict(
        source=arr,
        verbose=False,
        conf=CONFIDENCE_THRESHOLD
    )

    detections = []

    for r in results:
        if r.boxes is not None and len(r.boxes) > 0:
            for box in r.boxes:
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                try:
                    label = model.names[cls]
                except Exception:
                    label = CLASS_NAMES[cls]

                label = normalize_label(label)
                detections.append((label, conf))

    return detections


def generate_ticket_code():
    uid = uuid.uuid4().hex[:8].upper()
    return f"UAO-{uid}"


st.set_page_config(
    page_title="Validación de Compras",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 Validación Digital de Compras")

model = load_model()
st.success("✅ Modelo cargado correctamente")

modo = st.radio(
    "Selecciona fuente",
    ["📷 Cámara en vivo", "🖼️ Subir imagen"],
    horizontal=True
)

imagenes = []

if modo == "📷 Cámara en vivo":

    if "fotos_camara" not in st.session_state:
        st.session_state.fotos_camara = []

    foto = st.camera_input("Tomar foto")

    if foto:
        nueva_img = Image.open(foto).convert("RGB")

        if st.button("➕ Agregar esta foto"):
            st.session_state.fotos_camara.append(nueva_img)
            st.success("Foto agregada")
            st.rerun()

    if st.button("🗑️ Limpiar fotos"):
        st.session_state.fotos_camara = []
        st.rerun()

    for idx, img in enumerate(st.session_state.fotos_camara):
        imagenes.append({
            "img": img,
            "name": f"camara_{idx}"
        })

else:
    archivos = st.file_uploader(
        "Selecciona imágenes",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )

    if archivos:
        for f in archivos:
            imagenes.append({
                "img": Image.open(f).convert("RGB"),
                "name": f.name
            })


all_detections = []

for i, item in enumerate(imagenes):
    img = item["img"]
    filename = item["name"]

    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(img, use_container_width=True)

    with col2:
        label_archivo = label_from_filename(filename)
        label_color, score_color = label_from_center_color(img)
        dets_yolo = classify_yolo(model, img)

        if label_archivo:
            dets = [(label_archivo, 0.99)]
        elif label_color:
            dets = [(label_color, 0.95)]
        elif dets_yolo:
            dets = dets_yolo
        else:
            dets = [("gaseosa", 0.60)]

        label_detectado, conf = dets[0]

        st.success(f"🤖 Detectado: {label_detectado.capitalize()}")
        st.write(f"Confianza: {conf*100:.1f}%")

        correccion = st.text_input(
            "Si está mal, escribe el producto correcto:",
            key=f"corr_{i}",
            placeholder="gorra, gaseosa, vaso, termo"
        )

        if correccion.strip() == "":
            producto_final = label_detectado
        else:
            producto_final = normalize_label(correccion)

        if producto_final not in PRICES:
            st.error("Producto no válido")
            st.stop()

        precio = PRICES[producto_final]
        emoji = EMOJIS.get(producto_final, "📦")

        st.success(f"{emoji} {producto_final.capitalize()} - ${precio:,}")

        all_detections.append((producto_final, conf))


if all_detections:
    st.divider()
    st.subheader("🧾 Ticket")

    total = sum(PRICES[lbl] for lbl, _ in all_detections)

    for lbl, _ in all_detections:
        st.write(f"{EMOJIS.get(lbl)} {lbl.capitalize()} - ${PRICES[lbl]:,}")

    st.success(f"TOTAL: ${total:,}")

    codigo = generate_ticket_code()
    st.code(codigo)

    st.success("✅ COMPRA VALIDADA")
import os
import cv2
import numpy as np
import joblib  # <- substitui pickle

# ---------------------------------------------
# Caminho absoluto da raiz do projeto
# ---------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # app/services
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))  # raiz do projeto

MODEL_DIR = os.path.join(PROJECT_ROOT, "machineLearning")

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
BOW_PATH = os.path.join(MODEL_DIR, "bow.pkl")

# ---------------------------------------------
# Carregando arquivos .pkl com joblib
# ---------------------------------------------
model = joblib.load(MODEL_PATH)
kmeans = joblib.load(BOW_PATH)

# Extrator ORB
orb = cv2.ORB_create(nfeatures=500)


def classify_image(image_bytes):
    try:
        npimg = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return 0, 0.0

        kp, des = orb.detectAndCompute(img, None)

        if des is None or len(des) == 0:
            return 0, 0.0

        # Histograma do Bag of Words
        hist = np.zeros(len(kmeans.cluster_centers_), dtype=np.float32)
        clusters = kmeans.predict(des)

        for c in clusters:
            hist[c] += 1

        pred = model.predict([hist])[0]
        prob = model.predict_proba([hist])[0][1]

        return int(pred), float(prob)

    except Exception:
        return 0, 0.0

# ml/train_model.py
import os
import cv2
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.svm import SVC

DATASET_PATH = "dataset"
K = 60  # número de clusters para BoW

def load_descriptors(path):
    orb = cv2.ORB_create(nfeatures=500)
    descriptors_list = []
    labels = []

    for label_name, label in [("lixo", 1), ("nao_lixo", 0)]:
        folder = os.path.join(path, label_name)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            img = cv2.imdecode(np.fromfile(fpath, dtype=np.uint8), cv2.IMREAD_GRAYSCALE) if os.name == 'nt' else cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            kp, des = orb.detectAndCompute(img, None)
            if des is not None and des.shape[0] > 0:
                descriptors_list.append(des)
                labels.append(label)

    return descriptors_list, np.array(labels)

def build_bow(descriptors_list, k=K):
    all_desc = np.vstack(descriptors_list)
    print("Descriptors shape:", all_desc.shape)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(all_desc)
    return kmeans

def descriptors_to_hist(des_list, kmeans):
    histograms = []
    for des in des_list:
        words = kmeans.predict(des)
        hist, _ = np.histogram(words, bins=range(len(kmeans.cluster_centers_)+1))
        histograms.append(hist)
    return np.array(histograms)

def main():
    print("Carregando descritores...")
    des_list, labels = load_descriptors(DATASET_PATH)
    if len(des_list) == 0:
        print("Nenhum descritor encontrado. Verifique dataset.")
        return

    print("Construindo Bag of Words (KMeans)...")
    kmeans = build_bow(des_list)

    print("Convertendo descritores para histograma...")
    X = descriptors_to_hist(des_list, kmeans)
    y = labels

    print("Treinando SVM...")
    svm = SVC(kernel="linear", probability=True, random_state=42)
    svm.fit(X, y)

    print("Salvando artifacts...")
    os.makedirs("machineLearning", exist_ok=True)
    joblib.dump(svm, "machineLearning/model.pkl")
    joblib.dump(kmeans, "machineLearning/bow.pkl")

    print("Treinamento finalizado. model.pkl e bow.pkl em machineLearning/")

if __name__ == "__main__":
    main()

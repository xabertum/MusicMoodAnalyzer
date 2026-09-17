import numpy as np
import opensmile

from .config import MAX_SEQ_LEN, NUM_FEATURES_PER_FRAME

# Instancia costosa (carga config nativa de openSMILE): se crea una sola vez al importar
# el modulo, replicando el mismo FeatureSet/FeatureLevel usado en el notebook de entrenamiento.
_smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.ComParE_2016,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)


def extract_features(file_path: str) -> np.ndarray:
    """Extrae features con openSMILE y las ajusta a la forma (1, MAX_SEQ_LEN, NUM_FEATURES_PER_FRAME)
    que espera el modelo (mismo pipeline usado para entrenar: sin relleno de columnas, ya coinciden)."""
    features = _smile.process_file(file_path)
    seq = features.select_dtypes(include=[np.number]).values

    assert seq.shape[1] == NUM_FEATURES_PER_FRAME, (
        f"openSMILE devolvio {seq.shape[1]} columnas, se esperaban {NUM_FEATURES_PER_FRAME}"
    )

    if seq.shape[0] < MAX_SEQ_LEN:
        pad_width = MAX_SEQ_LEN - seq.shape[0]
        seq_padded = np.pad(seq, ((0, pad_width), (0, 0)), mode="constant")
    else:
        seq_padded = seq[:MAX_SEQ_LEN, :]

    return np.expand_dims(seq_padded.astype("float32"), axis=0)

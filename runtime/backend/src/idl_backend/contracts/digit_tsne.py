"""The nine immutable, precomputed MNIST experiments used by the lesson."""
import math
import os

COURSE_ID = os.environ.get("IDL_COURSE_UUID", "")
ENDPOINT = "/visual-feature-learning/digit-tsne-record"
VERSION = "mnist-full-v1"
EPOCHS = 15
SEED = 20261001
LEARNING_RATES = (0.0002, 0.002, 0.02)
BATCH_SIZES = (64, 128, 256)


def record_request(payload):
    if not isinstance(payload, dict) or set(payload) != {"learning_rate", "batch_size"}:
        raise ValueError("Only learning_rate and batch_size may be selected.")
    lr, batch = payload["learning_rate"], payload["batch_size"]
    if type(lr) not in (int, float) or not math.isfinite(lr) or lr not in LEARNING_RATES:
        raise ValueError("Unsupported learning rate.")
    if type(batch) is not int or batch not in BATCH_SIZES:
        raise ValueError("Unsupported batch size.")
    return {"version": VERSION, "learning_rate": float(lr), "batch_size": batch, "epochs": EPOCHS, "seed": SEED}

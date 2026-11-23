
# ==========================================
# AI MODEL TRAINING
# ==========================================

import csv
import json
import os

import numpy as np

from joblib import dump

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from config import (
    DATA_DIR,
    MODEL_PATH,
    LABELS_PATH
)


def main():

    csv_path = os.path.join(
        DATA_DIR,
        "gestures.csv"
    )

    if not os.path.exists(csv_path):

        print("Training data not found.")
        print("Run collect_data.py first.")
        return

    features = []
    labels = []

    with open(
        csv_path,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            try:

                sample = [
                    float(row[f"f{i}"])
                    for i in range(63)
                ]

                features.append(sample)
                labels.append(row["label"])

            except (ValueError, KeyError):
                continue

    if len(set(labels)) < 2:

        print(
            "Collect samples for at least "
            "two different signs."
        )

        return

    X = np.asarray(
        features,
        dtype=np.float32
    )

    y = np.asarray(labels)

    model = RandomForestClassifier(
        n_estimators=250,
        class_weight="balanced",
        random_state=42
    )

    # Split data for basic validation
    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(
        f"Validation accuracy: {accuracy:.2%}"
    )

    # Train final model using all collected samples
    model.fit(X, y)

    os.makedirs(
        os.path.dirname(MODEL_PATH),
        exist_ok=True
    )

    dump(
        model,
        MODEL_PATH
    )

    with open(
        LABELS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sorted(set(labels)),
            file,
            indent=4
        )

    print("AI model training completed.")
    print(f"Model saved: {MODEL_PATH}")


if __name__ == "__main__":
    main()

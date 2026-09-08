"""
NLP scoring interface.

The historical model architecture, labelled training data, model weights and
decision thresholds were not specified in the deposited schema. Therefore this
file defines the exact expected interface without inventing a model.

Replace `score_texts()` with the study's archived classifier before claiming
exact post-level NLP reproducibility.
"""
import pandas as pd

OUTPUTS = [
    "loneliness_score", "stress_score", "anxiety_score",
    "depression_score", "severe_distress_score",
    "public_distress_score", "latent_distress_score"
]

def score_texts(texts):
    raise NotImplementedError(
        "Insert the archived/validated NLP model here. Do not substitute a new "
        "classifier if exact historical reproducibility is required."
    )

def attach_scores(df):
    scores = score_texts(df["clean_text"].tolist())
    score_df = pd.DataFrame(scores, columns=OUTPUTS)
    return pd.concat([df.reset_index(drop=True), score_df], axis=1)

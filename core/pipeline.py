"""
CareerMatch AI — NLP Pipeline & Model Training
Handles dataset loading, NLP preprocessing, TF-IDF training, and model caching.
"""

import os
import re
import joblib
import pandas as pd
import numpy as np
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib")
JOB_MATRIX_PATH = os.path.join(MODEL_DIR, "job_vectors.joblib")
CLEAN_DF_PATH = os.path.join(MODEL_DIR, "clean_df.joblib")

# ---------------------------------------------------------------------------
# NLP Setup (lazy-loaded)
# ---------------------------------------------------------------------------
_nlp = None
_stop_words = None


def _init_nlp():
    """Lazily initialize spaCy and stopwords to avoid slow imports."""
    global _nlp, _stop_words
    if _nlp is not None:
        return

    _nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)

    universal_stopwords = {
        "summary", "skill", "qualification",
        "project", "projects", "certification", "honor", "award", "contact",
        "email", "phone", "location", "github", "linkedin", "profile",
        "status", "expected", "current", "gpa", "cumulative",
    }

    hr_fluff = {
        "ability", "candidate", "environment", "strong", "good",
        "hard", "deadline", "oriented", "fast", "paced", "proven",
        "excellent", "preferred", "required", "requirement",
    }

    _stop_words = set(nltk.corpus.stopwords.words("english")).union(
        universal_stopwords
    ).union(hr_fluff)


# ---------------------------------------------------------------------------
# Text Processing
# ---------------------------------------------------------------------------
def clean_text(raw_text: str) -> str:
    """
    NLP preprocessing pipeline: lowercasing, regex cleaning,
    spaCy lemmatization, and targeted stopword removal.
    """
    _init_nlp()

    if not isinstance(raw_text, str) or not raw_text:
        return ""

    text = raw_text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\S+@\S+", "", text)
    # Keep dots and plus signs for terms like C++, Node.js
    text = re.sub(r"[^\w\s\.+]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    doc = _nlp(text)
    purified_tokens = [
        token.lemma_
        for token in doc
        if token.lemma_ not in _stop_words
        and len(token.lemma_) > 1
        and not token.text.isnumeric()
    ]

    return " ".join(purified_tokens)


def boost_and_align_keywords(text: str) -> str:
    """
    Umbrella Terms Alignment — maps modern CV terminology to
    historical dataset terminology so TF-IDF retains context.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()

    synonyms = {
        # DOMAIN 1: TECH & AI
        r"\b(prompt engineering|nlp|deep learning|ai|machine learning|tensor flow|scikit-learn|classification|sentiment analysis)\b":
            "statistics data_science analytics",
        r"\b(next\.js|react|frontend|full-stack|backend|php|sql|node\.js|framework)\b":
            "web_development javascript html css",
        # DOMAIN 2: FINANCE & ACCOUNTING
        r"\b(pajak|brevet|taxation|tax)\b":
            "tax compliance accounting",
        r"\b(bookkeeping|pembukuan|accounting)\b":
            "accounting financial_reporting ledger",
        # DOMAIN 3: MARKETING & SALES
        r"\b(digital marketing|seo|sem|content creator)\b":
            "marketing advertising public_relations",
        r"\b(account executive|telemarketing)\b":
            "sales retail business_development",
    }

    for pattern, replacement in synonyms.items():
        text = re.sub(pattern, replacement, text)

    return text


# ---------------------------------------------------------------------------
# Model Training & Caching
# ---------------------------------------------------------------------------
def _download_and_prepare_dataset(progress_callback=None) -> pd.DataFrame:
    """Download Kaggle dataset and perform data cleaning."""
    import subprocess
    import zipfile

    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    csv_path = os.path.join(DATA_DIR, "data job posts.csv")

    # If CSV already exists locally, just load it
    if not os.path.exists(csv_path):
        os.makedirs(DATA_DIR, exist_ok=True)

        if progress_callback:
            progress_callback("Downloading job postings dataset from Kaggle...")

        zip_path = os.path.join(DATA_DIR, "jobposts.zip")
        try:
            subprocess.run(
                ["kaggle", "datasets", "download", "-d", "madhab/jobposts", "-p", DATA_DIR],
                check=True, capture_output=True, text=True,
            )
        except FileNotFoundError:
            raise RuntimeError(
                "Kaggle CLI not found. Install it with: pip install kaggle\n"
                "Then configure credentials: https://www.kaggle.com/docs/api"
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Kaggle download failed: {e.stderr}\n"
                "Make sure ~/.kaggle/kaggle.json exists with valid credentials."
            )

        # Extract zip
        if progress_callback:
            progress_callback("Extracting dataset...")

        zip_file = os.path.join(DATA_DIR, "jobposts.zip")
        if os.path.exists(zip_file):
            with zipfile.ZipFile(zip_file, "r") as zf:
                zf.extractall(DATA_DIR)
            os.remove(zip_file)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset CSV not found at: {csv_path}\n"
            "Please download it manually from https://www.kaggle.com/datasets/madhab/jobposts "
            "and place 'data job posts.csv' in the 'data/' folder."
        )

    if progress_callback:
        progress_callback("Loading dataset...")

    df_jobs = pd.read_csv(csv_path)

    if progress_callback:
        progress_callback("Cleaning dataset...")

    # Select relevant columns
    clean_df = df_jobs[[
        "Title", "JobDescription", "JobRequirment", "RequiredQual"
    ]].copy()

    # Drop missing values and duplicates
    clean_df = clean_df.dropna(
        subset=["Title", "JobDescription", "JobRequirment", "RequiredQual"]
    )
    clean_df = clean_df.drop_duplicates()
    clean_df = clean_df.reset_index(drop=True)

    return clean_df


def _run_nlp_pipeline(clean_df: pd.DataFrame, progress_callback=None) -> pd.DataFrame:
    """Apply NLP preprocessing to the dataset."""
    if progress_callback:
        progress_callback("Combining text columns...")

    clean_df["Combined_Text"] = (
        clean_df["Title"] + " " +
        clean_df["JobDescription"].fillna("") + " " +
        clean_df["JobRequirment"].fillna("") + " " +
        clean_df["RequiredQual"].fillna("")
    )

    if progress_callback:
        progress_callback("Applying NLP preprocessing (this may take a few minutes)...")

    tqdm.pandas(desc="Processing text")
    clean_df["Cleaned_Text"] = clean_df["Combined_Text"].progress_apply(clean_text)

    return clean_df


def _train_tfidf(clean_df: pd.DataFrame, progress_callback=None):
    """Train TF-IDF vectorizer and compute job vectors."""
    if progress_callback:
        progress_callback("Aligning umbrella terms...")

    aligned_jobs = clean_df["Cleaned_Text"].apply(boost_and_align_keywords)

    if progress_callback:
        progress_callback("Training TF-IDF Vectorizer...")

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2,
        max_df=0.85,
    )
    job_matrix = vectorizer.fit_transform(aligned_jobs)

    return vectorizer, job_matrix


def load_or_train_model(progress_callback=None):
    """
    Load cached model artifacts, or train from scratch if not available.

    Args:
        progress_callback: Optional callable(status_message: str) for UI updates.

    Returns:
        tuple: (vectorizer, job_matrix, clean_df)
    """
    # Try loading cached models
    if (
        os.path.exists(VECTORIZER_PATH)
        and os.path.exists(JOB_MATRIX_PATH)
        and os.path.exists(CLEAN_DF_PATH)
    ):
        if progress_callback:
            progress_callback("Loading cached model...")
        vectorizer = joblib.load(VECTORIZER_PATH)
        job_matrix = joblib.load(JOB_MATRIX_PATH)
        clean_df = joblib.load(CLEAN_DF_PATH)
        return vectorizer, job_matrix, clean_df

    # Train from scratch
    if progress_callback:
        progress_callback("No cached model found. Starting training pipeline...")

    clean_df = _download_and_prepare_dataset(progress_callback)
    clean_df = _run_nlp_pipeline(clean_df, progress_callback)
    vectorizer, job_matrix = _train_tfidf(clean_df, progress_callback)

    # Cache artifacts
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(job_matrix, JOB_MATRIX_PATH)
    joblib.dump(clean_df, CLEAN_DF_PATH)

    if progress_callback:
        progress_callback("Model training complete!")

    return vectorizer, job_matrix, clean_df

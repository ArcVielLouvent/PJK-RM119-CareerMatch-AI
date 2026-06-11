"""
CareerMatch AI — Inference Engine
Handles CV-to-job matching using Cosine Similarity with business rule heuristics.
"""

import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from core.pipeline import clean_text, boost_and_align_keywords


def extract_yoe(text: str) -> int:
    """
    Extract Years of Experience heuristically from text.

    Args:
        text: Raw text (CV or job qualification).

    Returns:
        int: Maximum detected years, or 0 if none found.
    """
    text = str(text).lower()
    pattern = r"(\d+)\s*(?:\+|-)?\s*(?:to\s*\d+\s*)?years?(?:\s*of\s*experience)?"
    matches = re.findall(pattern, text)
    if matches:
        return max(int(m) for m in matches)
    return 0


def get_job_recommendations(cv_text, tfidf_model, job_matrix, clean_df, top_k=5):
    """
    Find best-matching jobs for a CV using Cosine Similarity with
    business rule optimizations: Title Boosting, Negative Filter, YoE Penalty.

    Args:
        cv_text: Raw CV text (extracted from PDF or manual input).
        tfidf_model: Trained TF-IDF Vectorizer.
        job_matrix: Pre-computed TF-IDF job vectors.
        clean_df: Cleaned DataFrame with job postings.
        top_k: Number of top recommendations to return.

    Returns:
        list[dict]: Recommendations with Job Title, Match Score, YoE, Qualifications.
    """
    cleaned_cv = clean_text(cv_text)
    aligned_cv = boost_and_align_keywords(cleaned_cv)

    cv_vector = tfidf_model.transform([aligned_cv])
    similarity_scores = cosine_similarity(cv_vector, job_matrix).flatten()

    # Candidate pool — top 100 for filtering
    top_100_indices = similarity_scores.argsort()[-100:][::-1]

    cv_yoe = extract_yoe(cv_text)

    # Detect CV domain via umbrella terms
    is_tech_cv = any(
        kw in aligned_cv
        for kw in ["web_development", "data_science", "analytics", "javascript", "html"]
    )
    is_finance_cv = any(
        kw in aligned_cv
        for kw in ["accounting", "tax", "financial_reporting"]
    )
    is_marketing_cv = any(
        kw in aligned_cv
        for kw in ["marketing", "advertising", "sales"]
    )

    temp_recommendations = []

    for idx in top_100_indices:
        raw_score = similarity_scores[idx]
        if raw_score < 0.02:
            continue

        job_info = clean_df.iloc[idx]
        job_title = str(job_info["Title"]).lower()
        job_yoe = extract_yoe(job_info["RequiredQual"])

        # --- NEGATIVE FILTER (ANTI-MISMATCH) ---
        if is_tech_cv:
            non_tech_triggers = [
                "customs", "logistic", "warehouse", "clerical", "apparel", "secretary"
            ]
            if any(trigger in job_title for trigger in non_tech_triggers):
                continue

        if is_finance_cv:
            tech_triggers = [
                "developer", "programmer", "software engineer", "sysadmin", "devops"
            ]
            if any(trigger in job_title for trigger in tech_triggers):
                continue

        # --- YOE FILTER ---
        if cv_yoe == 0 and any(
            kw in job_title for kw in ["senior", "lead", "architect", "principal"]
        ):
            continue
        if cv_yoe < job_yoe:
            continue

        # --- TITLE BOOSTING ---
        title_boost = 1.0
        if is_tech_cv and any(
            kw in job_title
            for kw in ["developer", "analyst", "engineer", "programmer", "it", "technical"]
        ):
            title_boost = 1.15
        elif is_finance_cv and any(
            kw in job_title
            for kw in ["accountant", "finance", "audit", "tax", "bookkeeper"]
        ):
            title_boost = 1.15
        elif is_marketing_cv and any(
            kw in job_title
            for kw in ["marketing", "sales", "seo", "content", "brand"]
        ):
            title_boost = 1.15

        # --- SCORE CALCULATION ---
        scaled_score = np.sqrt(raw_score)
        final_score = (scaled_score * 2.0 * title_boost) * 100
        final_score = min(95.0, final_score)

        temp_recommendations.append({
            "Job Title": job_info["Title"],
            "Match Score": final_score,
            "Required YoE": job_yoe,
            "Required Qualifications": job_info["RequiredQual"],
        })

    # Sort by final score
    sorted_recs = sorted(
        temp_recommendations, key=lambda x: x["Match Score"], reverse=True
    )

    # Round and return top_k
    final_results = []
    for rec in sorted_recs[:top_k]:
        rec["Match Score"] = round(rec["Match Score"], 2)
        final_results.append(rec)

    return final_results

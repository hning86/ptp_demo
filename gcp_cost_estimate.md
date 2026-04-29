# GCP Cost Estimate for Craft PTP Demo

This document provides a rough estimate of the costs associated with deploying the Craft PTP Demo application to Google Cloud Platform (GCP).

## Architecture Summary

Based on the codebase analysis (specifically [main.py](file:///Users/ninghai/projects/craft-ptp-demo-v2/backend/main.py) and [Dockerfile](file:///Users/ninghai/projects/craft-ptp-demo-v2/Dockerfile)), the application uses the following services:

1.  **Compute:** Containerized FastAPI application (suitable for **Cloud Run**).
2.  **Database:** **BigQuery** for querying schedule data (table: `simulated_schedule`).
3.  **Storage:** **Cloud Storage (GCS)** for serving safety documents (bucket: `ninghai-bucket-0`).
4.  **AI/ML:** **Vertex AI / Gemini API** via the Google ADK for chat agent capabilities.

---

## Usage Scenarios

Since actual usage metrics are unknown, estimates are provided for two scenarios:

### 1. Demo / Developer Tier (Low Usage)
*   **Users:** 1-5 developers/testers.
*   **Interactions:** A few hundred chat messages per month.
*   **Data:** Minimal storage (< 1 GB) and low query volume.

### 2. Pilot / Small Team Tier (Moderate Usage)
*   **Users:** ~50 active users.
*   **Interactions:** Frequent daily usage (thousands of messages per month).
*   **Data:** Regular querying and document access.

---

## Cost Breakdown Estimate (Focused on Gemini 2.5 Flash)

Based on your confirmation that the app uses **Gemini 2.5 Flash** (as seen in [.env](file:///Users/ninghai/projects/craft-ptp-demo-v2/backend/.env)), the token costs are significantly lower than initially estimated for "Pro" models.

| Service | Demo Tier (Monthly) | Pilot Tier (Monthly) | Notes |
| :--- | :--- | :--- | :--- |
| **Cloud Run** (Compute) | $0.00 (Free Tier) | $5.00 - $20.00 | Assumes scaling to zero when idle. |
| **Cloud Storage** (Storage) | $0.00 (Free Tier) | < $1.00 | Very low storage requirements for PDFs. |
| **BigQuery** (Analytics) | $0.00 (Free Tier) | $1.00 - $5.00 | Low query volume for schedule lookups. |
| **Vertex AI (Gemini 2.5 Flash)** | **< $0.50** | **$2.00 - $10.00** | **Extremely cost-effective.** Billed per token. |
| **Vertex AI RAG Engine** | **$0.00 - $5.00** | **$10.00 - $50.00** | Billed per query and storage. See breakdown below. |
| **Networking** | $0.00 | $1.00 - $5.00 | Egress traffic costs. |
| **Total Estimated Cost** | **< $6.00** | **$20.00 - $90.00** | **Includes RAG costs.** |

---

## Gemini 2.5 Flash Token Cost Breakdown

Since exact public pricing for Gemini 2.5 Flash is not available in my offline training data, we use standard **Gemini 1.5 Flash** rates as a baseline. Flash models are designed to be lightweight and highly economical.

*   **Input Tokens:** ~$0.075 per 1,000,000 tokens ($0.000075 per 1k tokens).
*   **Output Tokens:** ~$0.30 per 1,000,000 tokens ($0.0003 per 1k tokens).

### Example Scenarios:

#### A. Single Chat Interaction
*   **Input:** 1,000 tokens (System prompt + User message + RAG context). Cost: ~$0.000075.
*   **Output:** 500 tokens (Agent response). Cost: ~$0.00015.
*   **Total:** ~$0.000225 (Less than 1/40th of a cent).

#### B. High Volume Usage (10,000 messages/month)
*   **Input:** 10,000,000 tokens. Cost: ~$0.75.
*   **Output:** 5,000,000 tokens. Cost: ~$1.50.
*   **Total:** ~$2.25.

---

## Vertex AI RAG Engine Cost Breakdown

Vertex AI RAG Engine (or Vertex AI Search) costs typically scale with the number of queries and the amount of data indexed.

*   **Storage/Indexing:** Costs are generally low for small document sets (like a few safety PDFs). Expect less than $5/month for a small corpus.
*   **Retrieval Queries:** If using Vertex AI Search standard edition, it costs ~$0.05 per query.
    *   **Demo (100 queries/month):** ~$5.00.
    *   **Pilot (1,000 queries/month):** ~$50.00.

> [!IMPORTANT]
> RAG Engine queries can add up quickly if every chat message triggers a search. Ensure your agent only calls the RAG tool when necessary to keep costs down.

---

## Key Cost Drivers & Recommendations

> [!TIP]
> **Context Caching:** If your agent uses large static system instructions or large documents frequently, check if Vertex AI Context Caching is supported for Gemini 2.5 Flash. This can reduce input token costs by up to 50% for cached content.

> [!NOTE]
> **Flash vs Pro:** Stick with Gemini 2.5 Flash unless you find a specific task requires the advanced reasoning capabilities of Gemini 1.5 Pro or 2.5 Pro. The cost difference is substantial (up to 20x-50x more for Pro models).

## Next Steps

To get a more precise estimate:
1.  Monitor your token usage in the Google Cloud Console under Vertex AI metrics.
2.  Estimate the average size of your RAG retrieval context, as this contributes significantly to input tokens.

# PathoScope AI — AI Configuration Report

**Date**: June 5, 2026  
**Auditor**: Antigravity  
**Status**: Completed  

---

## 1. Environment Variables Config Audit

We verified the mechanism for loading LLM API keys:
- Enclosing single/double quotes are stripped: `strip().strip('\'"')` is added in `backend/config/settings.py` to prevent quotes from polluting API keys.
- Environment variables loaded:
  - `OPENAI_API_KEY`: used to configure the OpenAI chat completion engine.
  - `GEMINI_API_KEY`: used to configure Google Generative AI (`gemini-1.5-flash`).
- Safe check flags `is_openai_available` and `is_gemini_available` return `True` only if key length > 0.
- Fallback logic: If neither API key is configured or requests fail, the pipeline falls back to an offline rule-based interpretation with a warning.

---

## 2. Security Compliance

- **Rule 9.3**: API keys are stored only in `backend/.env`. No hardcoded keys exist in the repository.
- **Rule 9.4**: The Next.js frontend has no access to the keys. All AI calls run inside the backend (`backend/services/ai_service.py`) and result fields are committed to the SQL database (`AIInterpretation` table). The frontend reads only processed database records.
- Environment configurations are loaded using pydantic models (`Settings` in `backend/config/settings.py`) with zero secrets exposed to client-side.

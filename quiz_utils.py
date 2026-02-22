"""
Quiz utility functions: answer normalization, text matching, client IP.
"""

from typing import Optional

import streamlit as st

from i18n import translate_text


def _normalize_answer_text(value: str) -> str:
    return value.lower().strip() if isinstance(value, str) else ""


def _is_text_answer_correct(user_answer: str, correct_answer: str) -> bool:
    user_clean = _normalize_answer_text(user_answer)
    if not user_clean:
        return False
    variants = {correct_answer}
    translated_correct = translate_text(correct_answer) if correct_answer else ""
    if translated_correct and translated_correct != correct_answer:
        variants.add(translated_correct)

    for variant in variants:
        variant_clean = _normalize_answer_text(variant)
        if not variant_clean:
            continue
        if user_clean == variant_clean:
            return True
        variant_keywords = [keyword for keyword in variant_clean.split() if len(keyword) > 3]
        user_keywords = [keyword for keyword in user_clean.split() if len(keyword) > 3]
        if any(keyword in user_clean for keyword in variant_keywords):
            return True
        if any(keyword in variant_clean for keyword in user_keywords):
            return True
    return False


def _extract_ip_from_headers(headers) -> Optional[str]:
    if not headers:
        return None
    try:
        header_get = headers.get
    except AttributeError:
        try:
            header_get = dict(headers).get
        except Exception:
            return None
    for key in ("X-Forwarded-For", "X-Real-IP", "CF-Connecting-IP", "True-Client-IP"):
        value = header_get(key)
        if value:
            return value.split(",")[0].strip()
    return None


def get_client_ip() -> str:
    """Best-effort client IP lookup (may be unavailable in some envs)."""
    try:
        if hasattr(st, "context") and getattr(st.context, "headers", None):
            ip = _extract_ip_from_headers(st.context.headers)
            if ip:
                return ip
    except Exception:
        pass

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        ctx = get_script_run_ctx()
        request = getattr(ctx, "request", None) if ctx else None
        if request is not None:
            ip = _extract_ip_from_headers(getattr(request, "headers", None))
            if ip:
                return ip
            remote_ip = getattr(request, "remote_ip", None)
            if remote_ip:
                return remote_ip
    except Exception:
        pass

    return "Ismeretlen"

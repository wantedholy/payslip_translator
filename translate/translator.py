from deep_translator import GoogleTranslator


def preserve_numbers_translate(text, target_lang):
    """
    Use deep-translator library for more reliable translation
    """
    if not text.strip():
        return ""

    try:
        # Language mapping
        lang_map = {
            "hi": "hindi",
            "bn": "bengali",
            "or": "odia"
        }

        target = lang_map.get(target_lang, target_lang)

        translator = GoogleTranslator(source='english', target=target)
        translated = translator.translate(text)

        print(f"Original: {text[:50]}...")
        print(f"Translated: {translated[:50]}...")

        return translated

    except Exception as e:
        print(f"Translation error: {e}")
        return f"[Translation failed] {text}"

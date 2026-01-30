# Test Folder

Plaats hier je test foto's van bonnetjes en gebruik het test script.

## Gebruik

```bash
# Vanuit de root folder (CloudClaude/)

# 1. Test modus - fake data (geen foto nodig)
python test/test_ocr.py

# 2. Test met een foto + Tesseract (gratis)
python test/test_ocr.py test/bonnetje.jpg tesseract

# 3. Test met een foto + OpenAI (kost ~€0.02)
python test/test_ocr.py test/bonnetje.jpg openai
```

## Voorbeelden

Plaats je bonnetje foto's in deze folder:
- `test/bonnetje.jpg`
- `test/ah_bon.png`
- etc.

## Output

Het script toont:
1. Geformatteerde output (zoals je in Telegram ziet)
2. Ruwe JSON data (voor debugging)
3. OCR tekst (bij tesseract/openai modus)

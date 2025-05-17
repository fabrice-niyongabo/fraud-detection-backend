import asyncio
from googletrans import Translator

def translate(text):
    translator = Translator()
    
    async def do_translate():
        result = await translator.translate(text, dest='en')
        return result.text
    
    try:
        translated_text = asyncio.run(do_translate())
        return translated_text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text
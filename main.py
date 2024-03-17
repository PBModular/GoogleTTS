from base.mod_ext import BaseModule
from base.module import command
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from gtts import gTTS
from io import BytesIO
from langdetect import detect
import tempfile
import os


class GoogleTTSModule(BaseModule):
    @command("tts")
    async def tts_cmd(self, bot: Client, message: Message):
        """Convert text to speech with Google APIs"""

        text = await self.get_text_from_message(message)
        
        if not text:
            await message.reply(self.S["no_text"])
            return
        
        try:
            lang = detect(text)
            tts = gTTS(text=text, lang=lang)
            speech_bytes = BytesIO()
            tts.write_to_fp(speech_bytes)
            speech_bytes.seek(0)
        except ValueError:
            await message.reply(self.S["no_lang"].format(lang=lang))
            return
        
        temp_filename = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
                temp_filename = temp.name
                temp.write(speech_bytes.read())

            await message.reply_voice(voice=temp_filename)
        finally:
            if temp_filename and os.path.exists(temp_filename):
                os.remove(temp_filename)

    async def get_text_from_message(self, message):
        """Extract text from the message or the replied message"""
        text = message.text.split(" ", 1)
        
        if message.reply_to_message:
            text = message.reply_to_message.text or ""
        elif len(text) > 1:
            text = text[1]
        else:
            text = ""
            
        return text.strip()

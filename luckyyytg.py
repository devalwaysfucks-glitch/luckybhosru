import asyncio
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ChatType
from telegram.error import RetryAfter, TimedOut, NetworkError
import logging
import re
import random
from telegram.request import HTTPXRequest

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)

OWNER_ID = 8138884920
BOT_TOKENS = [
"8835485714:AAGhbaA56uOlO0r35mVyHbEhrLH1Q7fb0QA",
"8906962785:AAHbP89S1uDe2w6B28W8jaufIepGLM5gdlw",
"8699397297:AAEb98IO6m67RgVWitDR1EHq8S_KUYDVHS0",
"8847893364:AAGfVV28wSaLDVLxgWnvdLNS_stdoRWBsJc",
"8905623267:AAHs6WPUSE83Q-oTMP_-xvzHdT18e6OXEbg",
"8856042776:AAFxSpfDVF4-eLPFtO6pv5HgwAhtWL_zLu4",
"8242597379:AAFNZ9_LCmmpfbt1HS6Sizdt7-kOnuJ3Xvg",
"8758907155:AAEaNgb8peVoJRK3-oaq-3rIiE1IlPXDa8E",
"8843993022:AAE-aCEubXxNfutwq0ngDhrr4ViFNToIdt4",
"8600852322:AAFGz6JprTd7Nn3MN86yM-GQFicQd8nEuXI",
"8858657720:AAH-FTtjDo17etJh6p-8UQrsaEawYDypapc",
"8810298978:AAELm44ma8BWVzakMbAyPD9Rv_bNr4ut55o",
"8852378197:AAFRmdbMl7RQAn1h_40mbAwItaTAHQKlbkY",
"8686292896:AAHDiUctYSG6OAHMwC6V94moJzu7tFduj50",   
]

BOT_TOKENS = [t for t in BOT_TOKENS if t]

if not BOT_TOKENS:
    print("ERROR: No bot tokens found! Set BOT_TOKEN_1, BOT_TOKEN_2, etc. environment variables")
    exit(1)

STRAWBERRY_EMOJIS = ["🍓🎀❤️","🍓🎀🧡","🍓🎀💛","🍓🎀💚","🍓🎀💙","🍓🎀💜","🍓🎀🖤","🍓🎀🤍","🍓🎀🤎","🍓🎀💗",
    "💓","💞","💕","💘","💝","💖","♥️","❣️","💟","🫀",]

heart_EMOJIS = ["// 😩🌊 // 🐮🩶 /","// 😩🌊 // 🐮🖤 /","// 😩🌊 // 🐮🤍 /","// 😩🌊 // 🐮🩵 /","// 😩🌊 // 🐮💙 /","// 😩🌊 // 🐮💔 /","// 😩🌊 // 🐮❤️‍🩹 /","// 😩🌊 // 🐮🩶 /","// 😩🌊 // 🐮🩶 /","// 😩🌊 // 🐮🩶 /","/ / 😩🌊 // 🐮🩶 /","// 😩🌊 // 🐮🩶 /","// 😩🌊 // 🐮💝 /","// 😩🌊 // 🐮❤️‍🔥 /","// 😩🌊 // 🐮🩶 /","// 😩🌊 // 🐮🩷 /","// 😩🌊 // 🐮❤️ /"]

NC_heart_MESSAGES = [
    "कमजोर रण्डी 🩶᭪","कमजोर रण्डी 🩵᭪","कमजोर रण्डी 🩷᭪","कमजोर रण्डी 🤍᭪","कमजोर रण्डी 🤎᭪","कमजोर रण्डी 🖤᭪","कमजोर रण्डी 💜᭪","कमजोर रण्डी 💙᭪","कमजोर रण्डी 💛᭪","कमजोर रण्डी 🧡᭪","कमजोर रण्डी ❤️᭪","कमजोर रण्डी 💚᭪",
]

FLAG_EMOJIS = ['🏳️', '🏴', '🚩', '🎌', '🏁', '🇮🇳', '🏳️‍🌈', '🏴‍☠️', '⛳', '🎏', '🇦🇨', '🇧🇭', '🇧🇬', '🇦🇶', '🇦🇴', '🇦🇮', '🇦🇲', '🇦🇽', '🇦🇱', '🇦🇷','🏳️', '🏴', '🚩', '🎌', '🏁', '🇮🇳', '🏳️‍🌈', '🏴‍☠️', '⛳', '🎏']

NC_FLAG_MESSAGES = [
    "{target} चुद पुत्र 🍓🎀🩵💋🏴‍☠️⊹","{target} चुद पुत्र 🍓🎀🩵💋⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇦🇫⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇧🇧⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇧🇱⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇪🇺⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇦🇺⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇪🇪⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇪🇭⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇬🇵⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇭🇰⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇪🇬⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇲🇴⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇵🇬⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇱🇾⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇲🇦⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🏴󠁧󠁢󠁷󠁬󠁳󠁿⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇻🇮⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇸🇩⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇲🇵⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇾🇹⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇹🇷⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇸🇾⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇸🇬⊹","{target} चुद पुत्रˑ 🍓🎀🩵💋🇸🇬⊹"

]

TIME_NC_MESSAGES = [
   "{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕧➥🚸🧦",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕐➥🧦🚸",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕜➥🚸🧦",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕑➥🧦🚸",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕝➥🚸🧦 ",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕒➥🧦🚸 ",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕞➥🚸🧦 ",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕓➥🧦🚸 ",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕓➥🚸🧦",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕟➥🧦🚸 ",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕔➥🚸🧦 ",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕠➥🧦🚸 ",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕕➥🚸🧦 ",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕡➥🧦🚸",
"{target} 𝗞𝗜 𝗠𝗔 𝗖𝗛𝗨𝗗𝗜 𝗔𝗧 - 🕖➥🚸🧦 ",
    
]

NC_WEB_MESSAGES = [
    "{target} 𝑇𝑀𝐾𝐿℘✩₊˚.⋆🕸️",
    "{target} 𝑇𝐵𝐾𝐿℘✩₊˚.⋆🕸️",
    "{target} 𝑇𝑀𝐾𝐶℘✩₊˚.⋆🕸️",
    "{target} 𝐺𝐴𝑌℘✩₊˚.⋆🕸️",
    "{target} 𝐶𝐻𝑈𝐷℘✩₊˚.⋆🕸️",
    "{target} 𝐷𝐹𝐴𝑁℘✩₊˚.⋆🕸️",
    "{target} 𝐾𝐼𝐷℘✩₊˚.⋆🕸️",
    "{target} 𝐶𝐻𝐴𝑃𝑅𝐼℘✩₊˚.⋆🕸️",
    "{target} 𝐿𝐸𝑆𝐵𝐼𝐴𝑁℘✩₊˚.⋆🕸️",
    "{target} 𝐻𝐼𝐽𝐷𝐴℘✩₊˚.⋆🕸️",
    "{target} 𝑃𝑈𝑆𝑆𝑌 𝐺𝑈𝑌℘✩₊˚.⋆🕸️",
    "{target} 𝐹𝑈𝐶𝐾𝐵𝑂𝑌℘✩₊˚.⋆🕸️",
    "{target} 𝑇𝑅𝐴𝑁𝑆𝐺𝐸𝑁𝐷𝐸𝑅℘✩₊˚.⋆🕸️",
    "{target} 𝑀𝑂𝑇𝐻𝐸𝑅𝐹𝑈𝐶𝐾𝐸𝑅℘✩₊˚.⋆🕸️",
    "{target} 𝐵𝐼𝑇𝐶𝐻℘✩₊˚.⋆🕸️",
    "{target} 𝑅𝐴𝑁𝐷𝐼℘✩₊˚.⋆🕸️",
    "{target} 𝐶𝐻𝐼𝑁𝑁𝐴𝑅℘✩₊˚.⋆🕸️",
    "{target} 𝑇𝑀𝐾𝐵℘✩₊˚.⋆🕸️", 
]

DOTZKENG_MESSAGES = [
    "{target} SWIPE KENG BANAU RNDY K <🐎>",
    "{target} 𝐂ʜᴜᴅᴊᴀ 𝐑ᴇɴᴅʏ 𝐊ᴇʏ <🦧>",
    "{target} 𝐋ɴᴅ 𝐂ʜᴜꜱ <🩶>",
    "{target} 𝐒ᴜᴄᴋ 𝐌ʏ 𝐃ɪᴄᴋ <🦕>",
    "{target} 𝐌ᴀᴀ 𝐂ʜᴜᴅᴀ <🫎>",
    "{target} 𝐄ᴋ 𝐑ᴇᴩᴛᴇʏ 𝐌ᴀɪ 𝐌ᴜᴛᴛ 𝐃ᴇɢᴀ <🐘>",
    "{target} 𝐋ᴡᴅᴀ 𝐏ᴀɢʟᴜ <🐙>",
    "{target} 𝐆ᴀʏ 𝐓ᴍᴋʙ <🪼>",
    "{target} CHMR EY TU <🦖>",
    "{target}  𝐆ᴀᴅʜᴇʏ 𝐊ɪ 𝐆ᴀᴀɴᴅ <🐸>",
    "{target}  CUDKEY DIKA बचें <🦁>",
    "{target} TERY MA MAFIA RNDY <🫏>"]

FLOWER_NC_MESSAGES = [
    "𝜗𝜚⋆₊🍁˚{target} Sʟᴜᴛ Mᴀᴀ ᴋᴇ Lᴀᴅᴋᴇ ",
    "𝜗𝜚⋆₊🌱˚{target} Sʟᴜᴛ Mᴀᴀ ᴋᴇ Lᴀᴅᴋᴇ ",
    "𝜗𝜚⋆₊🌿˚{target} Sʟᴜᴛ Mᴀᴀ ᴋᴇ Lᴀᴅᴋᴇ ",
    "𝜗𝜚⋆₊🍃˚{target} Sʟᴜᴛ Mᴀᴀ ᴋᴇ Lᴀᴅᴋᴇ ",
    "𝜗𝜚⋆₊☘️˚{target} Sʟᴜᴛ Mᴀᴀ ᴋᴇ Lᴀᴅᴋᴇ ",
    "𝜗𝜚⋆₊🍀˚{target} Sʟᴜᴛ Mᴀᴀ ᴋᴇ Lᴀᴅᴋᴇ ",
    "𝜗𝜚⋆₊🪴˚{target} Sʟᴜᴛ Mᴀᴀ ᴋᴇ Lᴀᴅᴋᴇ ",
]

UNAUTHORIZED_MESSAGE = "-Sᴜᴅᴏ Lᴇᴋᴇ Aᴀᴊᴀ Fʜɪʀ Kʀɪʏᴏ Cᴏᴍᴍᴀɴᴅ Tᴍᴋᴄ ⭐"

NAME_CHANGE_MESSAGES = [
    "{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥🩶₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥🩵₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥🩷₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥🤍₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥🖤₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥🤎₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥💜₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥💙₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥💚₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥💛₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥🧡₊⊹","{target} 𝙍𝘼𝙉𝘿 𝙎𝙊𝙉 ➥❤️₊⊹",
]

REPLY_MESSAGES = [
    "{target} - 𝐌ᴜᴊᴇʏ 𝐊ʏᴀ 𝐌ᴇʏ 𝐓ᴏ 𝐓ʀɪ 𝐌ᴀ चोदूंगा ➥🦁🥀",
    "{target} - 𝐁ʜᴀɢᴀ 𝐓ᴏ 𝐓ᴇʀʏ 𝐌ᴀᴀ 𝐊ɪʏ 𝐋ᴀꜱʜ 𝐂ʜᴜᴅ जाएगी ➥🌸🐮🦓",
     "{} - 𝐊ᴏ 𝐏ᴇʟᴛᴇʏ 𝐇ᴜᴇ 𝐁ᴀᴛᴍᴀɴ 𝐏ᴀᴩᴀ 𝐊ɪ 𝐄ɴᴛʀʏ ➥🧦🚸",
    "{target} - 𝐂ᴩ 𝐊ʀᴋᴇʏ 𝐂ʜᴜᴅ 𝐆ʀɪʙ 𝐊ᴇʏ 𝐋ᴅᴋᴇʏ ➥❤️‍🔥🔥🦋", 
    "{target} - 𝐆ʀɪʙ 𝐊ᴇʏ 𝐋ᴅᴋᴇʏ 𝐓ᴇʀʏ 𝐌ᴀ 𝐃ɪ 𝐅ᴜᴅɪ 𝐑ᴇʏ ➥🤣🫶🏻🌙🔥", 
    "{target} - 𝟎ʏʏ 𝐓ᴇʀʏ 𝐌ᴀᴀ 𝐊ɪ 𝐂ʜᴜᴛ 𝐌ᴇʏ 𝐌ᴇʀᴇʏ 𝐋ᴏᴅᴇʏ 𝐊ɪ 𝐄ɴᴛʀʏ  ➥🤮🤘🏿🔥",
    "{target} - 2026 𝐌ᴇ 𝐃ᴜɴɪʏᴀ 𝐊ʜᴛᴍ 𝐇ᴇʏ (😋🤙) 𝐏ʀ 𝐓ᴇʀʏ 𝐌ᴀᴀ 𝐊ɪ 𝐂ʜᴜᴛ 𝐓ᴏᴅᴀʏ 𝐊ʜᴛᴍ 𝐊ʏ ➥🤪🤟🏿 ",
     "{target} - 𝐀ᴀᴩ 𝐊ɪ 𝐌ᴀɪʏᴀ 𝐂ʜᴏᴅᴜɴɢᴀ 𝐑ᴇɴᴅʏ 𝐊ᴇʏ ➥😍❤️‍🔥☪️", 
     "{target} -  𝐌ᴍᴀᴍʏ 𝐊ɪ 𝐂ʜᴜᴛ 𝐌ᴇʏ 𝐈ᴄᴇ 𝐂ʀᴇᴀᴍ🍦🍦🍦🍦🍦🍦𝐋ɢᴀ 𝐊ᴇʏ 𝐁ᴜᴅʜɪ करुँ ➥😜🙌🏻😜",
    "{target} - 𝐓ᴇʀʏ 𝐌ᴀᴀ 𝐊ɪʏ चूत 𝐌ᴇʏ 𝐋ᴀᴜᴅᴀ ➥🤣🙏🏿🥀", 
    "{target} - 𝐂ʜᴜᴘᴘ 😈🤎🙌 𝐕ᴀʀɴᴀᴀ 𝐓ʀʏ 𝐌ᴀ ¿?...😜 छोड़ के 😌 𝐌ᴜʀɢʜɪ † 𝐁ɴᴀ 𝐃ᴜɴɢᴀ.!! ➥💸♠️",
     "{target} - 𝐓ᴇʀʏ 𝐌ᴀᴀ (𝐁ᴀᴛᴍᴀɴ) 𝐊ᴇʏ 𝐋ᴜɴᴅ 𝐊ɪ 𝐅ᴀɴ 𝐄ʏʏ ➥🦋❤️‍🔥",
    "𝐊ʙᴀᴀᴅɪ 𝐖ᴀʟᴇʏ 🤣😭 {target}  𝐓ʀʏ 𝐌ᴀᴀ का भोसड़ा 𝐅ᴀᴀᴅ 𝐃ɪʏᴀ ➥😩🔥🤲🏻", 
    "{target} - 𝐓ᴇʀʏ 𝐌ᴀᴍᴍʏ चोद चोद 𝐊ᴇʏ रंडी 𝐁ɴᴀᴅɪ 𝐇ᴇʜᴇ ➥🤣🩶💢",
     "{target} - Teri माँ की चूत पे इतने बल्ले🏏🏏  𝐌ᴀʀᴜɴɢᴀ 𝗜𝗣𝗟 𝐉ᴇᴇᴛ 𝐉ᴀʏᴇɢɪ ➥🥂🧊🥂🧊🥂🧊🥂",
]

SPAM_MESSAGE_TEMPLATE = """{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙{target} ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 B4TMAN PAPA 𝑲𝑨 कुतिया के 🥂🌙"""

SPAM_MESSAGE_2 = """{target} 🤢🪽 𝐀ᴊ 𝐊ʜᴀᴋᴇ 𝐁ᴜʀɢᴇʀ 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐂ᴜᴅᴇɢɪ 𝐆ʜᴀʀ 𝐆ʜᴀʀ 🤪🤘🏿🔥 ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎{target} 🤢🪽 𝐀ᴊ 𝐊ʜᴀᴋᴇ 𝐁ᴜʀɢᴇʀ 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐂ᴜᴅᴇɢɪ 𝐆ʜᴀʀ 𝐆ʜᴀʀ 🤪🤘🏿🔥 """

SPAM_MESSAGE_3 = """ {target} ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄ ʜ ᴜ ᴛ ᴋᴀ ᴘᴀᴀɴɪ ɴɪᴋᴀʟᴜ ʀᴀɴᴅɪ ᴋᴇ ¿🛸　 　🌎　°　🌓　•　.°•　　🚀 ✯★　*　　　°　　　🛰 　°·　 🪐.　　　•　° ★　• ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ 









‎‎{target} 𑁍ࠬܓ<🩷>ʟᴀɴᴅ ᴄʜᴏᴏꜱ ɴᴏʀᴍɪᴇ ℘✩₊˚.⋆🕸️"""


def extract_retry_after(error_str):
    match = re.search(r'retry after (\d+)', error_str.lower())
    if match:
        return int(match.group(1))
    return None


class BotInstance:
    def __init__(self, bot_number, owner_id):
        self.bot_number = bot_number
        self.owner_id = owner_id
        self.sudo_users = set()
        self.active_spam_tasks = {}
        self.active_name_change_tasks = {}
        self.active_ncheart_tasks = {}
        self.active_ncflag_tasks = {}
        self.active_dotzkeng_tasks = {}
        self.active_curly_tasks = {}
        self.active_timenc_tasks = {}
        self.active_reply_tasks = {}
        self.active_reply_targets = {}
        self.active_react_chats = {}
        self.pending_replies = {}
        self.chat_delays = {}
        self.chat_threads = {}
        self.locks = {}
        self.proxy = None
        self.proxies_list = []
        self._load_proxies()

    def _load_proxies(self):
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as f:
                self.proxies_list = [line.strip() for line in f if line.strip()]
            if self.proxies_list:
                self.proxy = random.choice(self.proxies_list)

    async def join_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        if not context.args:
            await update.message.reply_text("Usage: -join <invite_link_or_username>")
            return
            
        link = context.args[0]
        # Clean the link if it's a full URL
        if "t.me/" in link:
            link = link.split("t.me/")[-1]
        if link.startswith("+"):
            link = link[1:]
        if link.startswith("@"):
            link = link[1:]
            
        print(f"[Bot {self.bot_number}] Attempting to join: {link}")
        try:
            # For public usernames or private invite hashes
            await context.bot.join_chat(link)
            # await update.message.reply_text(f"Bot {self.bot_number} joined! ✅")
        except Exception as e:
            print(f"[Bot {self.bot_number}] Join error: {e}")
            # await update.message.reply_text(f"Bot {self.bot_number} failed to join: {e}")

    async def proxy_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        if not context.args:
            status = f"Current Proxy: {self.proxy}" if self.proxy else "No proxy configured."
            await update.message.reply_text(f"{status}\nUsage: -proxy add <url> or -proxy reload")
            return

        cmd = context.args[0].lower()
        if cmd == "add" and len(context.args) > 1:
            proxy_url = context.args[1]
            with open("proxies.txt", "a") as f:
                f.write(f"{proxy_url}\n")
            self._load_proxies()
            await update.message.reply_text(f"Proxy added and reloaded! ✅")
        elif cmd == "reload":
            self._load_proxies()
            await update.message.reply_text(f"Proxies reloaded! Total: {len(self.proxies_list)} ✅")

    def get_lock(self, chat_id):
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    def is_owner(self, user_id):
        return user_id == self.owner_id or user_id in self.sudo_users

    async def sudo_command(self, update, context):
        if update.effective_user.id != self.owner_id:
            return

        if not context.args and not update.message.reply_to_message:
            await update.message.reply_text("Usage: -sudo @username or reply to a message with -sudo")
            return

        user_to_sudo = None
        if update.message.reply_to_message:
            user_to_sudo = update.message.reply_to_message.from_user.id
        else:
            # Try to get user from mention or ID
            arg = context.args[0]
            if arg.startswith("@"):
                # Note: CommandHandler doesn't resolve usernames to IDs automatically
                # This usually requires the user to be in the bot's cache
                await update.message.reply_text("Please reply to the user's message with -sudo to grant sudo.")
                return
            else:
                try:
                    user_to_sudo = int(arg)
                except ValueError:
                    await update.message.reply_text("Invalid User ID.")
                    return

        if user_to_sudo:
            self.sudo_users.add(user_to_sudo)
            await update.message.reply_text(f"User {user_to_sudo} granted SUDO powers! ✅")

    async def refresh_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        await update.message.reply_text(f"Bot {self.bot_number} is active and refreshed! ⚡")

    async def check_owner(self, update):
        user_id = update.effective_user.id
        if not self.is_owner(user_id):
            try:
                await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            except Exception:
                pass
            return False
        return True

    async def start(self, update, context):
        if not await self.check_owner(update):
            return

        help_text = f"""

- 𝐓ᴇʟᴇɢʀᴀᴍ 𝐕2 ℘✩₊˚.⋆🕸️


📑 | 𝑁𝐴𝑀𝐸 𝐶𝐻𝐴𝑁𝐺𝐸𝑅𝑆 ℘✩₊˚.⋆🕸️
• -nc < target > 
• -ncheart < target > 
• -ncemo < target > 
• -flowernc < target > 
• -ncflag < target > 
• -timenc < target > 
• -nccurly < target > 

⚙️ | 𝑆𝑃𝐴𝑀𝑆 & 𝑆𝑊𝐼𝑃𝐸 ℘✩₊˚.⋆🕸️
• -spam < target >
• -multispam < target > 
• -reply < target > 

💠 | 𝐺𝑅𝑂𝑈𝑃 𝑃𝐹𝑃 𝐶𝐻𝐴𝑁𝐺𝐸 ℘✩₊˚.⋆🕸️
• -setgc < send a picture and reply it with ( -setgc )
• -gc < changes telegram group image automatically >

✳️ | 𝑀𝐴𝑁𝐴𝐺𝐸𝑀𝐸𝑁𝑇 ℘✩₊˚.⋆🕸️
• -start
• -sudo < reply there message > 
• -ping < ms > 
• - delay < 1 - 100 > 
• -target < target > 
• -threads <1-50> [ Set Threads For nc+spams ]
• -refresh 

🛡️ | 𝐒ᴛᴏᴘ 𝐂ᴏᴍᴍᴀɴᴅs 
• -stopall
• -stopncflag 
• -stoptimenc
• -stopemonc
• -stopdotzkeng
• -stopnccurly
• -stopncheart
• -stopspam

📌 | 𝐍ᴏᴛɪᴄᴇ 
• ᴀʟʟ ᴀᴄᴛɪᴏɴs ʀᴜɴ ɪɴ ʟᴏᴏᴘs ғᴏʀ (ᴏᴡɴᴇʀs-sᴜᴅᴏ)
"""
        await update.message.reply_text(help_text)

    async def auto_name_loop(self, context, target_name):
        msg_index = 0
        num_messages = len(NAME_CHANGE_MESSAGES)
        print(f"[Bot {self.bot_number}] AUTO NAME LOOP started for {target_name}")
        try:
            while True:
                try:
                    display_name = target_name
                    await context.bot.set_my_name(name=display_name)
                    await asyncio.sleep(60)
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except Exception:
                    await asyncio.sleep(10.0)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] AUTO NAME LOOP stopped")

    async def auto_name_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        target_name = " ".join(context.args) if context.args else "BOT"
        chat_id = update.effective_chat.id
        
        # Stop existing auto_name tasks for this chat
        if chat_id in self.active_name_change_tasks:
            for task in self.active_name_change_tasks[chat_id]:
                task.cancel()
            del self.active_name_change_tasks[chat_id]

        task = asyncio.create_task(self.auto_name_loop(context, target_name))
        if chat_id not in self.active_name_change_tasks:
            self.active_name_change_tasks[chat_id] = []
        self.active_name_change_tasks[chat_id].append(task)
        await update.message.reply_text(f"Auto name change loop started for {target_name}! 🔄")

    async def stop_auto_name(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat_id = update.effective_chat.id
        if chat_id in self.active_name_change_tasks:
            for task in self.active_name_change_tasks[chat_id]:
                task.cancel()
            del self.active_name_change_tasks[chat_id]
        await update.message.reply_text("Auto name change stopped! 🛑")

    async def multispam_command(self, update, context):
        if not await self.check_owner(update):
            return
        if not context.args:
            await update.message.reply_text("Usage: -multispam <target>")
            return
        
        target = " ".join(context.args)
        chat_id = update.effective_chat.id
        await update.message.reply_text(f"🚀 Coordinated multi-spam started for {target}!")
        
        # This will be triggered on all bot instances since they share the same command handlers
        num_threads = self.chat_threads.get(chat_id, 1)
        self.active_spam_tasks[chat_id] = [asyncio.create_task(self.spam_loop(chat_id, target, context, i)) for i in range(num_threads)]

    async def react_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat_id = update.effective_chat.id
        if chat_id in self.active_react_chats:
            del self.active_react_chats[chat_id]
            await update.message.reply_text("Reactions disabled! ❌")
        else:
            self.active_react_chats[chat_id] = True
            await update.message.reply_text("Reactions enabled! 💀✅")

    async def time_nc_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(TIME_NC_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] TIME NC LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = TIME_NC_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.1))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except Exception:
                    await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] TIME NC LOOP stopped after {success_count} changes")

    async def time_nc_command(self, update, context):
        if not await self.check_owner(update): return
        if not context.args:
            await update.message.reply_text("Usage: -timenc <target>")
            return
        target = " ".join(context.args)
        chat_id = update.effective_chat.id
        num_threads = self.chat_threads.get(chat_id, 1)
        self.active_timenc_tasks[chat_id] = [asyncio.create_task(self.time_nc_loop(chat_id, target, context, i+1)) for i in range(num_threads)]
        await update.message.reply_text(f"Time NC Loop started for {target} with {num_threads} threads! ⌚🔥")

    async def stop_time_nc(self, update, context):
        if not await self.check_owner(update): return
        chat_id = update.effective_chat.id
        if chat_id in self.active_timenc_tasks:
            for task in self.active_timenc_tasks[chat_id]: task.cancel()
            del self.active_timenc_tasks[chat_id]
        await update.message.reply_text("Time NC Loop stopped! 🛑")

    async def ownrp_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        reply_to_message = update.message.reply_to_message
        if not reply_to_message:
            await update.message.reply_text("Please reply to a message with -ownrp to see details.")
            return

        target_user = reply_to_message.from_user
        target_name = target_user.first_name if target_user else "Unknown"
        target_id = target_user.id if target_user else "Unknown"
        target_username = f"@{target_user.username}" if target_user and target_user.username else "None"
        
        owner_info = f"OWNER ID: `{self.owner_id}`"
        target_info = f"TARGET NAME: `{target_name}`\nTARGET ID: `{target_id}`\nTARGET USERNAME: {target_username}"
        
        await update.message.reply_text(
            f"𓆩 𝐃𝐄𝐓𝐀𝐈𝐋𝐒 𓆪\n\n"
            f"{owner_info}\n\n"
            f"{target_info}\n\n"
            f"𝐓𝐇𝐄 𝐆𝐑𝐄𝐀𝐓 B4TMAN⋆͙🐉 अब्बू'𝐒 𝐁𝐎𝐓",
            parse_mode='Markdown'
        )

    async def name_change_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NAME_CHANGE_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] Name change LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NAME_CHANGE_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    # Base delay of 0.1s to avoid immediate flood, plus user delay
                    await asyncio.sleep(max(delay, 0.1))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    # Add extra buffer to satisfy Telegram's cooling period
                    await asyncio.sleep(wait_time + 1.0)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(1.0)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 1.0)
                    else:
                        await asyncio.sleep(1.0)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Name change LOOP #{worker_id} stopped after {success_count} changes")

    async def flower_nc_loop(self, chat_id, base_name, context):
        msg_index = 0
        num_messages = len(FLOWER_NC_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] FLOWER NC LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = FLOWER_NC_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] FLOWER NC LOOP stopped after {success_count} changes")

    async def nc_emo_loop(self, chat_id, base_name, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] NC EMO LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    emoji = random.choice(HEART_EMOJIS)
                    display_name = f"{emoji} {base_name} {emoji}"
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except Exception:
                    await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC EMO LOOP stopped after {success_count} changes")

    async def nc_heart_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_heart_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] NC heart LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_heart_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC heart LOOP #{worker_id} stopped after {success_count} changes")

    async def nc_flag_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_FLAG_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] NC FLAG LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_FLAG_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC FLAG LOOP #{worker_id} stopped after {success_count} changes")

    async def dotzkeng_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(DOTZKENG_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] DOTZKENG LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = DOTZKENG_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] DOTZKENG LOOP #{worker_id} stopped after {success_count} changes")

    async def curly_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_WEB_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] CURLY LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_WEB_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] CURLY LOOP #{worker_id} stopped after {success_count} changes")

    async def gc_loop(self, chat_id, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] GC LOOP started for chat {chat_id}")
        image_paths = ["gc_image_1.png", "gc_image_2.png"]
        msg_index = 0
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    # Find which images exist
                    available_images = [p for p in image_paths if os.path.exists(p)]
                    
                    if available_images:
                        current_path = available_images[msg_index % len(available_images)]
                        with open(current_path, 'rb') as photo:
                            await context.bot.set_chat_photo(chat_id=chat_id, photo=photo)
                        success_count += 1
                        msg_index += 1
                        # Base delay for photo changes should be slightly higher to avoid immediate ban
                        await asyncio.sleep(max(delay, 2.0))
                    else:
                        await asyncio.sleep(5.0)
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except Exception as e:
                    print(f"[Bot {self.bot_number}] GC Error: {e}")
                    await asyncio.sleep(5.0)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] GC LOOP stopped after {success_count} changes")

    async def set_gc_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        message = update.message
        photo = None
        
        if message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo[-1]
        elif message.photo:
            photo = message.photo[-1]
            
        if not photo:
            await update.message.reply_text("Usage: Reply to a photo with -setgc [1 or 2] or send a photo with -setgc [1 or 2] caption")
            return
            
        # Determine slot
        slot = "1"
        if context.args:
            if context.args[0] in ["1", "2"]:
                slot = context.args[0]
            
        filename = f"gc_image_{slot}.png"
        file = await context.bot.get_file(photo.file_id)
        await file.download_to_drive(filename)
        await update.message.reply_text(f"Group image saved to Slot {slot}! ✅ Use -gc to start the loop cycling between available images.")

    async def ping_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        import time
        start_time = time.time()
        sent_message = await update.message.reply_text("Pinging...")
        end_time = time.time()
        
        latency = (end_time - start_time) * 1000
        await sent_message.edit_text(f"Bot {self.bot_number} Ping: {latency:.2f}ms ⚡")

    async def spam_loop(self, chat_id, target_name, context, worker_id):
        success_count = 0
        templates = [SPAM_MESSAGE_TEMPLATE, SPAM_MESSAGE_2, SPAM_MESSAGE_3]
        print(f"[Bot {self.bot_number}] Spam LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                # Smart Evasion: Randomized jitter (±15%) for un-patterned delivery
                jitter = delay * random.uniform(0.85, 1.15) if delay > 0 else random.uniform(0.1, 0.4)
                
                try:
                    # Message Rotation: Cycle through available templates automatically
                    template = templates[success_count % len(templates)]
                    spam_msg = template.format(target=target_name)
                    
                    await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                    success_count += 1
                    await asyncio.sleep(jitter)
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(1.0)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 1.0)
                    else:
                        await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Spam LOOP #{worker_id} stopped after {success_count} messages")

    async def reply_loop(self, chat_id, target_name, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] Reply LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                if chat_id in self.pending_replies and self.pending_replies[chat_id]:
                    async with self.get_lock(chat_id):
                        messages_to_reply = self.pending_replies[chat_id].copy()
                        self.pending_replies[chat_id] = []

                    for msg_id in messages_to_reply:
                        try:
                            reply_msg = random.choice(REPLY_MESSAGES).format(target=target_name)
                            await context.bot.send_message(
                                chat_id=chat_id, 
                                text=reply_msg,
                                reply_to_message_id=msg_id
                            )
                            success_count += 1
                            await asyncio.sleep(max(delay, 0.05))
                        except asyncio.CancelledError:
                            raise
                        except RetryAfter as e:
                            wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                            await asyncio.sleep(wait_time + 0.1)
                        except Exception:
                            await asyncio.sleep(0.5)
                else:
                    await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Reply LOOP stopped after {success_count} replies")

    async def message_collector(self, update, context):
        # We need to handle both message and channel_post
        msg = update.message or update.channel_post
        if not msg:
            return
            
        chat_id = update.effective_chat.id
        
        # Custom reaction logic
        if chat_id in self.active_react_chats:
            try:
                # Use set_message_reaction which is the modern method
                # Removing reaction limit checks for max speed
                await msg.react(reaction="💀")
            except Exception as e:
                # Fallback to bot method if message object reaction fails
                try:
                    await context.bot.set_message_reaction(
                        chat_id=chat_id,
                        message_id=msg.message_id,
                        reaction=[{"type": "emoji", "emoji": "💀"}]
                    )
                except Exception:
                    pass
                pass

        if not msg.text:
            return

        text = msg.text.lower()
        chat_id = update.effective_chat.id

        # Trigger for taixochutiya
        if "taixochutiya" in text:
            await update.message.reply_text("SUNNY Tᴇʀɪ ᴍᴏᴍ Cᴏᴍ Qᴜᴇᴇɴ 👑♥️")
            return

        if chat_id in self.active_reply_targets:
            msg_id = update.message.message_id
            async with self.get_lock(chat_id):
                if chat_id not in self.pending_replies:
                    self.pending_replies[chat_id] = []
                self.pending_replies[chat_id].append(msg_id)

    async def nc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /nc <name>")
            return

        base_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_name_change_tasks:
            old_tasks = self.active_name_change_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.name_change_loop(chat_id, base_name, context, i+1))
            tasks.append(task)

        self.active_name_change_tasks[chat_id] = tasks

        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ Name change LOOP started with {num_threads} threads!")

    async def stop_nc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_name_change_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Name change LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active name change loop!")

    async def spam_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /spam <target>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i+1))
            tasks.append(task)

        self.active_spam_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 💣 Spam LOOP started with {num_threads} threads! Running continuously...")

    async def stop_spam_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_spam_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Spam LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active spam loop!")

    async def target_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /target <name>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_name_change_tasks:
            old_tasks = self.active_name_change_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)

        nc_tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.name_change_loop(chat_id, target_name, context, i+1))
            nc_tasks.append(task)
        self.active_name_change_tasks[chat_id] = nc_tasks

        spam_tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i+1))
            spam_tasks.append(task)
        self.active_spam_tasks[chat_id] = spam_tasks

        total_threads = num_threads * 2
        await update.message.reply_text(f"[Bot {self.bot_number}] 🎯 TARGET MODE: NC ({num_threads}) + SPAM ({num_threads}) = {total_threads} threads running!")

    async def reply_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /reply <target>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_reply_tasks:
            old_task = self.active_reply_tasks[chat_id]
            old_task.cancel()
            try:
                await old_task
            except asyncio.CancelledError:
                pass

        self.active_reply_targets[chat_id] = target_name
        self.pending_replies[chat_id] = []

        task = asyncio.create_task(self.reply_loop(chat_id, target_name, context))
        self.active_reply_tasks[chat_id] = task

        await update.message.reply_text(f"[Bot {self.bot_number}] 💬 Reply LOOP activated! Replying to every message...")

    async def stop_reply_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_reply_tasks:
            task = self.active_reply_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_reply_tasks[chat_id]

        if chat_id in self.active_reply_targets:
            del self.active_reply_targets[chat_id]

        if chat_id in self.pending_replies:
            del self.pending_replies[chat_id]

        await update.message.reply_text(f"[Bot {self.bot_number}] Reply LOOP stopped!")

    async def delay_command(self, update, context):
        if not await self.check_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: /delay <seconds>")
            return

        try:
            delay = float(context.args[0])
            if delay < 0:
                await update.message.reply_text("Delay must be >= 0")
                return

            chat_id = update.effective_chat.id
            self.chat_delays[chat_id] = delay
            await update.message.reply_text(f"[Bot {self.bot_number}] Delay set to {delay}s (applies to all loops)")
        except ValueError:
            await update.message.reply_text("Invalid delay value!")

    async def threads_command(self, update, context):
        if not await self.check_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: /threads <number>")
            return

        try:
            threads = int(context.args[0])
            if threads < 1 or threads > 50:
                await update.message.reply_text("Threads must be between 1 and 50")
                return

            chat_id = update.effective_chat.id
            self.chat_threads[chat_id] = threads
            await update.message.reply_text(f"[Bot {self.bot_number}] Threads set to {threads} (applies to NC + SPAM)")
        except ValueError:
            await update.message.reply_text("Invalid threads value!")

    async def stop_all_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id
        stopped = []

        # List of all task categories to stop
        task_categories = [
            (self.active_name_change_tasks, "name change loop"),
            (self.active_ncheart_tasks, "nc heart loop"),
            (self.active_ncflag_tasks, "nc flag loop"),
            (self.active_dotzkeng_tasks, "dotzkeng loop"),
            (self.active_curly_tasks, "curly loop"),
            (self.active_spam_tasks, "spam loop")
        ]

        for task_dict, label in task_categories:
            if chat_id in task_dict:
                tasks = task_dict[chat_id]
                # Handle both list of tasks and single task
                if not isinstance(tasks, list):
                    tasks = [tasks]
                for task in tasks:
                    task.cancel()
                for task in tasks:
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                del task_dict[chat_id]
                stopped.append(label)

        if chat_id in self.active_reply_tasks:
            task = self.active_reply_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_reply_tasks[chat_id]
            stopped.append("reply loop")

        if chat_id in self.active_reply_targets:
            del self.active_reply_targets[chat_id]

        if chat_id in self.pending_replies:
            del self.pending_replies[chat_id]

        if hasattr(self, 'active_gc_tasks') and chat_id in self.active_gc_tasks:
            task = self.active_gc_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_gc_tasks[chat_id]
            stopped.append("gc loop")

        if stopped:
            await update.message.reply_text(f"[Bot {self.bot_number}] Stopped: {', '.join(stopped)} ✅")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active loops to stop!")

    async def flower_nc_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: -flowernc <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        
        # Stop existing loops in this category
        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks: task.cancel()
            del self.active_name_change_tasks[chat_id]
            
        task = asyncio.create_task(self.flower_nc_loop(chat_id, base_name, context))
        self.active_name_change_tasks[chat_id] = [task]
        await update.message.reply_text(f"[Bot {self.bot_number}] 🌸 FLOWER NC LOOP started!")

    async def nc_emo_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncemo <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks: task.cancel()
            del self.active_name_change_tasks[chat_id]
        task = asyncio.create_task(self.nc_emo_loop(chat_id, base_name, context))
        self.active_name_change_tasks[chat_id] = [task]
        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ NC EMO LOOP started!")

    async def ncheart_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncheart <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_ncheart_tasks:
            old_tasks = self.active_ncheart_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.nc_heart_loop(chat_id, base_name, context, i+1))
            tasks.append(task)
        self.active_ncheart_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 🌙 NC heart LOOP started with {num_threads} threads!")

    async def stop_ncheart_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_ncheart_tasks:
            tasks = self.active_ncheart_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_ncheart_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] NC heart LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active NC heart loop!")

    async def ncflag_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncflag <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_ncflag_tasks:
            old_tasks = self.active_ncflag_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.nc_flag_loop(chat_id, base_name, context, i+1))
            tasks.append(task)
        self.active_ncflag_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 🚩 NC FLAG LOOP started with {num_threads} threads!")

    async def stop_ncflag_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_ncflag_tasks:
            tasks = self.active_ncflag_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_ncflag_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] NC FLAG LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active NC Flag loop!")

    async def dotzkeng_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: -dotzkeng <name>")
            return

        base_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_dotzkeng_tasks:
            old_tasks = self.active_dotzkeng_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.dotzkeng_loop(chat_id, base_name, context, i+1))
            tasks.append(task)

        self.active_dotzkeng_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ DOTZKENG LOOP started with {num_threads} threads!")

    async def stop_dotzkeng_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_dotzkeng_tasks:
            tasks = self.active_dotzkeng_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_dotzkeng_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] DOTZKENG LOOP stopped!")
        else:
            await update.message.reply_text("No active DOTZKENG LOOP found.")

    async def nccurly_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: -nccurly <name>")
            return
        
        target_name = " ".join(context.args)
        chat_id = chat.id
        threads = self.chat_threads.get(chat_id, 1)

        if chat_id in self.active_curly_tasks:
            for task in self.active_curly_tasks[chat_id]:
                task.cancel()
        
        self.active_curly_tasks[chat_id] = []
        for i in range(threads):
            task = asyncio.create_task(self.curly_loop(chat_id, target_name, context, i+1))
            self.active_curly_tasks[chat_id].append(task)
        
        await update.message.reply_text(f"[Bot {self.bot_number}] Double Curly loop started for '{target_name}' with {threads} threads! 🌀")

    async def stop_nccurly_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_curly_tasks:
            for task in self.active_curly_tasks[chat_id]:
                task.cancel()
            for task in self.active_curly_tasks[chat_id]:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_curly_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Double Curly loop stopped! 🛑")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active Double Curly loop!")

    async def gc_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        chat_id = chat.id
        task = asyncio.create_task(self.gc_loop(chat_id, context))
        # Store in a new dict or reuse active_spam_tasks if appropriate
        if not hasattr(self, 'active_gc_tasks'): self.active_gc_tasks = {}
        self.active_gc_tasks[chat_id] = task
        await update.message.reply_text(f"[Bot {self.bot_number}] 🖼️ Group Image Change LOOP started!")


def create_bot_application(token, bot_number, owner_id):
    application = Application.builder().token(token).build()
    bot_instance = BotInstance(bot_number, owner_id)

    # Standard command handlers
    application.add_handler(CommandHandler("start", bot_instance.start))
    application.add_handler(CommandHandler("nc", bot_instance.nc_command))
    application.add_handler(CommandHandler("ncemo", bot_instance.nc_emo_command))
    application.add_handler(CommandHandler("ncheart", bot_instance.ncheart_command))
    application.add_handler(CommandHandler("ncflag", bot_instance.ncflag_command))
    application.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))
    application.add_handler(CommandHandler("stopncheart", bot_instance.stop_ncheart_command))
    application.add_handler(CommandHandler("stopncflag", bot_instance.stop_ncflag_command))
    application.add_handler(CommandHandler("spam", bot_instance.spam_command))
    application.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))
    application.add_handler(CommandHandler("target", bot_instance.target_command))
    application.add_handler(CommandHandler("reply", bot_instance.reply_command))
    application.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))
    application.add_handler(CommandHandler("delay", bot_instance.delay_command))
    application.add_handler(CommandHandler("threads", bot_instance.threads_command))
    application.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
    application.add_handler(CommandHandler("gc", bot_instance.gc_command))
    application.add_handler(CommandHandler("sudo", bot_instance.sudo_command))

    # Custom handler for prefix '-'
    async def prefix_handler(update, context):
        if not update.message or not update.message.text:
            return
        text = update.message.text
        if text.startswith('-'):
            parts = text[1:].split()
            if not parts:
                return
            command = parts[0].lower()
            context.args = parts[1:]
            
            cmd_map = {
                "start": bot_instance.start,
                "nc": bot_instance.nc_command,
                "stopnc": bot_instance.stop_nc_command,
                "spam": bot_instance.spam_command,
                "stopspam": bot_instance.stop_spam_command,
                "delay": bot_instance.delay_command,
                "threads": bot_instance.threads_command,
                "target": bot_instance.target_command,
                "stopall": bot_instance.stop_all_command,
                "ncheart": bot_instance.ncheart_command,
                "stopncheart": bot_instance.stop_ncheart_command,
                "ncflag": bot_instance.ncflag_command,
                "stopncflag": bot_instance.stop_ncflag_command,
                "dotzkeng": bot_instance.dotzkeng_command,
                "stopdotzkeng": bot_instance.stop_dotzkeng_command,
                "flowernc": bot_instance.flower_nc_command,
                "ncemo": bot_instance.nc_emo_command,
                "reply": bot_instance.reply_command,
                "stopreply": bot_instance.stop_reply_command,
                "gc": bot_instance.gc_command,
                "sudo": bot_instance.sudo_command,
                "refresh": bot_instance.refresh_command,
            }
            
            if command in cmd_map:
                await cmd_map[command](update, context)
            elif command == "flowernc":
                await bot_instance.flower_nc_command(update, context)

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), prefix_handler))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, bot_instance.message_collector))

    return application


async def run_bot(token, bot_number, owner_id):
    max_retries = 30
    retry_delay = 15
    
    # Load proxies
    proxies = []
    if os.path.exists("proxies.txt"):
        try:
            with open("proxies.txt", "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
        except Exception:
            pass

    for attempt in range(max_retries):
        bot_instance = BotInstance(bot_number, owner_id)
        
        # Assign proxy if available
        proxy_url = None
        if proxies:
            proxy_url = proxies[(bot_number - 1) % len(proxies)]
            bot_instance.proxy = proxy_url

        request = None
        if proxy_url:
            request = HTTPXRequest(proxy_url=proxy_url)

        builder = Application.builder().token(token)
        if request:
            builder.request(request)
        application = builder.build()
        
        # Standard command handlers
        application.add_handler(CommandHandler("start", bot_instance.start))
        application.add_handler(CommandHandler("nc", bot_instance.nc_command))
        application.add_handler(CommandHandler("ncemo", bot_instance.nc_emo_command))
        application.add_handler(CommandHandler("ncheart", bot_instance.ncheart_command))
        application.add_handler(CommandHandler("ncflag", bot_instance.ncflag_command))
        application.add_handler(CommandHandler("nccurly", bot_instance.nccurly_command))
        application.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))
        application.add_handler(CommandHandler("stopncheart", bot_instance.stop_ncheart_command))
        application.add_handler(CommandHandler("stopncflag", bot_instance.stop_ncflag_command))
        application.add_handler(CommandHandler("stopnccurly", bot_instance.stop_nccurly_command))
        application.add_handler(CommandHandler("dotzkeng", bot_instance.dotzkeng_command))
        application.add_handler(CommandHandler("stopdotzkeng", bot_instance.stop_dotzkeng_command))
        application.add_handler(CommandHandler("flowernc", bot_instance.flower_nc_command))
        application.add_handler(CommandHandler("spam", bot_instance.spam_command))
        application.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))
        application.add_handler(CommandHandler("target", bot_instance.target_command))
        application.add_handler(CommandHandler("reply", bot_instance.reply_command))
        application.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))
        application.add_handler(CommandHandler("delay", bot_instance.delay_command))
        application.add_handler(CommandHandler("threads", bot_instance.threads_command))
        application.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
        application.add_handler(CommandHandler("gc", bot_instance.gc_command))
        application.add_handler(CommandHandler("setgc", bot_instance.set_gc_command))
        application.add_handler(CommandHandler("ping", bot_instance.ping_command))
        application.add_handler(CommandHandler("sudo", bot_instance.sudo_command))
        application.add_handler(CommandHandler("proxy", bot_instance.proxy_command))
        application.add_handler(CommandHandler("refresh", bot_instance.refresh_command))

        # Custom handler for prefix '-'
        async def prefix_handler(update, context):
            if not update.message or not update.message.text:
                return
            text = update.message.text
            if text.startswith('-'):
                parts = text[1:].split()
                if not parts:
                    return
                command = parts[0].lower()
                context.args = parts[1:]
                
                cmd_map = {
                    "start": bot_instance.start,
                    "nc": bot_instance.nc_command,
                    "stopnc": bot_instance.stop_nc_command,
                    "spam": bot_instance.spam_command,
                    "stopspam": bot_instance.stop_spam_command,
                    "delay": bot_instance.delay_command,
                    "threads": bot_instance.threads_command,
                    "target": bot_instance.target_command,
                    "stopall": bot_instance.stop_all_command,
                    "ncheart": bot_instance.ncheart_command,
                    "stopncheart": bot_instance.stop_ncheart_command,
                    "ncflag": bot_instance.ncflag_command,
                    "stopncflag": bot_instance.stop_ncflag_command,
                    "nccurly": bot_instance.nccurly_command,
                    "stopnccurly": bot_instance.stop_nccurly_command,
                    "dotzkeng": bot_instance.dotzkeng_command,
                    "stopdotzkeng": bot_instance.stop_dotzkeng_command,
                    "flowernc": bot_instance.flower_nc_command,
                    "ncemo": bot_instance.nc_emo_command,
                    "ownrp": bot_instance.ownrp_command,
                    "timenc": bot_instance.time_nc_command,
                    "stoptimenc": bot_instance.stop_time_nc,
                    "react": bot_instance.react_command,
                    "multispam": bot_instance.multispam_command,
                    "autoname": bot_instance.auto_name_command,
                    "stopautoname": bot_instance.stop_auto_name,
                    "reply": bot_instance.reply_command,
                    "stopreply": bot_instance.stop_reply_command,
                    "ping": bot_instance.ping_command,
                    "gc": bot_instance.gc_command,
                    "setgc": bot_instance.set_gc_command,
                    "sudo": bot_instance.sudo_command,
                    "proxy": bot_instance.proxy_command,
                    "join": bot_instance.join_command,
                    "refresh": bot_instance.refresh_command,
                }
                
                if command in cmd_map:
                    await cmd_map[command](update, context)
            else:
                await bot_instance.message_collector(update, context)

        application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), prefix_handler))

        try:
            await application.initialize()
            await application.start()
            if application.updater:
                # Removed large stagger per user request for 1s startup
                await asyncio.sleep(0.1)
                await application.updater.start_polling(drop_pending_updates=True)
            print(f"Bot {bot_number} started successfully!")

            while True:
                await asyncio.sleep(3600)

        except Exception as e:
            error_str = str(e).lower()
            if "conflict" in error_str:
                print(f"Bot {bot_number} conflict (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                try:
                    if application.updater:
                        await application.updater.stop()
                    await application.stop()
                    await application.shutdown()
                except Exception:
                    pass
                await asyncio.sleep(retry_delay)
                # More aggressive exponential backoff for conflicts
                retry_delay = min(retry_delay + 15, 300)
                continue
            else:
                print(f"Bot {bot_number} error: {e}")
                break
        finally:
            try:
                if application.updater:
                    await application.updater.stop()
                await application.stop()
                await application.shutdown()
            except Exception:
                pass
        break
    else:
        print(f"Bot {bot_number} failed after {max_retries} attempts - token may be used elsewhere")

async def main():
    print(f"Starting {len(BOT_TOKENS)} bots for owner ID: {OWNER_ID}")
    print("All actions (name change, spam, reply) run in LOOPS!")

    tasks = []
    for i, token in enumerate(BOT_TOKENS, 1):
        task = asyncio.create_task(run_bot(token, i, OWNER_ID))
        tasks.append(task)
        # Stagger slightly to allow some breathing room but fast enough for 1s total
        await asyncio.sleep(0.05)

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\nShutting down all bots...")


if __name__ == "__main__":
    asyncio.run(main())

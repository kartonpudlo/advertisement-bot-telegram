from telethon import TelegramClient, errors
import asyncio
import logging
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler

# Ustawienia dla Rich
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    datefmt='[%X]',
    handlers=[RichHandler(console=console, show_time=False, show_path=False)]
)
logger = logging.getLogger('pieklobot')

# Twoje dane z my.telegram.org
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'  


MESSAGE_LINK = 'YOUR_MESSAGE_LINK'
GROUP_IDS = [YOUR, GRUOP, ID]

# TIME INTERVAL
INTERVAL = 900 

async def forward_message(client):
    try:
        message_id = int(MESSAGE_LINK.split('/')[-1])
        
        # Próbuj pobrać wiadomość z określonego czatu
        chat_id = 'YOUR_NAME_GRUOP_FROM_LINK'  # Zaktualizuj na właściwy czat
        logger.info(f'🌐 Próba pobrania wiadomości {message_id} z czatu {chat_id}')
        message = await client.get_messages(chat_id, ids=message_id)
        
        if message:
            # Przekaż wiadomość do grup
            for group_id in GROUP_IDS:
                try:
                    await client.forward_messages(group_id, message)
                    group_name = f'Grupa {group_id}'
                    logger.info(f'✅ Wiadomość {message_id} przekazana do grupy {group_name} o {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                except errors.ChatAdminRequiredError:
                    logger.error(f'🚫 Błąd: Brak uprawnień administratora w grupie {group_id}')
                except Exception as e:
                    logger.error(f'❌ Błąd przy przekazywaniu wiadomości {message_id} do grupy {group_id}: {e}')
        else:
            logger.info(f'🔍 Wiadomość o ID {message_id} nie została znaleziona.')
    except Exception as e:
        logger.error(f'❗ Nie udało się pobrać wiadomości z linku: {e}')

async def main():
    # Utwórz klienta Telegram i zaloguj się jako użytkownik
    session_file = 'unique_session_name.session'
    client = TelegramClient(session_file, api_id, api_hash)
    await client.start(phone=phone_number)
    logger.info('🚀 [bold cyan]Zalogowano jako użytkownik.[/bold cyan]')

    # Pętla główna, która co INTERVAL czasu przekazuje wiadomość
    while True:
        await forward_message(client)
        await asyncio.sleep(INTERVAL)

if __name__ == '__main__':
    asyncio.run(main())

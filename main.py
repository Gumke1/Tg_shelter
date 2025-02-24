import asyncio
from bot import main

if __name__ == "__main__": #Запуск бота
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('off')
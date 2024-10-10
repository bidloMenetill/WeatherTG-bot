

from aiogram import Bot, Dispatcher
import  asyncio
from handlers import router

bot = Bot(token="7702264804:AAHxUX7VHyKL2pKfDpKkGG-rv67nZNOopEI")
dp= Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
if __name__ == "__main__":
   try:
        asyncio.run(main())
   except KeyboardInterrupt:
        print("Бот выключен") 

 
      
 


















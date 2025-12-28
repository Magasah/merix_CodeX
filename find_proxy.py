"""
Скрипт для автоматического поиска и тестирования рабочих SOCKS5 прокси
"""
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
import time

# Список прокси для тестирования (обновляется ежедневно)
PROXY_LIST = [
    "socks5://98.162.25.4:31679",
    "socks5://98.162.25.7:31665",
    "socks5://72.210.221.223:4145",
    "socks5://184.178.172.28:15294",
    "socks5://184.178.172.17:4145",
    "socks5://192.252.211.197:14921",
    "socks5://192.252.208.70:14282",
    "socks5://72.195.34.60:27391",
    "socks5://72.195.34.42:4145",
    "socks5://72.210.252.134:46164",
]

BOT_TOKEN = "8308229352:AAEYG58uicc3rc_r7iBrcJH9eYP8-aWfa5E"
TEST_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"


async def test_proxy(proxy_url, timeout=10):
    """Тестирует прокси на подключение к Telegram API"""
    try:
        connector = ProxyConnector.from_url(proxy_url)
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            start_time = time.time()
            async with session.get(TEST_URL) as response:
                if response.status == 200:
                    elapsed = time.time() - start_time
                    data = await response.json()
                    if data.get('ok'):
                        return True, elapsed, proxy_url
        return False, None, proxy_url
    except Exception as e:
        return False, None, proxy_url


async def find_working_proxy():
    """Находит рабочий прокси из списка"""
    print("🔍 Поиск рабочего прокси для Telegram API...\n")
    
    tasks = [test_proxy(proxy) for proxy in PROXY_LIST]
    results = await asyncio.gather(*tasks)
    
    working_proxies = []
    
    for success, speed, proxy_url in results:
        proxy_display = proxy_url.split('://')[1]
        if success:
            print(f"✅ {proxy_display} - работает! ({speed:.2f}s)")
            working_proxies.append((proxy_url, speed))
        else:
            print(f"❌ {proxy_display} - не работает")
    
    if working_proxies:
        # Сортируем по скорости
        working_proxies.sort(key=lambda x: x[1])
        print(f"\n🎯 Найдено рабочих прокси: {len(working_proxies)}")
        print(f"\n⚡ Самый быстрый прокси: {working_proxies[0][0]} ({working_proxies[0][1]:.2f}s)")
        print(f"\n📝 Добавьте в .env файл:")
        print(f"PROXY_URL={working_proxies[0][0]}")
        return working_proxies[0][0]
    else:
        print("\n❌ Ни один прокси не работает!")
        print("\n💡 Рекомендации:")
        print("1. Используйте VPN (ProtonVPN, Windscribe, 1.1.1.1)")
        print("2. Купите платный прокси (Proxy6.net - от 50₽/месяц)")
        print("3. Обновите список прокси на https://www.proxy-list.download/SOCKS5")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("  Telegram Bot Proxy Finder - Merix CodeX")
    print("=" * 60)
    print()
    
    proxy = asyncio.run(find_working_proxy())
    
    if proxy:
        print("\n✅ Готово! Теперь запустите бота: python main.py")
    else:
        print("\n⚠️ Необходимо использовать VPN или платный прокси")
    
    print("\n" + "=" * 60)
    input("\nНажмите Enter для выхода...")

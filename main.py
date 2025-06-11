import asyncio
import os
import logging
from src.processor.process import process_set_async

BASE_DIR = 'rpa_test_data_all_sets'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("logs.log")]
)
logger = logging.getLogger(__name__)


async def main():
    tasks = []
    for name in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, name)
        if os.path.isdir(path) and name.startswith('set_'):
            tasks.append(process_set_async(path))
    results = await asyncio.gather(*tasks)

    for result in results:
        logger.info(f"📦 Набор: {result['set_name']}")

        logger.info(f"✅ Успешно создано заявок: {result['success_count']}")
        for s in result.get('successful_ids', []):
            logger.info(f"  - {s['client_id']}: заявка создана")

        logger.info(f"❌ Отказы: {len(result['refusals'])}")
        for r in result['refusals']:
            logger.info(f"  - {r['client_id']}: {r['reason']}")

        logger.info("-" * 40)


if __name__ == '__main__':
    asyncio.run(main())

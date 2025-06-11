import os
import logging
from src.processor.const import AVAILABLE_PORTS
from src.processor.utils import read_json, read_coverage, write_json

logger = logging.getLogger(__name__)


async def process_set_async(set_path):
    try:
        clients = await read_json(os.path.join(set_path, 'clients.json'))
        coverage = await read_coverage(os.path.join(set_path, 'coverage_list.txt'))
        used_ports_data = await read_json(os.path.join(set_path, 'used_ports.json'))
        used_ports = set(used_ports_data.get("used_ports", []))
    except Exception as e:
        logger.error(f"Ошибка при чтении данных из файлов: {e}")
        return {
            "set_name": os.path.basename(set_path),
            "success_count": 0,
            "refusals": [{"client_id": "unknown", "reason": f"ошибка чтения файлов: {str(e)}"}],
            "successful_ids": [],
        }

    free_ports = list(AVAILABLE_PORTS - used_ports)
    crm_requests = []
    refusals = []
    successful_ids = []

    for client in clients:
        try:
            client_id = client.get("client_id")
            address = client.get("address")
            request_date = client.get("request_date")

            if not client_id or not address or not request_date:
                refusals.append({
                    "client_id": client_id or None,
                    "reason": "неполные данные"
                })
                continue

            if address not in coverage:
                refusals.append({"client_id": client_id, "reason": "нет покрытия"})
                continue

            if not free_ports:
                refusals.append({"client_id": client_id, "reason": "нет свободных портов"})
                continue

            assigned_port = free_ports.pop(0)
            used_ports.add(assigned_port)

            crm_requests.append({
                "client_id": client_id,
                "address": address,
                "assigned_port": assigned_port,
                "request_date": request_date
            })
            successful_ids.append({"client_id": client_id})

        except Exception as e:
            logger.warning(f"Ошибка при обработке клиента {client.get('client_id', 'unknown')}: {e}")
            refusals.append({
                "client_id": client.get("client_id", "unknown"),
                "reason": f"ошибка при обработке заявки: {str(e)}"
            })

    try:
        await write_json(os.path.join(set_path, 'crm_requests.json'), crm_requests)
    except Exception as e:
        logger.error(f"Ошибка при записи crm_requests.json: {e}")
        refusals.append({
            "client_id": "all",
            "reason": f"ошибка записи CRM-заявок: {str(e)}"
        })

    return {
        "set_name": os.path.basename(set_path),
        "success_count": len(crm_requests),
        "refusals": refusals,
        "successful_ids": successful_ids,
    }

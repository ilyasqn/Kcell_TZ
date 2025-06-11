import aiofiles
import json
from pathlib import Path


async def read_json(file_path):
    async with aiofiles.open(file_path, encoding='utf-8') as f:
        content = await f.read()
        return json.loads(content)


async def read_coverage(file_path):
    async with aiofiles.open(file_path, encoding='utf-8') as f:
        lines = await f.readlines()
        return set(line.strip() for line in lines)


async def write_json(file_path, data):
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))


async def load_json(path: Path):
    async with aiofiles.open(path, encoding='utf-8') as file:
        content = await file.read()
        return json.loads(content)


async def load_coverage(path: Path):
    async with aiofiles.open(path, encoding='utf-8') as file:
        lines = await file.readlines()
        return {line.strip() for line in lines if line.strip()}


async def save_json(data, path: Path):
    async with aiofiles.open(path, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=2))

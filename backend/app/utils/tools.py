#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, List, Dict, Sequence, Optional, Union
import importlib, uuid, random, os
from pathlib import Path
from app.shared.crud.base import ModelType
from app.models.base import Model
from sqlalchemy.sql.elements import ColumnElement
from fastapi import UploadFile
from app.config.setting import settings
from app.config.path_conf import APP_DIR
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def import_module(module: str) -> Any:
    """
    导入模块
    :param module: 模块名称
    :return: 模块对象
    """
    module_path, module_class = module.rsplit(".", 1)
    module = importlib.import_module(module_path)
    cls = getattr(module, module_class)
    return cls


def dict_to_search_sql(model: ModelType, search: Dict) -> List[ColumnElement]:
    """
    用于搜索的参数字典转sql表达式数组
    :param model: 模型对象
    :param search: 搜索参数
    :return: sql表达式数组
    """
    sql_where = []

    for key, value in search.items():
        seq = None

        if isinstance(value, tuple):
            seq, value = value

        if value is None:
            continue

        if seq == "like":
            sql_where.append(getattr(model, key).like(f"%{value}%"))

        if seq == "in":
            sql_where.append(getattr(model, key).in_(value))

        if seq == "between":
            start, end = value
            if not start or not end:
                continue
            sql_where.append(getattr(model, key).between(*value))

        if seq is None:
            sql_where.append(getattr(model, key) == value)

    return sql_where


def get_random_character() -> str:
    """
    获取随机字符
    :return: 随机字符串
    """
    return uuid.uuid4().hex


def _load_captcha_font(size: int = 42) -> Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]:
    """按绝对路径加载验证码字体，缺失时回退到系统字体。"""
    windir = Path(os.environ.get("WINDIR", r"C:\Windows"))
    candidates = [
        APP_DIR / "resources" / "gantians.otf",
        APP_DIR / "resources" / "captcha.ttf",
        windir / "Fonts" / "arial.ttf",
        windir / "Fonts" / "segoeui.ttf",
        windir / "Fonts" / "consola.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    ]
    for font_path in candidates:
        if not font_path.is_file():
            continue
        try:
            return ImageFont.truetype(str(font_path), size)
        except OSError:
            continue
    return ImageFont.load_default()



def generate_captcha(code) -> BytesIO:
    """
    生成带有噪声和干扰的验证码图片
    :return: 验证码图片流
    """

    background_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
    width, height = 160, 60
    image = Image.new('RGB', (width, height), color=background_color)


    draw = ImageDraw.Draw(image)
    font = _load_captcha_font(42)

    # 计算验证码文本的总宽度
    total_text_width = 0
    for char in code:

        bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), char, font=font)
        text_width = bbox[2] - bbox[0]
        total_text_width += text_width


    x_offset = (width - total_text_width) / 2

    bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), code[0], font=font)
    text_height = bbox[3] - bbox[1]
    y_offset = (height - text_height) / 2 - draw.textbbox((0, 0), code[0], font=font)[1]


    for char in code:

        text_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))


        bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), char, font=font)
        char_width = bbox[2] - bbox[0]
        char_x = x_offset + random.uniform(-3, 3)
        char_y = y_offset + random.uniform(-5, 5)


        draw.text((char_x, char_y), char, font=font, fill=text_color)


        x_offset += char_width + random.uniform(2, 8)


    for _ in range(random.randint(2, 4)):
        # 随机位置和大小
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(5, 10)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=text_color)


    for _ in range(random.randint(10, 20)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        noise_size = random.randint(2, 4)
        noise_color = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
        draw.rectangle([x, y, x + noise_size, y + noise_size], fill=noise_color)


    stream = BytesIO()
    image.save(stream, format='PNG')

    return stream


def get_parent_id_map(model_list: Sequence[Model]) -> Dict[int, int]:
    """
    获取父级ID的映射集
    :param model_list: 模型数组
    :return: 映射集字典
    """
    data_map = {item.id: item.parent_id for item in model_list}
    return data_map


def get_parent_recursion(
        id: int,
        id_map: Dict[int, int],
        ids: Optional[List[int]] = None
) -> List[int]:
    """
    递归获取某ID的所有父级的ID数组
    :param id: ID
    :param id_map: ID的映射集
    :param ids: ID数组
    :return: 所有父级的ID数组
    """
    if ids is None:
        ids = []

    ids.append(id)
    parent_id = id_map.get(id)
    if parent_id:
        get_parent_recursion(parent_id, id_map, ids)

    return ids


def get_child_id_map(model_list: Sequence[Model]) -> Dict[int, List[int]]:
    """
    获取子级ID的映射集
    :param model_list: 模型数组
    :return: 映射集字典
    """
    data_map = {}
    for model in model_list:
        data_map.setdefault(model.id, [])
        if model.parent_id:
            data_map.setdefault(model.parent_id, []).append(model.id)

    return data_map


def get_child_recursion(
        id: int,
        id_map: Dict[int, List[int]],
        ids: Optional[List[int]] = None
) -> List[int]:
    """
    递归获取某ID的所有子级的ID数组
    :param id: ID
    :param id_map: ID的映射集
    :param ids: ID数组
    :return: 所有子级的ID数组
    """
    if ids is None:
        ids = []

    ids.append(id)
    child_ids = id_map.get(id, [])
    for child in child_ids:
        get_child_recursion(child, id_map, ids)

    return ids


async def upload_image(file: UploadFile, dirname: str) -> Optional[str]:
    """图片上传，走统一存储，返回访问 URL。"""
    from pathlib import Path

    from app.utils.storage import StorageFactory

    ext = Path(file.filename or "").suffix.lower()
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"}
    content_type = (file.content_type or "").lower()
    is_image = "image" in content_type or ext in image_exts
    if not is_image:
        return None

    content = await file.read()
    max_bytes = settings.UPLOAD_MAX_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        return None
    await file.seek(0)

    storage = StorageFactory.create()
    result = await storage.upload(file, dirname)
    return result.get("url")

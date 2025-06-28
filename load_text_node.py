# load_text_node.py

import os
import re
from pypinyin import lazy_pinyin, Style

class LoadTextFromFolder:
    """
    A node to load text files from a specific directory and select one using an index.
    Supports natural sorting of filenames with Chinese, English, and numbers.
    Outputs: content, file name (without extension), and index of the selected .txt file.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {
                    "default": "/path/to/txt/files",
                    "multiline": False,
                    "lazy": True
                }),
                "start_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1,
                    "display": "number",
                    "lazy": True
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")  # 输出顺序：content, file_name, index
    RETURN_NAMES = ("content", "file_name", "index")
    FUNCTION = "load_text"
    CATEGORY = "Example"

    def check_lazy_status(self, directory, start_index):
        return ["directory", "start_index"]

    def load_text(self, directory, start_index):
        if not os.path.isdir(directory):
            raise ValueError(f"The provided path is not a valid directory: {directory}")

        # 获取所有 .txt 文件
        all_files = [f for f in os.listdir(directory) if f.endswith(".txt")]

        # 按拼音 + 自然排序
        txt_files = sorted(all_files, key=self._chinese_natural_key)

        if not txt_files:
            raise ValueError(f"No .txt files found in directory: {directory}")

        # 确保索引不越界
        index = min(start_index, len(txt_files) - 1)
        selected_file = txt_files[index]
        file_path = os.path.join(directory, selected_file)

        # 去除 .txt 后缀
        file_name = os.path.splitext(selected_file)[0]

        # 读取文件内容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read file '{selected_file}': {str(e)}")

        return (content, file_name, index)

    # 辅助函数：生成用于排序的键（中文转拼音 + 数字识别）
    def _chinese_natural_key(self, s):
        """将字符串拆分为中文、英文、数字部分，用于排序"""
        def convert(text):
            if text.isdigit():
                return int(text)
            else:
                return lazy_pinyin(text, style=Style.NORMAL)

        parts = re.split(r'(\d+)', s)
        return [convert(part) for part in parts]

    # 可选调试方法：打印排序结果
    def _debug_print_sorted_files(self, files):
        print("Sorted Files:")
        for i, f in enumerate(files):
            print(f"{i}: {f}")
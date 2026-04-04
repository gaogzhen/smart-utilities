#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

POSTS_DIR = '/Users/gaogzhen/blog/blog-source/source/_posts'

def replace_toc_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经包含目标占位符，避免重复替换
    if '<!-- toc -->' in content:
        print(f'跳过 (已包含): {filepath}')
        return

    # 替换 [TOC] 为 <!-- toc -->，考虑可能的空格和换行
    new_content = re.sub(r'\[TOC\]', '<!-- toc -->', content, flags=re.IGNORECASE)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'已替换: {filepath}')
    else:
        print(f'无变化: {filepath}')

def main():
    print("即将把 source/_posts 下所有 .md 文件中的 [TOC] 替换为 <!-- toc -->")
    print("请确保已备份 source/_posts 目录！")
    confirm = input("输入 y 继续，其他任意键取消: ")
    if confirm.lower() != 'y':
        print("已取消。")
        return

    count = 0
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                replace_toc_in_file(filepath)
                count += 1
    print(f"处理完成，共检查 {count} 个文件。")

if __name__ == '__main__':
    main()
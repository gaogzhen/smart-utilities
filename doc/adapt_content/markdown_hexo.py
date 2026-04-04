#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
from datetime import datetime

POSTS_DIR = '/Users/gaogzhen/blog/github/source/_posts'

def ensure_front_matter(content, filepath):
    # 去除可能存在的 UTF-8 BOM
    if content.startswith('\ufeff'):
        content = content[1:]
    stripped = content.lstrip()
    # 只有文件开头（去除空白后）以 '---' 开头才认为已有 Front-matter
    if stripped.startswith('---'):
        return content, False

    # 生成默认 Front-matter
    filename = os.path.basename(filepath)
    title = os.path.splitext(filename)[0]
    mtime = os.path.getmtime(filepath)
    date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

    front_matter = f'''---
title: {title}
date: {date_str}
categories: 
tags:
---

'''
    new_content = front_matter + content
    return new_content, True

def convert_image_links(content, rel_dir):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    def repl(match):
        alt = match.group(1)
        link = match.group(2).strip()
        if link.startswith(('http://', 'https://', '/')):
            return f'![{alt}]({link})'
        if rel_dir:
            new_link = '/' + rel_dir.replace('\\', '/') + '/' + link
        else:
            new_link = '/' + link
        return f'![{alt}]({new_link})'
    new_content = re.sub(pattern, repl, content)
    return new_content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # 1. 处理 Front-matter
    content_after_fm, fm_added = ensure_front_matter(original_content, filepath)

    # 2. 处理图片链接
    abs_posts_dir = os.path.abspath(POSTS_DIR)
    abs_file = os.path.abspath(filepath)
    rel_path = os.path.relpath(os.path.dirname(abs_file), abs_posts_dir)
    rel_dir = '' if rel_path == '.' else rel_path

    final_content = convert_image_links(content_after_fm, rel_dir)

    # 3. 判断是否有任何修改（比较最终内容和原始内容）
    if final_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f'更新: {filepath} (Front-matter: {fm_added}, 图片链接: {final_content != content_after_fm})')
    else:
        print(f'无需修改: {filepath}')

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f'错误：找不到目录 "{POSTS_DIR}"')
        return
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.lower().endswith('.md'):
                filepath = os.path.join(root, file)
                process_file(filepath)
    print('处理完成。')

if __name__ == '__main__':
    main()
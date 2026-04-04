#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

POSTS_DIR = '/Users/gaogzhen/blog/github/source/_posts'

def add_mathjax_to_front_matter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 定位 Front-matter 边界
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        print(f'无 Front-matter: {filepath}')
        return

    fm_text = fm_match.group(1)
    # 检查是否已有 mathjax 字段
    if re.search(r'^mathjax:', fm_text, re.MULTILINE):
        print(f'已存在 mathjax: {filepath}')
        return

    # 在 Front-matter 末尾（即结束 --- 之前）插入 mathjax: true
    # 这里简单地在最后一行前插入，也可以选择在 tags 后插入
    new_fm = fm_text + '\nmathjax: true'
    new_content = content.replace(fm_text, new_fm, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'已添加 mathjax: {filepath}')

def main():
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                add_mathjax_to_front_matter(filepath)
    print('批量处理完成。')

if __name__ == '__main__':
    print('请确保已备份 source/_posts 目录！')
    confirm = input('输入 y 继续: ')
    if confirm.lower() == 'y':
        main()
    else:
        print('已取消。')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

POSTS_DIR = '/Users/gaogzhen/blog/github/source/_posts'

def wrap_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.strip().startswith('{% raw %}') and content.strip().endswith('{% endraw %}'):
        print(f'跳过（已包裹）: {filepath}')
        return
    new_content = '{% raw %}\n' + content + '\n{% endraw %}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'已包裹: {filepath}')

def main():
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith('.md'):
                wrap_file(os.path.join(root, file))
    print('批量包裹完成。')

if __name__ == '__main__':
    main()
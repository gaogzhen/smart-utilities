#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

POSTS_DIR = '/Users/gaogzhen/blog/blog-source/source/_posts'

def wrap_file_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 分离 Front-matter 和正文
    # 匹配以 --- 开头和结尾的部分
    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if fm_match:
        front_matter = fm_match.group(0)  # 包含 --- 的整个 Front-matter
        body = content[fm_match.end():]   # 正文部分
    else:
        # 理论上你的文件都有 Front-matter，但为安全起见，如果没有则跳过
        print(f'警告: 未找到 Front-matter，跳过 {filepath}')
        return

    # 2. 检查正文是否已经被 {% raw %} 包裹
    # 简单的启发式检查：如果正文开头是 {% raw %} 且结尾是 {% endraw %}，则跳过
    if re.match(r'^\s*{%\s*raw\s*%}', body) and re.search(r'{%\s*endraw\s*%}\s*$', body):
        print(f'跳过 (已包裹): {filepath}')
        return

    # 3. 将正文用 {% raw %} 包裹
    new_body = '{% raw %}\n' + body + '\n{% endraw %}'
    new_content = front_matter + new_body

    # 4. 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'已包裹: {filepath}')

def main():
    print("即将对所有 Markdown 文件正文添加 {% raw %} 包裹。")
    print("请确保已执行备份！")
    confirm = input("输入 y 继续，其他任意键取消: ")
    if confirm.lower() != 'y':
        print("已取消。")
        return

    processed = 0
    skipped = 0
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                # 简单起见，不在循环内打印，避免刷屏
                wrap_file_content(filepath)
                # 可以根据需要添加计数
    print("\n批量处理完成。请运行 hexo clean && hexo generate 测试。")

if __name__ == '__main__':
    main()
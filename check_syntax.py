#!/usr/bin/env python3
import ast
import sys

with open('main.py', 'r') as f:
    source = f.read()

try:
    ast.parse(source)
    print('Syntax OK')
except SyntaxError as e:
    print(f'Syntax error at line {e.lineno}: {e.msg}')
    lines = source.split('\n')
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 3)
    for i in range(start, end):
        marker = '>>> ' if i == e.lineno - 1 else '    '
        print(f'{marker}{i+1:4d}: {lines[i]}')
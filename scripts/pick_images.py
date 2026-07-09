#!/usr/bin/env python3
"""免版权配图助手(可靠源,直接嵌 URL)。
头像/人脸(强烈推荐,最稳):  https://i.pravatar.cc/{尺寸}?img={1-70}
通用照片(风景/食物/物品):    https://picsum.photos/seed/{任意种子}/{宽}/{高}
用法: python3 pick_images.py avatar 3   → 3 个头像URL
      python3 pick_images.py photo 686 400 2
规则:同页每图换不同 img/种子;⚠不要用 loremflickr(实测经常挂图)。"""
import sys,random
kind=sys.argv[1] if len(sys.argv)>1 else 'avatar'
if kind=='avatar':
    n=int(sys.argv[2]) if len(sys.argv)>2 else 1
    for i in range(n):print(f'https://i.pravatar.cc/150?img={random.randint(1,70)}')
else:
    w=sys.argv[2] if len(sys.argv)>2 else '686'
    h=sys.argv[3] if len(sys.argv)>3 else '400'
    n=int(sys.argv[4]) if len(sys.argv)>4 else 1
    for i in range(n):print(f'https://picsum.photos/seed/{random.randint(1,9999)}/{w}/{h}')

# -*- coding: utf-8 -*-
import os
import sys

# Добавляем путь к модулям
sys.path.append('/home/pdvdanya/Agy_Projects/Me/Course_work/docs/report_builder')

from part1_intro import TITLE_PAGE, ASSIGNMENT, ABSTRACT, TOC, INTRODUCTION
from part2_chapter1 import CHAPTER_1
from part3_chapter2 import CHAPTER_2
from part4_chapter3 import CHAPTER_3
from part5_conclusion_and_appendix import CONCLUSION, REFERENCES, get_appendix

print("Сборка полного Markdown отчета...")

full_markdown = "\n".join([
    TITLE_PAGE,
    ASSIGNMENT,
    ABSTRACT,
    TOC,
    INTRODUCTION,
    CHAPTER_1,
    CHAPTER_2,
    CHAPTER_3,
    CONCLUSION,
    REFERENCES,
    get_appendix()
])

md_path1 = '/home/pdvdanya/Agy_Projects/Me/Course_work/docs/Otchet_Kursovaya_TiMP.md'
md_path2 = '/home/pdvdanya/Agy_Projects/Me/Course_work/Otchet_Kursovaya_TiMP.md'

with open(md_path1, 'w', encoding='utf-8') as f:
    f.write(full_markdown)

with open(md_path2, 'w', encoding='utf-8') as f:
    f.write(full_markdown)

print(f"✅ Markdown отчет сохранен: {md_path1}")
print(f"✅ Копия в корне проекта: {md_path2}")
print(f"Длина Markdown отчета: {len(full_markdown)} символов, {len(full_markdown.split())} слов")


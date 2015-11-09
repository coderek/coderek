from markdown import markdown
import yaml


def parse_markdown(text):
    meta_start = text.index('---')
    meta_end = text.index('---', meta_start + 3)
    meta_str = text[meta_start + 3: meta_end].strip()
    meta = yaml.load(meta_str)

    return markdown(text[meta_end + 3:]), meta

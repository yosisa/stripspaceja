# -*- coding: utf-8 -*-

import re
from docutils.nodes import Text, paragraph, literal


def is_ascii(char):
    return ord(char) < 128


def is_need_spacer(prev_text, next_text, has_spacer):
    if not is_ascii(prev_text[-1]) and not is_ascii(next_text[0]):
        return False
    if not has_spacer:
        return False
    return True


def join_text(prev_text, next_text, has_spacer):
    if is_need_spacer(prev_text, next_text, has_spacer):
        return prev_text + ' ' + next_text
    return prev_text + next_text


def tidy_text(text, insert_spacer):
    parts = [x for x in re.split(r'[\n\r\t]', text) if x]
    newtext = parts[0]
    for text in parts[1:]:
        newtext = join_text(newtext, text, insert_spacer)
    return newtext.strip()


def strip_space(app, doctree, docname):
    if not app.config.stripspaceja_enable:
        return
    has_spacer = app.config.stripspaceja_has_spacer
    for para in doctree.traverse(paragraph):
        # 段落単位で処理
        nodes = [[x, tidy_text(x.astext(), has_spacer)]
                 for x in para.traverse(Text)]
        for i, pair in enumerate(nodes[1:]):
            prev = nodes[i]
            if not is_need_spacer(prev[1], pair[1], has_spacer):
                continue
            # literal ノードの前後のノードにスペースを付加
            if isinstance(pair[0].parent, literal):
                prev[1] = prev[1] + ' '
            else:
                pair[1] = ' ' + pair[1]
        # ノードを置換
        for pair in nodes:
            pair[0].parent.replace(pair[0], Text(pair[1]))


def setup(app):
    app.add_config_value('stripspaceja_enable', True, 'env')
    app.add_config_value('stripspaceja_has_spacer', True, 'env')
    app.connect("doctree-resolved", strip_space)

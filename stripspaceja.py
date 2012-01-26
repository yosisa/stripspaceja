# -*- coding: utf-8 -*-

import re
from docutils.nodes import Text, paragraph


def is_ascii(char):
    return ord(char) < 128


def join_text(prev_text, next_text, insert_spacer):
    if insert_spacer:
        if not is_ascii(prev_text[-1]) and not is_ascii(next_text[0]):
            prev_text += next_text
        else:
            prev_text += ' ' + next_text
    else:
        if is_ascii(prev_text[-1]) and is_ascii(next_text[0]):
            prev_text += ' ' + next_text
        else:
            prev_text += next_text
    return prev_text


def tidy_text(text, insert_spacer):
    parts = [x for x in re.split(r'[\n\r\t]', text) if x]
    newtext = parts[0]
    for text in parts[1:]:
        newtext = join_text(newtext, text, insert_spacer)
    return newtext.strip()


def strip_space(app, doctree, docname):
    if not app.config.stripspaceja_enable:
        return
    for para in doctree.traverse(paragraph):
        # 段落単位で処理
        followed_ascii = False
        for node in para.traverse(Text):
            newtext = node.astext()
            if isinstance(node.parent, paragraph):
                newtext = tidy_text(newtext,
                                    app.config.stripspaceja_insert_spacer)
                if followed_ascii:
                    newtext = ' ' + newtext
            # 最後の文字がasciiかどうか確認
            if len(newtext) > 0:
                followed_ascii = is_ascii(newtext[-1])
            node.parent.replace(node, Text(newtext))


def setup(app):
    app.add_config_value('stripspaceja_enable', True, 'env')
    app.add_config_value('stripspaceja_insert_spacer', True, 'env')
    app.connect("doctree-resolved", strip_space)

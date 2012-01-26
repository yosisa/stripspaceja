# -*- coding: utf-8 -*-

def strip_space(app, doctree, docname):
    if not app.config.stripspaceja_enable:
        return
    import re
    from docutils.nodes import Text, paragraph
    for para in doctree.traverse(paragraph):
        # 段落単位で処理
        followed_ascii = False
        for node in para.traverse(Text):
            newtext = node.astext()
            if isinstance(node.parent, paragraph):
                # 単なるテキストの改行と前後スペースを削除
                newtext = re.sub(r'[\n\r\t]', '', newtext)
                newtext = newtext.strip()
                # 前の文字がasciiなら先頭に半角スペースを入れる
                if followed_ascii:
                    newtext = ' ' + newtext
            # 最後の文字がasciiかどうか確認
            if len(newtext) > 0:
                followed_ascii = ord(newtext[-1]) < 128
            node.parent.replace(node, Text(newtext))


def setup(app):
    app.add_config_value('stripspaceja_enable', 'env', 'env')
    app.connect("doctree-resolved", strip_space)

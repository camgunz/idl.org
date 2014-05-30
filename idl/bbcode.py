# -*- coding: UTF-8 -*-

_base_replacements = (
    ('[b]', '<strong>'),
    ('[/b]', '</strong>'),
    ('[i]', '<em>'),
    ('[/i]', '</em>'),
    ('[u]', '<u>'),
    ('[/u]', '</u>'),
    ('[s]', '<strike>'),
    ('[/s]', '</strike>'),
    ('[code]', '<pre>'),
    ('[/code]', '</pre>'),
    ('[left]', '<div style="text-align: left">'),
    ('[/left]', '</div>'),
    ('[center]', '<div style="text-align: center">'),
    ('[/center]', '</div>'),
    ('[right]', '<div style="text-align: right">'),
    ('[/right]', '</div>'),
    ('[move]', '<marquee>'),
    ('[/move]', '</marquee>'),
    ('[/glow]', ''),
    ('[/shadow]', ''),
    ('[sup]', '<sup>'),
    ('[/sup]', '</sup>'),
    ('[sub]', '<sub>'),
    ('[/sub]', '</sub>'),
    ('[tt]', '<tt>'),
    ('[/tt]', '</tt>'),
    ('[table]', '<table>'),
    ('[/table]', '</table>'),
    ('[tr]', '<tr>'),
    ('[/tr]', '</tr>'),
    ('[td]', '<td>'),
    ('[/td]', '</td>'),
    ('[code]', '<pre>'),
    ('[/code]', '</pre>'),
    ('[quote]', '<blockquote>'),
    ('[/quote]', '</blockquote>'),
    ('[list]', '<ul>'),
    ('[list type=decimal]', '<ul>'),
    ('[/list]', '</ul>'),
    ('[li]', '<li>'),
    ('[/li]', '</li>'),
    ('[*]', '<li>'),
    ('[hr]', '<hr/>'),
    ('[/font]', '</font>'),
    ('[/size]', '</span>'),
    ('[/color]', '</span>'),
    ('[/url]', '</a>'),
    ('[/ftp]', '</a>'),
    ('[/email]', '</a>'),
    ('[/img]', ''),
    ('[html]', ''),
    ('[/html]', '')
)

def get_tag_params(tag):
    for i in range(len(tag)):
        if tag[i] == '=':
            return tag[i+1:-1]
    return ''

def render(data):
    tags = []
    seen_tags = set()
    link_opens = []
    link_closes = []
    url_opens = []
    url_closes = []
    ftp_opens = []
    ftp_closes = []
    email_opens = []
    email_closes = []
    image_opens = []
    image_closes = []

    for i, c in enumerate(data):
        if c == '[':
            j = data[i+1:].find(']')
            if j != -1:
                tags.append((i, data[i:i+j + 2]))

    replacements = [x for x in _base_replacements]
    replacements.extend([(x.upper(), y) for x, y in _base_replacements])

    for position, tag in tags:
        if tag.lower().startswith('[url'):
            url_opens.append((position, tag))
        elif tag.lower().startswith('[/url'):
            url_closes.append((position, tag))
        if tag.lower().startswith('[email'):
            email_opens.append((position, tag))
        elif tag.lower().startswith('[/email'):
            email_closes.append((position, tag))
        if tag.lower().startswith('[ftp'):
            ftp_opens.append((position, tag))
        elif tag.lower().startswith('[/ftp'):
            ftp_closes.append((position, tag))
        elif tag.lower().startswith('[img'):
            image_opens.append((position, tag))
        elif tag.lower().startswith('[/img'):
            image_closes.append((position, tag))
        elif tag in seen_tags:
            continue
        elif tag.lower().startswith('[shadow'):
            replacements.append((tag, ''))
        elif tag.lower().startswith('[glow'):
            replacements.append((tag, ''))
        elif tag.lower().startswith('[quote'):
            replacements.append((tag, '<blockquote>'))
        elif tag.lower().startswith('[font'):
            params = get_tag_params(tag)
            replacements.append((tag, '<font face="%s">' % (params)))
        elif tag.lower().startswith('[size'):
            params = get_tag_params(tag)
            replacements.append((
                tag, '<span style="font-size: %s">' % (params)
            ))
        elif tag.lower().startswith('[color'):
            params = get_tag_params(tag)
            replacements.append((tag, '<span style="color: %s">' % (params)))
        seen_tags.add(tag)

    for x, y in zip(url_opens, url_closes):
        open_position, open_tag = x
        close_position, close_tag = y
        params = get_tag_params(open_tag)
        contents = data[open_position + len(open_tag):close_position]
        if params:
            url = params
        else:
            url = contents
        replacements.append(
            (open_tag + contents, '<a href="%s">%s' % (url, contents))
        )

    for x, y in zip(email_opens, email_closes):
        open_position, open_tag = x
        close_position, close_tag = y
        params = get_tag_params(open_tag)
        contents = data[open_position + len(open_tag):close_position]
        if params:
            url = params
        else:
            url = contents
        replacements.append(
            (open_tag + contents, '<a href="mailto:%s">%s' % (url, contents))
        )

    for x, y in zip(ftp_opens, ftp_closes):
        open_position, open_tag = x
        close_position, close_tag = y
        params = get_tag_params(open_tag)
        contents = data[open_position + len(open_tag):close_position]
        if params:
            url = params
        else:
            url = contents
        replacements.append(
            (open_tag + contents, '<a href="ftp://%s">%s' % (url, contents))
        )

    for x, y in zip(image_opens, image_closes):
        open_position, open_tag = x
        close_position, close_tag = y
        params = get_tag_params(open_tag)
        src = data[open_position + len(open_tag):close_position]
        replacements.append(
            (open_tag + src, '<img src="%s" %s/>' % (src, params))
        )

    for x, y in replacements:
        data = data.replace(x, y)

    return data


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera os cards SVG do README do perfil (tema claro/escuro, EN/PT).

Uso:   python tools/build_readme.py
Saida: assets/*.svg

Todo o conteudo visivel do README vive aqui. Para mudar um texto, edite COPY
e rode o script de novo -- nao edite os SVGs na mao.
"""
import io
import os
import html

W, PAD = 880, 44
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')

THEMES = {
    'dark': dict(bg='#0d1117', border='#30363d', dots='#30363d', text='#e6edf3',
                 muted='#9198a1', dim='#6e7681', a1='#58a6ff', a2='#a371f7',
                 chip_bg='#161b22', chip_br='#30363d', glow='#1f6feb', glow_o='0.16'),
    'light': dict(bg='#ffffff', border='#d0d7de', dots='#d8dee4', text='#1f2328',
                  muted='#59636e', dim='#848d97', a1='#0969da', a2='#8250df',
                  chip_bg='#f6f8fa', chip_br='#d0d7de', glow='#0969da', glow_o='0.08'),
}


def esc(s):
    return html.escape(s, quote=False)


def wrap(text, max_px, size, factor=0.55):
    """Quebra de linha manual -- SVG nao tem reflow de texto."""
    out, cur = [], ''
    for word in text.split():
        cand = (cur + ' ' + word).strip()
        if cur and len(cand) * size * factor > max_px:
            out.append(cur)
            cur = word
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out


def style(n_delays=14):
    delays = ''.join('.d%d{animation-delay:%.2fs}' % (i, .04 + i * .07)
                     for i in range(1, n_delays + 1))
    return (
        '<style>'
        '.f{font-family:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}'
        '.m{font-family:ui-monospace,SFMono-Regular,"Cascadia Code","Fira Code",Consolas,monospace}'
        '.j{font-family:"Yu Gothic","Hiragino Sans","Noto Sans JP","MS Gothic",sans-serif}'
        '.r{opacity:0;animation:rise .6s cubic-bezier(.2,.7,.3,1) forwards}'
        '@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}'
        '.drift{animation:drift 20s ease-in-out infinite alternate}'
        '@keyframes drift{from{transform:translate(0,0)}to{transform:translate(-110px,28px)}}'
        '.grow{transform-box:fill-box;transform-origin:left center;'
        'animation:grow .7s .25s cubic-bezier(.2,.7,.3,1) both}'
        '@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}'
        + delays +
        '@media (prefers-reduced-motion:reduce){'
        '.r{animation:none;opacity:1;transform:none}'
        '.grow{animation:none;transform:none}'
        '.drift{animation:none}}'
        '</style>'
    )


def shell(h, th, label, body):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="%s"><title>%s</title>'
        '<defs>'
        '<radialGradient id="g" cx="0.5" cy="0.5" r="0.5">'
        '<stop offset="0%%" stop-color="%s" stop-opacity="%s"/>'
        '<stop offset="100%%" stop-color="%s" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="a" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%%" stop-color="%s"/><stop offset="58%%" stop-color="%s"/>'
        '<stop offset="100%%" stop-color="%s" stop-opacity="0"/></linearGradient>'
        '<pattern id="d" width="22" height="22" patternUnits="userSpaceOnUse">'
        '<circle cx="1.3" cy="1.3" r="1.3" fill="%s"/></pattern>'
        '<clipPath id="c"><rect width="%d" height="%d" rx="14"/></clipPath>'
        '</defs>%s'
        '<g clip-path="url(#c)">'
        '<rect width="%d" height="%d" fill="%s"/>'
        '<rect width="%d" height="%d" fill="url(#d)" opacity="0.5"/>'
        '<circle class="drift" cx="%d" cy="-70" r="250" fill="url(#g)"/></g>'
        '<rect x="0.5" y="0.5" width="%d" height="%d" rx="14" fill="none" stroke="%s"/>'
        '%s</svg>'
    ) % (W, h, W, h, html.escape(label), html.escape(label),
         th['glow'], th['glow_o'], th['glow'],
         th['a1'], th['a2'], th['a2'],
         th['dots'], W, h, style(),
         W, h, th['bg'], W, h, W - 110,
         W - 1, h - 1, th['border'], body)


def section_title(txt, th):
    return (
        '<text class="f r d1" x="%d" y="50" font-size="12.5" font-weight="700" '
        'letter-spacing="2.4" fill="%s">%s</text>'
        '<rect class="grow" x="%d" y="62" width="34" height="2.5" rx="1.25" fill="url(#a)"/>'
    ) % (PAD, th['a1'], esc(txt.upper()), PAD)


# --------------------------------------------------------------------- cards

def card_header(th):
    b = []
    # marca d'agua: Samui Arashi -- "tempestade fria" em japones
    b.append('<text class="j" text-anchor="end" x="%d" y="176" font-size="80" letter-spacing="6" '
             'fill="%s" opacity="0.055">寒い嵐</text>' % (W - 40, th['text']))
    b.append('<text class="m r d1" x="%d" y="58" font-size="13" letter-spacing="1.3" '
             'fill="%s">@SamuiArashi</text>' % (PAD, th['dim']))
    b.append('<text class="f r d2" x="%d" y="114" font-size="50" font-weight="700" '
             'letter-spacing="-1.3" fill="%s">Samui</text>' % (PAD, th['text']))
    b.append('<rect class="grow" x="%d" y="131" width="134" height="3" rx="1.5" fill="url(#a)"/>' % PAD)
    b.append('<text class="f r d4" x="%d" y="172" font-size="16.5" fill="%s">'
             '.NET 8 APIs on the back, React and Next.js on the front.</text>' % (PAD, th['text']))
    b.append('<text class="m r d6" x="%d" y="202" font-size="12.5" letter-spacing="0.3" fill="%s">'
             'C#  ·  ASP.NET Core  ·  EF Core  ·  TypeScript  ·  Next.js  '
             '·  Cloudflare Workers</text>' % (PAD, th['dim']))
    label = ('Samui - .NET 8 APIs on the back, React and Next.js on the front. '
             'C#, ASP.NET Core, EF Core, TypeScript, Next.js, Cloudflare Workers.')
    return shell(238, th, label, ''.join(b))


def card_text(th, title, paras, label):
    b, y, n = [section_title(title, th)], 100, 1
    for para in paras:
        for line in wrap(para, W - PAD * 2, 15.5):
            n += 1
            b.append('<text class="f r d%d" x="%d" y="%d" font-size="15.5" fill="%s">%s</text>'
                     % (min(n, 14), PAD, y, th['text'], esc(line)))
            y += 26
        y += 12
    return shell(y + 16, th, label, ''.join(b))


def card_stack(th, title, rows, label):
    b, y, n = [section_title(title, th)], 100, 1
    for name, items in rows:
        n += 1
        cls = 'r d%d' % min(n, 14)
        b.append('<text class="f %s" text-anchor="end" x="188" y="%d" font-size="13" fill="%s">%s</text>'
                 % (cls, y, th['muted'], esc(name)))
        x = 210
        for it in items:
            cw = len(it) * 7.5 + 26
            b.append('<g class="%s"><rect x="%d" y="%d" width="%d" height="26" rx="7" fill="%s" '
                     'stroke="%s"/><text class="m" x="%d" y="%d" font-size="12.5" fill="%s">%s</text></g>'
                     % (cls, x, y - 18, cw, th['chip_bg'], th['chip_br'],
                        x + 13, y, th['text'], esc(it)))
            x += cw + 8
        y += 42
    return shell(y - 8, th, label, ''.join(b))


def card_list(th, title, items, label):
    b, y, n = [section_title(title, th)], 100, 1
    for lead, desc in items:
        n += 1
        cls = 'r d%d' % min(n, 14)
        b.append('<rect class="%s" x="%d" y="%d" width="3" height="13" rx="1.5" fill="url(#a)"/>'
                 % (cls, PAD, y - 11))
        b.append('<text class="f %s" x="%d" y="%d" font-size="15" font-weight="650" fill="%s">%s</text>'
                 % (cls, PAD + 16, y, th['text'], esc(lead)))
        y += 22
        for line in wrap(desc, W - PAD * 2 - 60, 13.5):
            b.append('<text class="f %s" x="%d" y="%d" font-size="13.5" fill="%s">%s</text>'
                     % (cls, PAD + 16, y, th['muted'], esc(line)))
            y += 20
        y += 16
    return shell(y - 2, th, label, ''.join(b))


def badge(th, text, kind):
    w, h = int(len(text) * 8.4 + 78), 46
    if kind == 'email':
        icon = ('<rect x="26" y="15" width="19" height="15" rx="3" fill="none" stroke="%s" '
                'stroke-width="1.8"/>'
                '<path d="M26.8 16.6 L35.5 23.4 L44.2 16.6" fill="none" stroke="%s" '
                'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
                % (th['a1'], th['a1']))
    else:
        icon = ('<rect x="26" y="14" width="18" height="18" rx="4" fill="%s"/>'
                '<text class="f" x="35" y="27" font-size="11.5" font-weight="700" '
                'text-anchor="middle" fill="%s">in</text>' % (th['a1'], th['bg']))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="%s"><title>%s</title>'
        '<style>.f{font-family:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,'
        'sans-serif}</style>'
        '<rect x="0.75" y="0.75" width="%s" height="%s" rx="10" fill="%s" stroke="%s"/>%s'
        '<text class="f" x="58" y="28" font-size="14.5" font-weight="600" fill="%s">%s</text></svg>'
    ) % (w, h, w, h, html.escape(text), html.escape(text),
         w - 1.5, h - 1.5, th['chip_bg'], th['border'], icon, th['text'], esc(text))


# ------------------------------------------------------------------ conteudo

COPY = {
    'en': {
        'about_t': 'About',
        'about': [
            u'Full-stack developer, mostly on B2B products: multi-tenant APIs in .NET and the '
            u'interfaces that consume them.',
            u'I care about architecture that survives its second year — real boundaries '
            u'between layers, typed contracts between back and front, and tests that fail for '
            u'the right reason.',
            u'Most of what I ship is private client work, so this profile is about how I build '
            u'more than what is public.',
        ],
        'stack_t': 'Stack',
        'stack': [
            (u'Backend', [u'C#', u'.NET 8', u'ASP.NET Core', u'EF Core']),
            (u'Architecture', [u'Clean Architecture', u'CQRS + MediatR', u'ErrorOr',
                               u'FluentValidation']),
            (u'Data', [u'PostgreSQL', u'MySQL', u'Redis', u'S3 / MinIO']),
            (u'Frontend', [u'TypeScript', u'Next.js 14', u'React 18', u'Tailwind', u'shadcn/ui']),
            (u'Client state', [u'TanStack Query', u'Zustand', u'Zod', u'React Hook Form']),
            (u'Testing', [u'xUnit', u'FluentAssertions', u'Moq', u'Vitest', u'Playwright']),
            (u'Infra', [u'Docker', u'Cloudflare Workers', u'Hangfire', u'JWT']),
        ],
        'how_t': 'How I build',
        'how': [
            (u'Layers that mean something.',
             u'Domain, Application, Infrastructure and API are separate projects, not folders '
             u'with good intentions.'),
            (u'Expected failures are values, not exceptions.',
             u'ErrorOr<T> all the way up, so the compiler keeps track of what can go wrong.'),
            (u'Contract first.',
             u'The OpenAPI spec generates the frontend client — a breaking backend change '
             u'breaks the build, not production.'),
            (u'Two kinds of tests.',
             u'Fast unit tests around the domain, integration tests for anything that touches '
             u'a database.'),
            (u'Boring infrastructure.',
             u'Background jobs, object storage and caching solved with tools that already work.'),
        ],
        'now_t': 'Currently',
        'now': [
            (u'A multi-tenant white-label SaaS',
             u'.NET 8 and EF Core, background jobs, S3 storage, PDF generation.'),
            (u'A Next.js 14 app on Cloudflare Workers',
             u'i18n, a typed API client generated from OpenAPI, end-to-end Playwright suite.'),
        ],
    },
    'pt': {
        'about_t': 'Sobre',
        'about': [
            u'Desenvolvedor full-stack, principalmente em produtos B2B: APIs multi-tenant em '
            u'.NET e as interfaces que consomem essas APIs.',
            u'Me importo com arquitetura que sobrevive ao segundo ano — fronteiras reais '
            u'entre camadas, contratos tipados entre back e front, e testes que quebram pelo '
            u'motivo certo.',
            u'A maior parte do que entrego é trabalho privado para clientes, então '
            u'este perfil fala mais de como eu construo do que do que está público.',
        ],
        'stack_t': 'Stack',
        'stack': [
            (u'Backend', [u'C#', u'.NET 8', u'ASP.NET Core', u'EF Core']),
            (u'Arquitetura', [u'Clean Architecture', u'CQRS + MediatR', u'ErrorOr',
                              u'FluentValidation']),
            (u'Dados', [u'PostgreSQL', u'MySQL', u'Redis', u'S3 / MinIO']),
            (u'Frontend', [u'TypeScript', u'Next.js 14', u'React 18', u'Tailwind', u'shadcn/ui']),
            (u'Estado no cliente', [u'TanStack Query', u'Zustand', u'Zod', u'React Hook Form']),
            (u'Testes', [u'xUnit', u'FluentAssertions', u'Moq', u'Vitest', u'Playwright']),
            (u'Infra', [u'Docker', u'Cloudflare Workers', u'Hangfire', u'JWT']),
        ],
        'how_t': 'Como eu construo',
        'how': [
            (u'Camadas que significam alguma coisa.',
             u'Domain, Application, Infrastructure e API são projetos separados, não '
             u'pastas com boas intenções.'),
            (u'Falha esperada é valor, não exceção.',
             u'ErrorOr<T> até o topo, para o compilador lembrar o que pode dar errado.'),
            (u'Contrato primeiro.',
             u'A spec OpenAPI gera o client do frontend — mudança quebrando no backend '
             u'quebra o build, não a produção.'),
            (u'Dois tipos de teste.',
             u'Teste unitário rápido no domínio, teste de integração em '
             u'tudo que encosta no banco.'),
            (u'Infra sem graça.',
             u'Jobs em background, storage de objeto e cache resolvidos com ferramenta que já '
             u'funciona.'),
        ],
        'now_t': 'Agora',
        'now': [
            (u'Um SaaS white-label multi-tenant',
             u'.NET 8 e EF Core, jobs em background, storage S3, geração de PDF.'),
            (u'Um app Next.js 14 na Cloudflare Workers',
             u'i18n, client de API tipado gerado do OpenAPI, suíte end-to-end em Playwright.'),
        ],
    },
}


# --------------------------------------------------------------------- build

def write(name, content):
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(content)
    print('%-28s %6d bytes' % (name, len(content.encode('utf-8'))))


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for theme, th in THEMES.items():
        write('header-%s.svg' % theme, card_header(th))
        write('contact-email-%s.svg' % theme, badge(th, 'Email', 'email'))
        write('contact-linkedin-%s.svg' % theme, badge(th, 'LinkedIn', 'in'))
        for lang, c in COPY.items():
            sfx = '%s-%s.svg' % (lang, theme)
            write('about-' + sfx, card_text(th, c['about_t'], c['about'], ' '.join(c['about'])))
            write('stack-' + sfx, card_stack(
                th, c['stack_t'], c['stack'],
                c['stack_t'] + ': ' + '; '.join(n + ': ' + ', '.join(i) for n, i in c['stack'])))
            write('how-' + sfx, card_list(
                th, c['how_t'], c['how'],
                c['how_t'] + ': ' + ' '.join(a + ' ' + b for a, b in c['how'])))
            write('now-' + sfx, card_list(
                th, c['now_t'], c['now'],
                c['now_t'] + ': ' + ' '.join(a + ' — ' + b for a, b in c['now'])))


if __name__ == '__main__':
    main()

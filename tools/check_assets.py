#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere os assets gerados do perfil.

Uso:  python tools/check_assets.py

Roda no CI depois de `build_readme.py`, e vale rodar local antes de commitar.
Sai com codigo 1 e lista tudo que estiver errado.
"""
from __future__ import print_function

import io
import os
import re
import sys
import glob
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'assets')
README = os.path.join(ROOT, 'README.md')

SVG_NS = 'http://www.w3.org/2000/svg'


def check_svg_xml(problems):
    """Todo SVG precisa ser XML valido, ter viewBox e um titulo acessivel."""
    files = sorted(glob.glob(os.path.join(ASSETS, '*.svg')))
    if not files:
        problems.append('assets/ nao tem nenhum SVG -- o gerador rodou?')
        return files
    for path in files:
        name = os.path.basename(path)
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            problems.append('%s: XML invalido (%s)' % (name, exc))
            continue
        if root.tag != '{%s}svg' % SVG_NS:
            problems.append('%s: raiz nao e <svg> no namespace SVG' % name)
        if not root.get('viewBox'):
            problems.append('%s: sem viewBox -- nao escala no README' % name)
        if not (root.get('aria-label') or root.find('{%s}title' % SVG_NS) is not None):
            problems.append('%s: sem aria-label nem <title>' % name)
    return files


def check_readme(files, problems):
    """Referencias do README e assets no disco tem que bater exatamente."""
    if not os.path.isfile(README):
        problems.append('README.md nao existe')
        return
    text = io.open(README, encoding='utf-8').read()

    referenced = set(re.findall(r'assets/([\w.-]+\.svg)', text))
    on_disk = set(os.path.basename(f) for f in files)
    for missing in sorted(referenced - on_disk):
        problems.append('README aponta para assets/%s, que nao existe' % missing)
    for orphan in sorted(on_disk - referenced):
        problems.append('assets/%s nao e usado pelo README' % orphan)

    for tag in re.findall(r'<img\b[^>]*>', text):
        alt = re.search(r'alt="([^"]*)"', tag)
        if alt is None or not alt.group(1).strip():
            problems.append('<img> sem alt util: %s' % tag[:70])
        elif len(alt.group(1)) < 20:
            problems.append('alt curto demais (%r) -- e o unico texto que sobra '
                            'para leitor de tela' % alt.group(1))

    # cada <picture> precisa das duas fontes de tema
    for block in re.findall(r'<picture>.*?</picture>', text, re.S):
        for scheme in ('dark', 'light'):
            if 'prefers-color-scheme: %s' % scheme not in block:
                problems.append('<picture> sem variante %s' % scheme)

    for stem in sorted(set(n.rsplit('-', 1)[0] for n in on_disk)):
        for scheme in ('dark', 'light'):
            pair = '%s-%s.svg' % (stem, scheme)
            if pair not in on_disk:
                problems.append('%s nao tem par de tema (%s faltando)' % (stem, pair))


def main():
    problems = []
    files = check_svg_xml(problems)
    check_readme(files, problems)

    if problems:
        print('FALHOU -- %d problema(s):' % len(problems))
        for p in problems:
            print('  - %s' % p)
        return 1
    print('ok: %d SVGs validos, README em sincronia com assets/' % len(files))
    return 0


if __name__ == '__main__':
    sys.exit(main())

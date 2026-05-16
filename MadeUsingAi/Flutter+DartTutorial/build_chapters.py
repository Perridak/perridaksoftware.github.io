#!/usr/bin/env python3
"""
Build script: Convert markdown chapters to JavaScript objects with srcdoc content.
Usage: python build_chapters.py
Output: chapters.js (single file with all chapters)
"""

import os
import re
import json
from pathlib import Path

# Dart syntax highlighting colours (from design)
DART_COLORS = {
    'keyword': '#87ceeb',      # light blue
    'class': '#ff4444',        # red
    'number': '#bb86fc',       # purple
    'function': '#ffffff',     # white
    'operator': '#ffff44',     # yellow
    'string': '#44ff44',       # green
    'comment': '#888888',      # grey
    'variable': '#ffffff'      # white
}

# Dart keywords to highlight
DART_KEYWORDS = {
    'abstract', 'as', 'assert', 'async', 'await', 'break', 'case', 'catch',
    'class', 'const', 'continue', 'covariant', 'default', 'deferred', 'do',
    'dynamic', 'else', 'enum', 'export', 'extends', 'external', 'factory',
    'false', 'final', 'finally', 'for', 'Function', 'get', 'if', 'implements',
    'import', 'in', 'is', 'late', 'library', 'mixin', 'new', 'null', 'on',
    'operator', 'part', 'required', 'rethrow', 'return', 'set', 'static',
    'super', 'switch', 'sync', 'this', 'throw', 'true', 'try', 'type',
    'typedef', 'var', 'void', 'while', 'with', 'yield'
}

# Built-in Dart types
DART_TYPES = {
    'int', 'double', 'String', 'bool', 'List', 'Map', 'Set', 'Iterable',
    'Future', 'Stream', 'Duration', 'DateTime', 'Runes', 'Symbol'
}

class DartHighlighter:
    """Syntax highlighter for Dart code."""
    
    def highlight(self, code):
        """Apply syntax highlighting to Dart code."""
        result = []
        i = 0
        
        while i < len(code):
            # Comments
            if code[i:i+2] == '//':
                end = code.find('\n', i)
                if end == -1:
                    end = len(code)
                result.append(f'<span style="color: {DART_COLORS["comment"]}">{self.escape(code[i:end])}</span>')
                i = end
                continue
            
            if code[i:i+2] == '/*':
                end = code.find('*/', i)
                if end != -1:
                    end += 2
                else:
                    end = len(code)
                result.append(f'<span style="color: {DART_COLORS["comment"]}">{self.escape(code[i:end])}</span>')
                i = end
                continue
            
            # Strings
            if code[i] in ('"', "'", '`'):
                quote = code[i]
                start = i
                i += 1
                while i < len(code):
                    if code[i] == '\\':
                        i += 2
                    elif code[i] == quote:
                        i += 1
                        break
                    else:
                        i += 1
                result.append(f'<span style="color: {DART_COLORS["string"]}">{self.escape(code[start:i])}</span>')
                continue
            
            # Numbers
            if code[i].isdigit():
                start = i
                while i < len(code) and (code[i].isalnum() or code[i] in '._'):
                    i += 1
                result.append(f'<span style="color: {DART_COLORS["number"]}">{code[start:i]}</span>')
                continue
            
            # Identifiers and keywords
            if code[i].isalpha() or code[i] == '_':
                start = i
                while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                    i += 1
                word = code[start:i]
                
                if word in DART_KEYWORDS:
                    result.append(f'<span style="color: {DART_COLORS["keyword"]}">{word}</span>')
                elif word in DART_TYPES:
                    result.append(f'<span style="color: {DART_COLORS["class"]}">{word}</span>')
                else:
                    result.append(word)
                continue
            
            # Operators
            if code[i] in '+-*/%=<>!&|^?:':
                result.append(f'<span style="color: {DART_COLORS["operator"]}">{code[i]}</span>')
                i += 1
                continue
            
            # Whitespace and other
            result.append(self.escape(code[i]))
            i += 1
        
        return ''.join(result)
    
    @staticmethod
    def escape(text):
        """Escape HTML special characters."""
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('"', '&quot;')
                    .replace("'", '&#39;'))


def parse_markdown(markdown_text):
    """Convert Markdown to HTML, preserving HTML tags but parsing content within them."""
    lines = markdown_text.split('\n')
    html = []
    i = 0
    highlighter = DartHighlighter()
    
    while i < len(lines):
        line = lines[i]
        
        # Opening div tags - preserve them but parse content inside
        if line.strip().startswith('<div'):
            div_tag = line
            div_class = None
            
            # Extract class name for platform divs
            if 'class="platform-' in line:
                match = re.search(r'class="([^"]*)"', line)
                if match:
                    div_class = match.group(1)
            
            html.append(div_tag)
            i += 1
            
            # Parse content until closing </div>
            while i < len(lines) and '</div>' not in lines[i]:
                inner_line = lines[i]
                
                # Recursively parse the content inside the div
                if inner_line.strip():
                    # Process as if it's top-level markdown
                    if inner_line.startswith('# '):
                        html.append(f'<h1>{escape_html(inner_line[2:].strip())}</h1>')
                        i += 1
                    elif inner_line.startswith('## '):
                        html.append(f'<h2>{escape_html(inner_line[3:].strip())}</h2>')
                        i += 1
                    elif inner_line.startswith('### '):
                        html.append(f'<h3>{escape_html(inner_line[4:].strip())}</h3>')
                        i += 1
                    elif inner_line.strip() == '---':
                        html.append('<hr>')
                        i += 1
                    elif inner_line.strip().startswith('```'):
                        lang = inner_line.strip()[3:].strip() or 'dart'
                        code_lines = []
                        i += 1
                        while i < len(lines) and not lines[i].strip().startswith('```'):
                            code_lines.append(lines[i])
                            i += 1
                        code = '\n'.join(code_lines).rstrip()
                        if lang == 'output':
                            html.append(f'<pre style="background-color: #1a1a1a; color: #ffffff; padding: 1rem; border-radius: 4px; overflow-x: auto;"><code>{escape_html(code)}</code></pre>')
                        else:
                            highlighted = highlighter.highlight(code)
                            html.append(f'<pre style="background-color: #0f172a; color: #ffffff; padding: 1rem; border-radius: 4px; overflow-x: auto;"><code>{highlighted}</code></pre>')
                        i += 1
                    elif inner_line.startswith('- '):
                        list_items = []
                        while i < len(lines) and lines[i].startswith('- ') and '</div>' not in lines[i]:
                            item = lines[i][2:].strip()
                            item = process_inline_markdown(item, highlighter)
                            list_items.append(f'<li>{item}</li>')
                            i += 1
                        html.append(f'<ul>{"".join(list_items)}</ul>')
                    elif re.match(r'^\d+\. ', inner_line):
                        list_items = []
                        while i < len(lines) and re.match(r'^\d+\. ', lines[i]) and '</div>' not in lines[i]:
                            item = re.sub(r'^\d+\. ', '', lines[i]).strip()
                            item = process_inline_markdown(item, highlighter)
                            list_items.append(f'<li>{item}</li>')
                            i += 1
                        html.append(f'<ol>{"".join(list_items)}</ol>')
                    elif inner_line.startswith('> '):
                        quote_lines = []
                        while i < len(lines) and lines[i].startswith('> ') and '</div>' not in lines[i]:
                            quote_lines.append(lines[i][2:].strip())
                            i += 1
                        quote_text = ' '.join(quote_lines)
                        quote_text = process_inline_markdown(quote_text, highlighter)
                        html.append(f'<blockquote>{quote_text}</blockquote>')
                    else:
                        # Regular paragraph
                        paragraph = process_inline_markdown(inner_line.strip(), highlighter)
                        html.append(f'<p>{paragraph}</p>')
                        i += 1
                else:
                    i += 1
            
            # Add closing div tag
            if i < len(lines) and '</div>' in lines[i]:
                html.append(lines[i])
                i += 1
            continue
        
        # Headings
        if line.startswith('# '):
            html.append(f'<h1>{escape_html(line[2:].strip())}</h1>')
            i += 1
            continue
        
        if line.startswith('## '):
            html.append(f'<h2>{escape_html(line[3:].strip())}</h2>')
            i += 1
            continue
        
        if line.startswith('### '):
            html.append(f'<h3>{escape_html(line[4:].strip())}</h3>')
            i += 1
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            html.append('<hr>')
            i += 1
            continue
        
        # Code blocks
        if line.strip().startswith('```'):
            lang = line.strip()[3:].strip() or 'dart'
            code_lines = []
            i += 1
            
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            
            code = '\n'.join(code_lines).rstrip()
            
            if lang == 'output':
                html.append(f'<pre style="background-color: #1a1a1a; color: #ffffff; padding: 1rem; border-radius: 4px; overflow-x: auto;"><code>{escape_html(code)}</code></pre>')
            else:
                highlighted = highlighter.highlight(code)
                html.append(f'<pre style="background-color: #0f172a; color: #ffffff; padding: 1rem; border-radius: 4px; overflow-x: auto;"><code>{highlighted}</code></pre>')
            
            i += 1
            continue
        
        # Unordered lists
        if line.startswith('- '):
            list_items = []
            while i < len(lines) and lines[i].startswith('- '):
                item = lines[i][2:].strip()
                item = process_inline_markdown(item, highlighter)
                list_items.append(f'<li>{item}</li>')
                i += 1
            html.append(f'<ul>{"".join(list_items)}</ul>')
            continue
        
        # Ordered lists
        if re.match(r'^\d+\. ', line):
            list_items = []
            while i < len(lines) and re.match(r'^\d+\. ', lines[i]):
                item = re.sub(r'^\d+\. ', '', lines[i]).strip()
                item = process_inline_markdown(item, highlighter)
                list_items.append(f'<li>{item}</li>')
                i += 1
            html.append(f'<ol>{"".join(list_items)}</ol>')
            continue
        
        # Blockquotes
        if line.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:].strip())
                i += 1
            quote_text = ' '.join(quote_lines)
            quote_text = process_inline_markdown(quote_text, highlighter)
            html.append(f'<blockquote>{quote_text}</blockquote>')
            continue
        
        # Platform selector buttons (preserve as-is)
        if line.strip() == '<div class="platform-selector">':
            selector_lines = []
            selector_lines.append(line)
            i += 1
            while i < len(lines) and '</div>' not in lines[i]:
                selector_lines.append(lines[i])
                i += 1
            if i < len(lines):
                selector_lines.append(lines[i])
                i += 1
            html.append('\n'.join(selector_lines))
            continue
        
        # Regular paragraphs
        if line.strip():
            paragraph = process_inline_markdown(line.strip(), highlighter)
            html.append(f'<p>{paragraph}</p>')
        
        i += 1
    
    return '\n'.join(html)


def process_inline_markdown(text, highlighter):
    """Process inline markdown elements."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    
    # Images - MUST come before links (both use [])
    # Rewrite paths from ../images/file to just file
    text = re.sub(r'!\[([^\]]*)\]\(\.\./images/([^)]+)\)', r'<img src="\2" alt="\1" style="max-width: 100%; height: auto; border-radius: 4px; margin: 1rem 0;">', text)
    
    # Inline code with Dart highlighting
    def highlight_inline_code(match):
        code = match.group(1)
        highlighted = highlighter.highlight(code)
        return f'<code style="background-color: #f0f4f8; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">{highlighted}</code>'
    
    text = re.sub(r'`([^`]+)`', highlight_inline_code, text)
    
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color: #5A7A72; text-decoration: none; border-bottom: 1px solid #5A7A72;">\1</a>', text)
    
    return text


def escape_html(text):
    """Escape HTML special characters."""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


def escape_for_js(text):
    """Escape text for JavaScript string literal."""
    return (text.replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace('\r', '\\r')
                .replace('\t', '\\t'))


def build_chapters():
    """Build all chapters as standalone HTML files."""
    # Support both folder structure (chapters/) and flat structure
    chapters_dir = Path('chapters')
    
    # If chapters folder doesn't exist, look for .md files in current directory
    if not chapters_dir.exists():
        chapters_dir = Path('.')
        # Filter chapter markdown files (starting with digits) and project files
        md_files = sorted([f for f in chapters_dir.glob('*.md') if re.match(r'^(\d+|markdown-notes-project)', f.name)])
    else:
        # Use chapter subdirectory if it exists
        md_files = sorted(chapters_dir.glob('*.md'))
    
    if not md_files:
        print("ERROR: No markdown files found in chapters/ or current directory")
        return False
    
    print(f"Found {len(md_files)} markdown files")
    
    errors = []
    
    for md_file in md_files:
        try:
            print(f"  Processing {md_file.name}...", end=' ')
            
            # Read markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                markdown = f.read()
            
            if not markdown.strip():
                print("SKIP (empty)")
                continue
            
            # Convert to HTML
            html_content = parse_markdown(markdown)
            
            # Validate HTML
            if '<' not in html_content or '>' not in html_content:
                errors.append(f"{md_file.name}: No HTML tags generated")
                print("ERROR (no content)")
                continue
            
            # Create full HTML document
            chapter_id = md_file.stem
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(chapter_id)}</title>
    <link rel="stylesheet" href="common.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #3D4A52;
            background: transparent;
            padding: 0;
        }}
        
        h1, h2, h3 {{
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            color: #1B5A56;
        }}
        
        h1 {{
            font-size: 2.5rem;
            border-bottom: 3px solid #7BA857;
            padding-bottom: 0.75rem;
        }}
        
        h2 {{
            font-size: 1.8rem;
            margin-top: 2rem;
        }}
        
        h3 {{
            font-size: 1.4rem;
        }}
        
        p {{
            margin-bottom: 1rem;
        }}
        
        ul, ol {{
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        li {{
            margin-bottom: 0.5rem;
        }}
        
        blockquote {{
            background-color: #F5E6D3;
            border-left: 4px solid #7BA857;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }}
        
        pre {{
            background-color: #0f172a;
            color: #ffffff;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1rem 0;
        }}
        
        code {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        a {{
            color: #5A7A72;
            text-decoration: none;
            border-bottom: 1px solid #5A7A72;
        }}
        
        a:hover {{
            color: #1B5A56;
            border-bottom-color: #1B5A56;
        }}
        
        .platform-selector {{
            display: flex;
            gap: 1rem;
            margin: 2rem 0;
            justify-content: center;
        }}
        
        .platform-btn {{
            padding: 0.75rem 1.5rem;
            border: 2px solid #E8F0E6;
            background-color: white;
            color: #3D4A52;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .platform-btn:hover {{
            border-color: #7BA857;
            background-color: #F9F7F3;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid #E8F0E6;
            margin: 2rem 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
<script src="common.js"></script>
</html>
"""
            
            # Write HTML file
            output_file = Path(chapter_id + '.html')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            file_size = len(full_html)
            print(f"✓ ({file_size} bytes)")
            
        except Exception as e:
            errors.append(f"{md_file.name}: {str(e)}")
            print(f"ERROR ({str(e)})")
    
    # Report results
    print(f"\n{'='*60}")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  ✗ {error}")
        return False
    else:
        print(f"SUCCESS: All {len(md_files)} chapters built")
        return True


if __name__ == '__main__':
    import sys
    success = build_chapters()
    sys.exit(0 if success else 1)

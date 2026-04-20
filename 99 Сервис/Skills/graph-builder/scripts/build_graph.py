#!/usr/bin/env python3
"""
Build vault graph: parse markdown files, extract links, generate vault-graph.json
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import sys


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return match.group(1), content[match.end():]
    return None, content


def extract_wikilinks(content):
    """Extract [[wikilinks]] from content (both [[target]] and [[target|alias]])"""
    pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    return re.findall(pattern, content)


def process_vault(vault_path):
    """Process all .md files in vault and build graph"""
    vault_path = Path(vault_path)
    files = {}
    all_links = []
    orphans = []
    broken_links = []
    
    # Collect all .md files
    md_files = [f for f in vault_path.rglob("*.md") 
                if not any(p.startswith('.') for p in f.relative_to(vault_path).parts)]
    
    file_names = {f.stem for f in md_files}
    
    # Parse each file
    for md_file in md_files:
        rel_path = md_file.relative_to(vault_path)
        content = md_file.read_text(encoding='utf-8')
        
        frontmatter, body = parse_frontmatter(content)
        links = extract_wikilinks(content)
        
        files[str(rel_path)] = {
            'path': str(rel_path),
            'stem': md_file.stem,
            'links': links,
            'has_frontmatter': frontmatter is not None
        }
        
        # Check for broken links
        for link in links:
            # Remove path separators for simple matching
            link_stem = Path(link).stem
            if link_stem not in file_names:
                broken_links.append({
                    'from': str(rel_path),
                    'to': link
                })
        
        all_links.extend(links)
    
    # Find orphans (files with no incoming links)
    linked_files = {link for link in all_links}
    for file_path, file_data in files.items():
        stem = file_data['stem']
        # Check if this file is referenced by anyone
        if stem not in linked_files and len(file_data['links']) == 0:
            orphans.append(file_path)
    
    # Build stats
    stats = {
        'total_files': len(files),
        'total_links': len(all_links),
        'orphan_files': len(orphans),
        'broken_links': len(broken_links)
    }
    
    return {
        'stats': stats,
        'files': files,
        'orphans': sorted(orphans),
        'broken_links': broken_links
    }


def main():
    if len(sys.argv) < 2:
        vault_path = Path.cwd()
    else:
        vault_path = Path(sys.argv[1])
    
    if not vault_path.exists():
        print(f"Error: vault path does not exist: {vault_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Building graph for vault: {vault_path}")
    graph = process_vault(vault_path)
    
    # Create .graph directory
    graph_dir = vault_path / '.graph'
    graph_dir.mkdir(exist_ok=True)
    
    # Write vault-graph.json
    output_path = graph_dir / 'vault-graph.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Graph saved to {output_path}")
    print(f"\nStats:")
    print(f"  Total files: {graph['stats']['total_files']}")
    print(f"  Total links: {graph['stats']['total_links']}")
    print(f"  Orphan files: {graph['stats']['orphan_files']}")
    print(f"  Broken links: {graph['stats']['broken_links']}")


if __name__ == '__main__':
    main()

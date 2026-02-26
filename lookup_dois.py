#!/usr/bin/env python3
"""
Look up missing DOIs using CrossRef API
Updates reading_list.md with found DOIs
"""

import re
import requests
import time

READING_LIST = "reading_list.md"
CROSSREF_API = "https://api.crossref.org/v1/works"

def extract_metadata(paper_text):
    """Extract authors, year, title from paper text.
    Format: "Authors et al. (Year) — Title" or similar
    """
    authors = ""
    year = ""
    title = ""
    
    # Try first pattern with em-dash and unicode letters
    match = re.match(r'^(.+?)\s*\((\d{4})\)\s*\u2014\s*(.+)', paper_text)
    if not match:
        # Try with regular dash
        match = re.match(r'^(.+?)\s*\((\d{4})\)\s*-\s*(.+)', paper_text)
    if not match:
        # Try with any separator
        match = re.match(r'^(.+?)\s*\((\d{4})\).{1,3}(.+)', paper_text)
    
    if match:
        authors = match.group(1).strip()
        year = match.group(2)
        rest = match.group(3).strip()
        # Take everything before comma as title
        title = rest.split(',')[0].strip() if ',' in rest else rest
    
    return authors, year, title

def search_crossref(authors, year, title):
    """Search CrossRef for paper DOI."""
    if not title or len(title) < 5:
        return None
    
    params = {
        'rows': 3,
        'query': title
    }
    
    if year:
        params['query'] += f' {year}'
    
    try:
        resp = requests.get(CROSSREF_API, params=params, timeout=10)
        
        if resp.status_code == 200:
            results = resp.json()
            items = results.get('message', {}).get('items', [])
            
            if items:
                doi = items[0].get('DOI')
                return doi
        return None
    
    except:
        return None

def main():
    print("🔎 CrossRef DOI Lookup\n")
    
    with open(READING_LIST, 'r') as f:
        original_lines = f.readlines()
    
    lines = original_lines.copy()
    
    # Parse all papers
    papers_to_update = []
    for i, line in enumerate(lines):
        if '\t' in line and not line.startswith('#'):
            parts = line.split('\t')
            if len(parts) >= 3 and parts[0].strip().isdigit():
                paper = parts[2].strip()
                # Check if already has DOI
                if not re.search(r'10\.\d+/\S+', paper):
                    papers_to_update.append((i, parts))
    
    print(f"📖 Found {len([p for p in papers_to_update if True])} total")
    print(f"⚠️  {len(papers_to_update)} papers need DOIs\n")
    
    if not papers_to_update:
        print("✅ All papers have DOIs!")
        return
    
    print("🔍 Searching CrossRef...\n")
    
    updates = {}
    for line_num, parts in papers_to_update:
        session = parts[0].strip()
        paper = parts[2].strip()
        
        authors, year, title = extract_metadata(paper)
        
        if not title:
            print(f"  ⚠️  Session {session}: Could not parse")
            continue
        
        print(f"  S{session} ({year}): {title[:50]}...", end='', flush=True)
        
        doi = search_crossref(authors, year, title)
        
        if doi:
            print(f" ✓ {doi}")
            updates[line_num] = doi
        else:
            print(" ✗")
        
        time.sleep(0.5)
    
    # Apply updates
    if updates:
        print(f"\n📝 Updating {READING_LIST}...\n")
        
        for line_num, doi in updates.items():
            parts = original_lines[line_num].rstrip('\n').split('\t')
            # Add DOI to paper field
            parts[2] = parts[2].rstrip() + f' ({doi})'
            new_line = '\t'.join(parts) + '\n'
            lines[line_num] = new_line
            print(f"  ✅ Added {doi}")
        
        with open(READING_LIST, 'w') as f:
            f.writelines(lines)
        
        print(f"\n✅ Updated {len(updates)} papers!")
    else:
        print(f"\n⚠️  0 DOIs found")

if __name__ == '__main__':
    main()

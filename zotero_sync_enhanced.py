#!/usr/bin/env python3
"""
Enhanced Zotero sync - Add papers with metadata from reading_list.md to Zotero
Extracts authors, year, title, journal from paper citations
"""

import re
from pathlib import Path
import requests
import time

CONFIG_FILE = ".zotero_config"
READING_LIST = "reading_list.md"

def load_config():
    config = {}
    with open(CONFIG_FILE) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

def parse_paper_info(paper_text):
    """
    Parse paper info from format: Authors (Year) — *Title*, Journal
    Returns: (authors, year, title, journal, doi)
    """
    authors = ""
    year = ""
    title = ""
    journal = ""
    doi = None
    
    # Extract DOI
    doi_match = re.search(r'10\.\d+/\S+', paper_text)
    doi = doi_match.group(0).rstrip('])') if doi_match else None
    
    # Extract authors and year: "Lastname et al. (YYYY)"
    auth_year = re.match(r'^([A-Za-z\s\.]+et al\.)\s*\((\d{4})\)', paper_text)
    if auth_year:
        authors = auth_year.group(1).strip()
        year = auth_year.group(2)
    
    # Extract title between asterisks: *Title*
    title_match = re.search(r'\*(.*?)\*', paper_text)
    if title_match:
        title = title_match.group(1).strip()
    
    # Extract journal after the last comma
    parts = paper_text.split('*')
    if len(parts) > 2:
        after_title = parts[2]  # Text after closing *
        # Get text after last comma
        journal_parts = after_title.split(',')
        if journal_parts:
            journal = journal_parts[-1].strip().rstrip(')')
    
    return authors, year, title, journal, doi

def parse_reading_list():
    papers = []
    with open(READING_LIST, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.strip() and not line.startswith('#'):
            parts = line.split('\t')
            if len(parts) >= 3 and parts[0].strip().isdigit():
                session = int(parts[0].strip())
                topic = parts[1].strip() if len(parts) > 1 else "TBD"
                paper = parts[2].strip() if len(parts) > 2 else ""
                
                # Parse paper info
                authors, year, title, journal, doi = parse_paper_info(paper)
                
                papers.append({
                    'session': session,
                    'topic': topic,
                    'paper': paper,
                    'authors': authors,
                    'year': year,
                    'title': title,
                    'journal': journal,
                    'doi': doi
                })
    return papers

def sync_to_zotero(config, papers):
    library_id = config['LIBRARY_ID']
    api_key = config['API_KEY']
    base_url = f"https://api.zotero.org/groups/{library_id}"
    headers = {
        "Zotero-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    print(f"🔗 Connected to Zotero (Library: {library_id})")
    print(f"\n📁 Creating folder structure...")
    
    # Get or create Journal Club collection
    url = f"{base_url}/collections"
    resp = requests.get(url, headers=headers)
    collections = resp.json() if resp.status_code == 200 else []
    
    journal_club_key = None
    for col in collections:
        if col.get('data', {}).get('name') == 'Journal Club':
            journal_club_key = col.get('key')
            break
    
    if not journal_club_key:
        data = {"name": "Journal Club"}
        resp = requests.post(url, headers=headers, json=[data])
        if resp.status_code == 200:
            result = resp.json()
            journal_club_key = list(result.get('successful', {}).values())[0].get('key')
    
    if journal_club_key:
        print(f"✅ Journal Club ready")
    
    # Get or create Series 1 collection
    series_name = 'Series 1 - AI & ML in Clinical Microbiology'
    series_key = None
    for col in collections:
        if col.get('data', {}).get('name') == series_name:
            series_key = col.get('key')
            break
    
    if not series_key:
        data = {
            "name": series_name,
            "parentCollection": journal_club_key
        }
        resp = requests.post(url, headers=headers, json=[data])
        if resp.status_code == 200:
            result = resp.json()
            series_key = list(result.get('successful', {}).values())[0].get('key')
    
    if series_key:
        print(f"✅ {series_name} ready")
    
    # Refresh collections list
    resp = requests.get(url, headers=headers)
    collections = resp.json() if resp.status_code == 200 else []
    
    # Create session folders
    session_keys = {}
    for session_num in sorted(set(p['session'] for p in papers)):
        session_name = f"Session {session_num}"
        session_key = None
        
        for col in collections:
            col_data = col.get('data', {})
            if col_data.get('name') == session_name and col_data.get('parentCollection') == series_key:
                session_key = col.get('key')
                break
        
        if not session_key:
            data = {
                "name": session_name,
                "parentCollection": series_key
            }
            resp = requests.post(url, headers=headers, json=[data])
            if resp.status_code == 200:
                result = resp.json()
                response_obj = list(result.get('successful', {}).values())[0]
                session_key = response_obj.get('key') if isinstance(response_obj, dict) else response_obj
        
        session_keys[session_num] = session_key
        print(f"  ✓ Session {session_num} ready")
    
    # Add papers
    print(f"\n📄 Adding papers...")
    added = 0
    failed = 0
    
    items_url = f"{base_url}/items"
    
    for paper in papers:
        session = paper['session']
        topic = paper['topic']
        session_key = session_keys.get(session)
        
        if not session_key:
            print(f"  ⚠️  Session {session} key not found")
            continue
        
        # Create item with metadata
        item = {
            'itemType': 'journalArticle',
            'title': paper['title'] or f"({topic}) {paper['paper'][:80]}",
            'tags': [
                {'tag': f'Session {session}'},
                {'tag': topic}
            ]
        }
        
        # Add optional fields if available
        if paper['authors']:
            # Parse first author
            first_author = paper['authors'].split()[0].rstrip(',')
            item['creators'] = [
                {
                    'firstName': '',
                    'lastName': first_author,
                    'creatorType': 'author'
                }
            ]
        
        if paper['year']:
            item['date'] = paper['year']
        
        if paper['journal']:
            item['publicationTitle'] = paper['journal']
        
        if paper['doi']:
            item['DOI'] = paper['doi']
        
        resp = requests.post(items_url, headers=headers, json=[item])
        
        if resp.status_code == 200:
            result = resp.json()
            successful = result.get('successful', {})
            if successful:
                response_obj = list(successful.values())[0]
                item_key = response_obj.get('key') if isinstance(response_obj, dict) else response_obj
                
                # Add to collection
                coll_url = f"{base_url}/collections/{session_key}/items"
                resp = requests.post(coll_url, headers=headers, data=item_key)
                
                if resp.status_code == 204:
                    print(f"  ✅ Session {session}: {paper['title'][:50] or paper['authors'][:50]}...")
                    added += 1
                else:
                    failed += 1
        else:
            failed += 1
        
        time.sleep(0.1)  # Small delay to avoid rate limiting
    
    print(f"\n{'='*50}")
    print(f"📊 Sync complete!")
    print(f"   ✅ Added: {added}")
    print(f"   ❌ Failed: {failed}")
    print(f"{'='*50}")

def main():
    print("🔄 Zotero Reading List Sync (Enhanced)\n")
    
    config = load_config()
    papers = parse_reading_list()
    print(f"📖 Found {len(papers)} papers\n")
    
    if not papers:
        print("⚠️  No papers found")
        return
    
    # Show parsed metadata
    print("Parsed metadata:")
    for p in papers[:3]:
        print(f"  Title: {p['title'][:50]}")
        print(f"  Authors: {p['authors']}, Year: {p['year']}")
        print(f"  Journal: {p['journal']}\n")
    
    sync_to_zotero(config, papers)
    print("\n✨ Check your Zotero group library!")

if __name__ == '__main__':
    main()

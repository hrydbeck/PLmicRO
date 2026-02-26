#!/usr/bin/env python3
"""
Simple Zotero sync - Add papers from reading_list.md to Zotero
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
                doi_match = re.search(r'10\.\d+/\S+', paper)
                doi = doi_match.group(0).rstrip('])') if doi_match else None
                papers.append({
                    'session': session,
                    'topic': topic,
                    'paper': paper,
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
    
    # Determine which series are needed
    series_definitions = {
        'Series 1 - AI & ML in Clinical Microbiology': range(1, 7),
        'Series 2 - AI and Precision Medicine': range(7, 13),
    }
    
    series_keys = {}
    for series_name, session_range in series_definitions.items():
        # Check if any papers belong to this series
        if any(p['session'] in session_range for p in papers):
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
                series_keys[series_name] = series_key
                print(f"✅ {series_name} ready")
    
    # Refresh collections list
    resp = requests.get(url, headers=headers)
    collections = resp.json() if resp.status_code == 200 else []
    
    # Refresh collections list
    resp = requests.get(url, headers=headers)
    collections = resp.json() if resp.status_code == 200 else []
    
    # Helper to find series key for a session number
    def get_series_key_for_session(session_num):
        for series_name, session_range in series_definitions.items():
            if session_num in session_range and series_name in series_keys:
                return series_keys[series_name]
        return None
    
    # Create session folders
    session_keys = {}
    for session_num in sorted(set(p['session'] for p in papers)):
        session_name = f"Session {session_num}"
        parent_series_key = get_series_key_for_session(session_num)
        if not parent_series_key:
            print(f"  ⚠️  No series found for session {session_num}")
            continue
        session_key = None
        
        for col in collections:
            col_data = col.get('data', {})
            if col_data.get('name') == session_name and col_data.get('parentCollection') == parent_series_key:
                session_key = col.get('key')
                break
        
        if not session_key:
            data = {
                "name": session_name,
                "parentCollection": parent_series_key
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
        
        # Create item
        item = {
            'itemType': 'journalArticle',
            'title': f"({topic}) {paper['paper'][:80]}",
            'tags': [
                {'tag': f'Session {session}'},
                {'tag': topic}
            ]
        }
        
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
                    print(f"  ✅ Session {session}: {paper['paper'][:50]}...")
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
    print("🔄 Zotero Reading List Sync\n")
    
    config = load_config()
    papers = parse_reading_list()
    print(f"📖 Found {len(papers)} papers\n")
    
    if not papers:
        print("⚠️  No papers found")
        return
    
    sync_to_zotero(config, papers)
    print("\n✨ Check your Zotero group library!")

if __name__ == '__main__':
    main()

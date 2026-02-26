#!/usr/bin/env python3
"""
Zotero Reading List Sync
Populates Zotero collections from reading_list.md
"""

import re
from pathlib import Path
import requests
import json

CONFIG_FILE = ".zotero_config"
READING_LIST = "reading_list.md"

class ZoteroSync:
    def __init__(self, library_id, library_type, api_key):
        self.library_id = library_id
        self.library_type = library_type
        self.api_key = api_key
        self.base_url = f"https://api.zotero.org/{library_type}s/{library_id}"
        self.headers = {
            "Zotero-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def list_collections(self):
        """Get all collections."""
        url = f"{self.base_url}/collections"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"Error listing collections: {resp.status_code}")
            return []
    
    def create_collection(self, name, parent_key=None):
        """Create a new collection."""
        url = f"{self.base_url}/collections"
        
        data = {
            "name": name
        }
        if parent_key:
            data["parentCollection"] = parent_key
        
        resp = requests.post(url, headers=self.headers, json=[data])
        
        if resp.status_code == 200:
            result = resp.json()
            if isinstance(result, dict) and 'successful' in result:
                keys = result.get('successful', {})
                if keys:
                    return list(keys.values())[0]
            return result
        else:
            print(f"Error creating collection '{name}': {resp.status_code}")
            if resp.text:
                print(f"  Response: {resp.text[:200]}")
            return None
    
    def get_or_create_collection(self, name, parent_key=None):
        """Get collection if exists, else create it."""
        collections = self.list_collections()
        
        for col in collections:
            col_data = col.get('data', {})
            col_name = col_data.get('name', '')
            col_parent = col_data.get('parentCollection', False)
            
            if col_name == name:
                if (parent_key is None and col_parent is False) or (col_parent == parent_key):
                    return col['key']
        
        # Create if not found
        print(f"  Creating collection: {name}")
        key = self.create_collection(name, parent_key)
        if key:
            print(f"    ✓ Created with key: {key}")
        return key
    
    def create_item(self, item_data, collection_key=None):
        """Create an item in Zotero."""
        url = f"{self.base_url}/items"
        
        resp = requests.post(url, headers=self.headers, json=[item_data])
        
        if resp.status_code == 200:
            result = resp.json()
            if isinstance(result, dict) and 'successful' in result:
                keys = result.get('successful', {})
                if keys:
                    item_key = list(keys.values())[0]
                    
                    # Add to collection if specified
                    if collection_key:
                        self.add_item_to_collection(item_key, collection_key)
                    
                    return item_key
            return result
        else:
            print(f"  Error creating item: {resp.status_code}")
            return None
    
    def add_item_to_collection(self, item_key, collection_key):
        """Add item to collection."""
        url = f"{self.base_url}/collections/{collection_key}/items"
        resp = requests.post(url, headers=self.headers, data=item_key)
        return resp.status_code == 204

def load_config():
    """Load Zotero credentials from config file."""
    config = {}
    if not Path(CONFIG_FILE).exists():
        print(f"❌ Config file not found: {CONFIG_FILE}")
        exit(1)
    
    with open(CONFIG_FILE) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                config[key] = value
    
    return config

def parse_reading_list(filepath):
    """Parse reading_list.md and extract paper information."""
    papers = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if line.strip() and not line.startswith('#'):
            parts = line.split('\t')
            if len(parts) >= 3 and parts[0].strip().isdigit():
                session = int(parts[0].strip())
                topic = parts[1].strip() if len(parts) > 1 else "TBD"
                paper = parts[2].strip() if len(parts) > 2 else ""
                
                # Extract DOI if present
                doi_match = re.search(r'10\.\d+/\S+', paper)
                doi = doi_match.group(0) if doi_match else None
                
                papers.append({
                    'session': session,
                    'topic': topic,
                    'paper': paper,
                    'doi': doi
                })
    
    return papers

def main():
    """Main entry point."""
    print("🔄 Zotero Reading List Sync\n")
    
    # Load config
    config = load_config()
    
    # Parse reading list
    if not Path(READING_LIST).exists():
        print(f"❌ Reading list not found: {READING_LIST}")
        exit(1)
    
    papers = parse_reading_list(READING_LIST)
    print(f"📖 Found {len(papers)} papers in {READING_LIST}\n")
    
    if not papers:
        print("⚠️  No papers found in reading list")
        return
    
    # Initialize Zotero sync
    library_type = config.get('LIBRARY_TYPE', 'user')
    sync = ZoteroSync(config['LIBRARY_ID'], library_type, config['API_KEY'])
    
    print(f"🔗 Connected to Zotero (Library: {config['LIBRARY_ID']}, Type: {library_type})")
    
    # Create folder structure
    print("\n📁 Creating folder structure...")
    journal_club_key = sync.get_or_create_collection('Journal Club')
    if not journal_club_key:
        print("❌ Failed to create Journal Club collection")
        return
    print(f"✅ Journal Club collection ready")
    
    # Create Series folders
    series_map = {}
    for paper in papers:
        series_name = 'Series 1 - AI & ML in Clinical Microbiology'
        
        if series_name not in series_map:
            series_key = sync.get_or_create_collection(series_name, journal_club_key)
            if series_key:
                series_map[series_name] = series_key
                print(f"✅ {series_name} ready")
    
    # Create session folders and add papers
    print("\n📄 Adding papers...")
    added = 0
    failed = 0
    
    session_keys = {}
    
    for paper in papers:
        session = paper['session']
        topic = paper['topic']
        series_name = 'Series 1 - AI & ML in Clinical Microbiology'
        
        if series_name not in series_map:
            continue
        
        series_key = series_map[series_name]
        
        # Create session folder (cache to avoid recreating)
        session_name = f"Session {session}"
        if session not in session_keys:
            session_key = sync.get_or_create_collection(session_name, series_key)
            if session_key:
                session_keys[session] = session_key
            else:
                continue
        else:
            session_key = session_keys[session]
        
        # Add paper
        print(f"\n  📘 Session {session} ({topic}): {paper['paper'][:50]}...")
        
        item = {
            'itemType': 'journalArticle',
            'title': paper['paper'] if not paper['doi'] else f"DOI: {paper['doi']}",
            'tags': [
                {'tag': f'Session {session}'},
                {'tag': topic}
            ]
        }
        
        if paper['doi']:
            item['DOI'] = paper['doi']
        
        if sync.create_item(item, session_key):
            print(f"     ✅ Added")
            added += 1
        else:
            print(f"     ❌ Failed")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"📊 Sync complete!")
    print(f"   ✅ Added: {added}")
    print(f"   ❌ Failed: {failed}")
    print(f"{'='*50}")
    print(f"\n✨ Check your Zotero group library!")

if __name__ == '__main__':
    main()

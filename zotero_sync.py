#!/usr/bin/env python3
"""
Zotero Reading List Sync
Populates Zotero collections from reading_list.md

Setup:
1. Install: pip install pyzotero
2. Get API key from: https://www.zotero.org/settings/keys
3. Get Library ID from: https://www.zotero.org/settings/keys (userID)
4. Create .zotero_config file with:
   API_KEY=your_api_key
   LIBRARY_ID=your_library_id
   LIBRARY_TYPE=user
"""

import os
import re
from pathlib import Path
from pyzotero import zotero

# Configuration
CONFIG_FILE = ".zotero_config"
READING_LIST = "reading_list.md"

def load_config():
    """Load Zotero credentials from config file."""
    config = {}
    if not Path(CONFIG_FILE).exists():
        print(f"❌ Config file not found: {CONFIG_FILE}")
        print(f"\nCreate {CONFIG_FILE} with:")
        print("API_KEY=your_api_key")
        print("LIBRARY_ID=your_library_id")
        print("LIBRARY_TYPE=user  # or 'group' if using group library")
        exit(1)
    
    with open(CONFIG_FILE) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                config[key] = value
    
    return config

def get_zotero_client(config):
    """Initialize Zotero client."""
    return zotero.Zotero(
        config['LIBRARY_ID'],
        config.get('LIBRARY_TYPE', 'user'),
        config['API_KEY']
    )

def parse_reading_list(filepath):
    """Parse reading_list.md and extract paper information."""
    papers = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if line.strip() and not line.startswith('#'):
            # Format: SESSION\tTOPIC\tPAPER\tSTATUS
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

def get_or_create_collection(zotero_client, collection_name, parent_id=None):
    """Get collection by name or create it if it doesn't exist."""
    # List collections
    collections = zotero_client.collections()
    
    for col in collections:
        if col['data']['name'] == collection_name:
            parent_key = col['data'].get('parentCollection', False)
            if (parent_id is None and parent_key is False) or (parent_id == parent_key):
                return col['key']
    
    # Create collection if not found
    template = zotero_client.item_template('collection')
    template['name'] = collection_name
    if parent_id:
        template['parentCollection'] = parent_id
    
    response = zotero_client.create_collections([template])
    if response:
        return response[0]
    return None

def add_paper_by_doi(zotero_client, doi, collection_key, session, topic):
    """Add paper to Zotero using DOI."""
    try:
        template = zotero_client.item_template('journalArticle')
        template['DOI'] = doi
        template['title'] = "See DOI for details"
        template['tags'] = [
            {'tag': f'Session {session}'},
            {'tag': topic}
        ]
        
        response = zotero_client.create_items([template])
        if response:
            item_key = response[0]
            zotero_client.collection_item_add(collection_key, item_key)
            return True
    except Exception as e:
        print(f"  ⚠️  Error adding {doi}: {e}")
        return False

def add_paper_manually(zotero_client, paper_text, collection_key, session, topic):
    """Create a manual entry with the paper text."""
    try:
        template = zotero_client.item_template('journalArticle')
        template['title'] = paper_text[:100]
        template['tags'] = [
            {'tag': f'Session {session}'},
            {'tag': topic}
        ]
        
        response = zotero_client.create_items([template])
        if response:
            item_key = response[0]
            zotero_client.collection_item_add(collection_key, item_key)
            return True
    except Exception as e:
        print(f"  ⚠️  Error adding {paper_text[:50]}: {e}")
        return False

def sync_to_zotero(config, papers):
    """Sync papers to Zotero with folder structure."""
    zotero_client = get_zotero_client(config)
    
    print(f"🔗 Connected to Zotero (Library: {config['LIBRARY_ID']})")
    
    # Create main folder
    journal_club_id = get_or_create_collection(zotero_client, 'Journal Club')
    print(f"✅ Journal Club collection: {journal_club_id}")
    
    # Create Series folders
    series_map = {}
    for paper in papers:
        series_name = 'Series 1 - AI & ML in Clinical Microbiology'
        
        if series_name not in series_map:
            series_id = get_or_create_collection(zotero_client, series_name, journal_club_id)
            series_map[series_name] = series_id
            print(f"✅ {series_name}: {series_id}")
    
    # Create session folders and add papers
    added = 0
    failed = 0
    
    for paper in papers:
        session = paper['session']
        topic = paper['topic']
        series_name = 'Series 1 - AI & ML in Clinical Microbiology'
        series_id = series_map[series_name]
        
        # Create session folder
        session_name = f"Session {session}"
        session_id = get_or_create_collection(zotero_client, session_name, series_id)
        
        # Add paper
        print(f"\n📄 Session {session} ({topic}): {paper['paper'][:60]}...")
        
        if paper['doi']:
            if add_paper_by_doi(zotero_client, paper['doi'], session_id, session, topic):
                print(f"  ✅ Added via DOI")
                added += 1
            else:
                failed += 1
        else:
            if add_paper_manually(zotero_client, paper['paper'], session_id, session, topic):
                print(f"  ✅ Added manually")
                added += 1
            else:
                failed += 1
    
    print(f"\n{'='*50}")
    print(f"📊 Sync complete: {added} added, {failed} failed")
    print(f"{'='*50}")

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
    
    # Sync to Zotero
    sync_to_zotero(config, papers)

if __name__ == '__main__':
    main()

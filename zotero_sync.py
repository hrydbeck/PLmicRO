#!/usr/bin/env python3
"""
Zotero Reading List Sync
Populates Zotero collections from reading_list.md
"""

import re
from pathlib import Path
from pyzotero import zotero

CONFIG_FILE = ".zotero_config"
READING_LIST = "reading_list.md"

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

def get_or_create_collection(zotero_client, collection_name, parent_key=None):
    """Get collection by name or create it if it doesn't exist."""
    try:
        # List existing collections
        collections = zotero_client.collections()
        
        for col in collections:
            col_name = col['data'].get('name', '')
            col_parent = col['data'].get('parentCollection', False)
            
            if col_name == collection_name:
                if (parent_key is None and col_parent is False) or (col_parent == parent_key):
                    return col['key']
        
        # Create collection if not found
        print(f"  Creating collection: {collection_name}")
        collection_data = {
            'name': collection_name
        }
        if parent_key:
            collection_data['parentCollection'] = parent_key
        
        # create_collection returns the key directly as a string
        response = zotero_client.create_collection(collection_data)
        if response:
            print(f"    ✓ Created with key: {response}")
            return response
        return None
        
    except Exception as e:
        print(f"  ⚠️  Error with collection {collection_name}: {e}")
        return None

def add_paper_by_doi(zotero_client, doi, collection_key, session, topic):
    """Add paper to Zotero using DOI."""
    try:
        item = {
            'itemType': 'journalArticle',
            'DOI': doi,
            'title': f'DOI: {doi}',
            'tags': [
                {'tag': f'Session {session}'},
                {'tag': topic}
            ]
        }
        
        response = zotero_client.create_items([item])
        if response:
            item_key = response[0]
            # Add to collection
            try:
                zotero_client.collection_item_add(collection_key, item_key)
            except:
                pass
            return True
    except Exception as e:
        print(f"  ⚠️  Error adding {doi}: {e}")
        return False

def add_paper_manually(zotero_client, paper_text, collection_key, session, topic):
    """Create a manual entry with the paper text."""
    try:
        # Clean up paper text
        title = paper_text[:150]
        if '—' in title:
            title = title.split('—', 1)[1].strip()
        
        item = {
            'itemType': 'journalArticle',
            'title': title,
            'tags': [
                {'tag': f'Session {session}'},
                {'tag': topic}
            ]
        }
        
        response = zotero_client.create_items([item])
        if response:
            item_key = response[0]
            try:
                zotero_client.collection_item_add(collection_key, item_key)
            except:
                pass
            return True
    except Exception as e:
        print(f"  ⚠️  Error adding {paper_text[:50]}: {e}")
        return False

def sync_to_zotero(config, papers):
    """Sync papers to Zotero with folder structure."""
    try:
        zotero_client = get_zotero_client(config)
        print(f"🔗 Connected to Zotero (Library: {config['LIBRARY_ID']})")
    except Exception as e:
        print(f"❌ Failed to connect to Zotero: {e}")
        print("Check your API_KEY and LIBRARY_ID in .zotero_config")
        return
    
    # Create main folder
    print("\n📁 Creating folder structure...")
    journal_club_key = get_or_create_collection(zotero_client, 'Journal Club')
    if not journal_club_key:
        print("❌ Failed to create Journal Club collection")
        return
    print(f"✅ Journal Club collection ready")
    
    # Create Series folders
    series_map = {}
    for paper in papers:
        series_name = 'Series 1 - AI & ML in Clinical Microbiology'
        
        if series_name not in series_map:
            series_key = get_or_create_collection(zotero_client, series_name, journal_club_key)
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
            print(f"⚠️  Series not found for session {session}")
            continue
        
        series_key = series_map[series_name]
        
        # Create session folder (cache to avoid recreating)
        session_name = f"Session {session}"
        if session not in session_keys:
            session_key = get_or_create_collection(zotero_client, session_name, series_key)
            if session_key:
                session_keys[session] = session_key
            else:
                print(f"⚠️  Failed to create {session_name}")
                continue
        else:
            session_key = session_keys[session]
        
        # Add paper
        print(f"\n  📘 Session {session} ({topic}): {paper['paper'][:50]}...")
        
        if paper['doi']:
            if add_paper_by_doi(zotero_client, paper['doi'], session_key, session, topic):
                print(f"     ✅ Added via DOI")
                added += 1
            else:
                failed += 1
        else:
            if add_paper_manually(zotero_client, paper['paper'], session_key, session, topic):
                print(f"     ✅ Added manually")
                added += 1
            else:
                failed += 1
    
    print(f"\n{'='*50}")
    print(f"📊 Sync complete!")
    print(f"   ✅ Added: {added}")
    print(f"   ❌ Failed: {failed}")
    print(f"{'='*50}")
    print(f"\n✨ Check your Zotero group library!")

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
    
    # Sync to Zotero
    sync_to_zotero(config, papers)

if __name__ == '__main__':
    main()

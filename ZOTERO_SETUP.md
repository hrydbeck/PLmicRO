# Zotero Integration Guide

This folder includes a script to automatically populate your Zotero library with papers from the reading list.

## Setup

### 1. Create Zotero API Key

1. Go to https://www.zotero.org/settings/keys
2. Generate a new API key
3. Copy it (you'll need it in the next step)

### 2. Find Your Library ID

**For Personal Library:**
- At https://www.zotero.org/settings/keys, look for **userID** (e.g., `12345678`)
- This is your Library ID

**For Group Library:**
- Go to https://www.zotero.org/groups
- Click on your group (e.g., "Journal Club")
- Copy the number from the URL: `zotero.org/groups/YOUR_GROUP_ID`
- Format as: `group/YOUR_GROUP_ID`

### 3. Create Configuration File

1. Copy the example config:
   ```bash
   cp .zotero_config.example .zotero_config
   ```

2. Edit `.zotero_config` and fill in your values:
   ```
   API_KEY=your_actual_api_key
   LIBRARY_ID=your_library_id_or_group_id
   LIBRARY_TYPE=user  # or 'group' if using group library
   ```

⚠️ **IMPORTANT**: Add `.zotero_config` to `.gitignore` so you don't commit your API key!

### 4. Install Dependencies

```bash
pip install pyzotero
```

## Usage

Run the sync script:

```bash
python3 zotero_sync.py
```

This will:
1. ✅ Create a "Journal Club" folder in Zotero
2. ✅ Create "Series 1", "Series 2", etc. subfolders
3. ✅ Create "Session 1", "Session 2", etc. subfolders
4. ✅ Add papers with automatic tagging (Session #, Topic)

## Folder Structure Created

```
📦 Journal Club
├── 📁 Series 1 - AI & ML in Clinical Microbiology
│   ├── 📁 Session 1
│   │   └── 📄 Greener et al. ...
│   ├── 📁 Session 2
│   │   ├── 📄 Topçuoğlu et al. ...
│   │   └── 📄 Wheeler et al. ...
│   └── ...
└── 📁 Series 2 - AI and Precision Medicine
    └── (Papers to be added)
```

## Notes

- Papers with DOIs are easier to add (Zotero can fetch metadata)
- Papers without DOIs get basic manual entries
- After sync, check Zotero and manually add missing metadata (journal names, year, etc.)
- Tags are automatically added for Session and Topic

## Limitations

- Some papers may need manual metadata enrichment
- Very old papers might not have comprehensive DOI coverage

## Troubleshooting

**"Config file not found"**
- Create `.zotero_config` with your API key and Library ID

**"Authentication failed"**
- Check your API key is correct
- Verify Library ID matches your account

**"Collection already exists"**
- The script won't duplicate collections - it reuses existing ones

**Papers showing as basic entries**
- Manually edit in Zotero to add proper titles, journals, and metadata

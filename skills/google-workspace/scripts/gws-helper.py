#!/usr/bin/env python3
"""
Google Workspace CLI Helper Script
Provides simplified interface for common Google Workspace operations using gws CLI.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def run_gws_command(args):
    """Run a gws command and return the result."""
    cmd = ['gws'] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout) if result.stdout else None
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        return result.stdout

def create_spreadsheet(title, data=None):
    """Create a new Google Spreadsheet with optional data."""
    body = {'properties': {'title': title}}
    
    if data:
        body['sheets'] = [{
            'properties': {
                'title': 'Sheet1',
                'gridProperties': {
                    'rowCount': len(data) + 10,
                    'columnCount': max(len(row) for row in data) + 5
                }
            }
        }]
    
    result = run_gws_command([
        'sheets', 'spreadsheets', 'create',
        '--json', json.dumps(body)
    ])
    
    if result and 'spreadsheetId' in result:
        spreadsheet_id = result['spreadsheetId']
        
        if data:
            # Write data to the spreadsheet
            write_to_spreadsheet(spreadsheet_id, 'Sheet1!A1', data)
        
        return {
            'id': spreadsheet_id,
            'url': f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        }
    
    return None

def write_to_spreadsheet(spreadsheet_id, range_name, values):
    """Write data to a spreadsheet."""
    body = {'values': values}
    
    result = run_gws_command([
        'sheets', 'spreadsheets', 'values', 'update',
        '--params', json.dumps({
            'spreadsheetId': spreadsheet_id,
            'range': range_name,
            'valueInputOption': 'USER_ENTERED'
        }),
        '--json', json.dumps(body)
    ])
    
    return result

def read_spreadsheet(spreadsheet_id, range_name):
    """Read data from a spreadsheet."""
    result = run_gws_command([
        'sheets', 'spreadsheets', 'values', 'get',
        '--params', json.dumps({
            'spreadsheetId': spreadsheet_id,
            'range': range_name
        })
    ])
    
    return result.get('values', []) if result else []

def create_document(title, content=None):
    """Create a new Google Doc with optional content."""
    body = {'title': title}
    
    result = run_gws_command([
        'docs', 'documents', 'create',
        '--json', json.dumps(body)
    ])
    
    if result and 'documentId' in result:
        document_id = result['documentId']
        
        if content:
            # Write content to the document
            write_to_document(document_id, content)
        
        return {
            'id': document_id,
            'url': f"https://docs.google.com/document/d/{document_id}/edit"
        }
    
    return None

def write_to_document(document_id, content):
    """Write content to a Google Doc."""
    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': content
        }
    }]
    
    body = {'requests': requests}
    
    result = run_gws_command([
        'docs', 'documents', 'batchUpdate',
        '--params', json.dumps({'documentId': document_id}),
        '--json', json.dumps(body)
    ])
    
    return result

def read_document(document_id):
    """Read content from a Google Doc."""
    result = run_gws_command([
        'docs', 'documents', 'get',
        '--params', json.dumps({'documentId': document_id})
    ])
    
    return result

def list_files(page_size=10):
    """List files in Google Drive."""
    result = run_gws_command([
        'drive', 'files', 'list',
        '--params', json.dumps({'pageSize': page_size})
    ])
    
    return result.get('files', []) if result else []

def upload_file(file_path, mime_type=None):
    """Upload a file to Google Drive."""
    params = {}
    if mime_type:
        params['mimeType'] = mime_type
    
    args = [
        'drive', 'files', 'create',
        '--params', json.dumps(params),
        '--upload', file_path
    ]
    
    if mime_type:
        args.extend(['--upload-content-type', mime_type])
    
    result = run_gws_command(args)
    return result

def share_file(file_id, email, role='writer'):
    """Share a file with a user."""
    body = {
        'role': role,
        'type': 'user',
        'emailAddress': email
    }
    
    result = run_gws_command([
        'drive', 'permissions', 'create',
        '--params', json.dumps({'fileId': file_id}),
        '--json', json.dumps(body)
    ])
    
    return result

def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: gws-helper.py <command> [args...]")
        print("Commands:")
        print("  create-sheet <title> [data.json]")
        print("  write-sheet <spreadsheet_id> <range> <data.json>")
        print("  read-sheet <spreadsheet_id> <range>")
        print("  create-doc <title> [content.txt]")
        print("  read-doc <document_id>")
        print("  list-files [page_size]")
        print("  upload <file_path> [mime_type]")
        print("  share <file_id> <email> [role]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create-sheet':
        title = sys.argv[2]
        data = None
        if len(sys.argv) > 3:
            with open(sys.argv[3]) as f:
                data = json.load(f)
        result = create_spreadsheet(title, data)
        print(json.dumps(result, indent=2))
    
    elif command == 'write-sheet':
        spreadsheet_id = sys.argv[2]
        range_name = sys.argv[3]
        with open(sys.argv[4]) as f:
            data = json.load(f)
        result = write_to_spreadsheet(spreadsheet_id, range_name, data)
        print(json.dumps(result, indent=2))
    
    elif command == 'read-sheet':
        spreadsheet_id = sys.argv[2]
        range_name = sys.argv[3]
        result = read_spreadsheet(spreadsheet_id, range_name)
        print(json.dumps(result, indent=2))
    
    elif command == 'create-doc':
        title = sys.argv[2]
        content = None
        if len(sys.argv) > 3:
            with open(sys.argv[3]) as f:
                content = f.read()
        result = create_document(title, content)
        print(json.dumps(result, indent=2))
    
    elif command == 'read-doc':
        document_id = sys.argv[2]
        result = read_document(document_id)
        print(json.dumps(result, indent=2))
    
    elif command == 'list-files':
        page_size = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        result = list_files(page_size)
        print(json.dumps(result, indent=2))
    
    elif command == 'upload':
        file_path = sys.argv[2]
        mime_type = sys.argv[3] if len(sys.argv) > 3 else None
        result = upload_file(file_path, mime_type)
        print(json.dumps(result, indent=2))
    
    elif command == 'share':
        file_id = sys.argv[2]
        email = sys.argv[3]
        role = sys.argv[4] if len(sys.argv) > 4 else 'writer'
        result = share_file(file_id, email, role)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()

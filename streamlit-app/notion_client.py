"""
Notion API Client with enhanced functionality for DanceSport Assistant
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class NotionClient:
    """Enhanced Notion API client with support for comments and advanced queries"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def get_integration_info(self) -> Dict:
        """Get integration bot information"""
        url = f"{self.base_url}/users/me"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def search_all(self, query: str = "", page_size: int = 100) -> Dict:
        """Search all pages and databases"""
        url = f"{self.base_url}/search"
        payload = {"page_size": page_size}
        if query:
            payload["query"] = query
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_page(self, page_id: str) -> Dict:
        """Get a specific page by ID"""
        url = f"{self.base_url}/pages/{page_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_block_children(self, block_id: str) -> Dict:
        """Get children blocks of a page or block"""
        url = f"{self.base_url}/blocks/{block_id}/children"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_database(self, database_id: str) -> Dict:
        """Get database schema"""
        url = f"{self.base_url}/databases/{database_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def query_database(self, database_id: str, filter_obj: Optional[Dict] = None, 
                      sorts: Optional[List] = None) -> Dict:
        """Query database with filters and sorting"""
        url = f"{self.base_url}/databases/{database_id}/query"
        payload = {}
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def add_comment(self, page_id: str, comment_text: str) -> Dict:
        """Add a comment to a page or discussion"""
        url = f"{self.base_url}/comments"
        payload = {
            "parent": {"page_id": page_id},
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": comment_text}
                }
            ]
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_comments(self, page_id: str) -> List[Dict]:
        """Get all comments for a page"""
        url = f"{self.base_url}/comments"
        params = {"block_id": page_id}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get('results', [])
    
    def update_page_properties(self, page_id: str, properties: Dict) -> Dict:
        """Update page properties"""
        url = f"{self.base_url}/pages/{page_id}"
        payload = {"properties": properties}
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def append_block_children(self, block_id: str, children: List[Dict]) -> Dict:
        """Append blocks to a page"""
        url = f"{self.base_url}/blocks/{block_id}/children"
        payload = {"children": children}
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


class WorkspaceAnalyzer:
    """Helper class to analyze Notion workspace structure"""
    
    def __init__(self, notion_client: NotionClient):
        self.notion = notion_client
    
    def extract_title(self, obj: Dict) -> str:
        """Extract title from a page or database object"""
        if obj.get('object') == 'page':
            properties = obj.get('properties', {})
            for prop_value in properties.values():
                if prop_value.get('type') == 'title':
                    title_array = prop_value.get('title', [])
                    if title_array:
                        return title_array[0].get('plain_text', 'Untitled')
        elif obj.get('object') == 'database':
            title_array = obj.get('title', [])
            if title_array:
                return title_array[0].get('plain_text', 'Untitled Database')
        return 'Untitled'
    
    def build_hierarchy(self, all_objects: List[Dict]) -> Dict:
        """Build workspace hierarchy from objects"""
        pages = [obj for obj in all_objects if obj.get('object') == 'page']
        databases = [obj for obj in all_objects if obj.get('object') == 'database']
        
        workspace_data = {
            "total_objects": len(all_objects),
            "total_pages": len(pages),
            "total_databases": len(databases),
            "main_pages": [],
            "databases_by_parent": {},
            "pages_by_parent": {}
        }
        
        # Process pages
        for page in pages:
            parent = page.get('parent', {})
            parent_type = parent.get('type')
            parent_id = None
            
            if parent_type == 'page_id':
                parent_id = parent.get('page_id')
            elif parent_type == 'database_id':
                parent_id = parent.get('database_id')
            
            page_info = {
                'id': page.get('id'),
                'title': self.extract_title(page),
                'created_time': page.get('created_time'),
                'url': page.get('url'),
                'parent_id': parent_id,
                'parent_type': parent_type,
                'object': page
            }
            
            if parent_id is None:
                workspace_data['main_pages'].append(page_info)
            else:
                if parent_id not in workspace_data['pages_by_parent']:
                    workspace_data['pages_by_parent'][parent_id] = []
                workspace_data['pages_by_parent'][parent_id].append(page_info)
        
        # Process databases
        for db in databases:
            parent = db.get('parent', {})
            parent_type = parent.get('type')
            parent_id = parent.get('page_id') if parent_type == 'page_id' else None
            
            db_info = {
                'id': db.get('id'),
                'title': self.extract_title(db),
                'created_time': db.get('created_time'),
                'url': db.get('url'),
                'parent_id': parent_id,
                'parent_type': parent_type,
                'object': db
            }
            
            if parent_id not in workspace_data['databases_by_parent']:
                workspace_data['databases_by_parent'][parent_id] = []
            workspace_data['databases_by_parent'][parent_id].append(db_info)
        
        return workspace_data
    
    def find_dancesport_content(self, workspace_data: Dict) -> Dict:
        """Find DanceSport-related pages and databases"""
        dancesport_items = {
            'main_page': None,
            'dance_categories': [],
            'all_dances': []
        }
        
        # Find main DanceSport page
        for page in workspace_data['main_pages']:
            if 'dancesport' in page['title'].lower():
                dancesport_items['main_page'] = page
                break
        
        if not dancesport_items['main_page']:
            return dancesport_items
        
        # Find dance categories (Fundamental, Open)
        main_page_id = dancesport_items['main_page']['id']
        databases = workspace_data['databases_by_parent'].get(main_page_id, [])
        
        for db in databases:
            title_lower = db['title'].lower()
            if 'fundamental' in title_lower or 'open' in title_lower:
                # Get individual dances from this category
                dance_dbs = workspace_data['databases_by_parent'].get(db['id'], [])
                for dance_db in dance_dbs:
                    dancesport_items['dance_categories'].append({
                        'category': db['title'],
                        'dance': dance_db['title'],
                        'database_id': dance_db['id']
                    })
        
        return dancesport_items

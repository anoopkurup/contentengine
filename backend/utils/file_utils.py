import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import zipfile

class FileManager:
    """Utility class for file operations in ContentEngine projects"""
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """Read text content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    @staticmethod
    def write_text_file(file_path: str, content: str) -> bool:
        """Write text content to a file"""
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return False
    
    @staticmethod
    def read_json_file(file_path: str) -> Dict[str, Any]:
        """Read JSON content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return {}
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict[str, Any]) -> bool:
        """Write JSON data to a file"""
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing JSON file {file_path}: {e}")
            return False
    
    @staticmethod
    def list_files_in_directory(directory: str, extension: str = None) -> List[str]:
        """List files in a directory, optionally filtered by extension"""
        try:
            directory_path = Path(directory)
            if not directory_path.exists():
                return []
            
            files = []
            for file_path in directory_path.iterdir():
                if file_path.is_file():
                    if extension is None or file_path.suffix == extension:
                        files.append(str(file_path))
            
            return sorted(files)
        except Exception as e:
            print(f"Error listing files in {directory}: {e}")
            return []
    
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy a file from source to destination"""
        try:
            Path(destination).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Error copying file from {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def move_file(source: str, destination: str) -> bool:
        """Move a file from source to destination"""
        try:
            Path(destination).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(source, destination)
            return True
        except Exception as e:
            print(f"Error moving file from {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete a file"""
        try:
            Path(file_path).unlink()
            return True
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get detailed file information"""
        try:
            path = Path(file_path)
            stat = path.stat()
            
            return {
                "name": path.name,
                "size": stat.st_size,
                "size_human": FileManager.format_file_size(stat.st_size),
                "modified": stat.st_mtime,
                "extension": path.suffix,
                "is_file": path.is_file(),
                "is_dir": path.is_dir()
            }
        except Exception:
            return {}
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    @staticmethod
    def create_zip_archive(source_dir: str, zip_path: str, 
                          exclude_patterns: List[str] = None) -> bool:
        """Create a zip archive of a directory"""
        try:
            exclude_patterns = exclude_patterns or []
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                source_path = Path(source_dir)
                
                for file_path in source_path.rglob('*'):
                    if file_path.is_file():
                        # Check if file should be excluded
                        should_exclude = False
                        for pattern in exclude_patterns:
                            if pattern in str(file_path):
                                should_exclude = True
                                break
                        
                        if not should_exclude:
                            relative_path = file_path.relative_to(source_path)
                            zipf.write(file_path, relative_path)
            
            return True
        except Exception as e:
            print(f"Error creating zip archive: {e}")
            return False

class ContentFileManager:
    """Specialized file manager for ContentEngine content files"""
    
    @staticmethod
    def parse_keywords_from_text(text: str) -> List[str]:
        """Parse keywords from text input (comma or newline separated)"""
        # Split by commas and newlines, clean up whitespace
        keywords = []
        for line in text.replace(',', '\n').split('\n'):
            keyword = line.strip()
            if keyword:
                keywords.append(keyword)
        return keywords
    
    @staticmethod
    def format_keywords_for_display(keywords: List[str]) -> str:
        """Format keywords list for display"""
        return '\n'.join(keywords)
    
    @staticmethod
    def extract_content_from_json(json_file: str, content_key: str = "content") -> str:
        """Extract content from a JSON file"""
        data = FileManager.read_json_file(json_file)
        return data.get(content_key, "")
    
    @staticmethod
    def save_content_with_metadata(file_path: str, content: str, 
                                 metadata: Dict[str, Any]) -> bool:
        """Save content with associated metadata"""
        data = {
            "content": content,
            "metadata": metadata,
            "generated_at": FileManager.get_current_timestamp()
        }
        return FileManager.write_json_file(file_path, data)
    
    @staticmethod
    def get_current_timestamp() -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    @staticmethod
    def analyze_content_metrics(content: str) -> Dict[str, Any]:
        """Analyze content metrics (word count, reading time, etc.)"""
        import re
        
        # Basic metrics
        word_count = len(content.split())
        char_count = len(content)
        char_count_no_spaces = len(content.replace(' ', ''))
        
        # Estimate reading time (average 200 words per minute)
        reading_time = max(1, round(word_count / 200))
        
        # Count paragraphs (rough estimate)
        paragraphs = len([p for p in content.split('\n\n') if p.strip()])
        
        # Count sentences (rough estimate)
        sentences = len(re.split(r'[.!?]+', content))
        
        return {
            "word_count": word_count,
            "character_count": char_count,
            "character_count_no_spaces": char_count_no_spaces,
            "estimated_reading_time": reading_time,
            "paragraph_count": paragraphs,
            "sentence_count": sentences,
            "avg_words_per_sentence": round(word_count / max(1, sentences), 1) if sentences > 0 else 0
        }
    
    @staticmethod
    def extract_headings_from_markdown(markdown_content: str) -> List[Dict[str, Any]]:
        """Extract headings from markdown content"""
        import re
        
        headings = []
        lines = markdown_content.split('\n')
        
        for i, line in enumerate(lines):
            # Match markdown headings
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                level = len(match.group(1))
                text = match.group(2)
                headings.append({
                    "level": level,
                    "text": text,
                    "line_number": i + 1
                })
        
        return headings
    
    @staticmethod
    def generate_table_of_contents(markdown_content: str) -> str:
        """Generate a table of contents from markdown headings"""
        headings = ContentFileManager.extract_headings_from_markdown(markdown_content)
        
        if not headings:
            return ""
        
        toc_lines = ["## Table of Contents", ""]
        
        for heading in headings:
            # Skip H1 (usually the main title)
            if heading["level"] == 1:
                continue
            
            indent = "  " * (heading["level"] - 2)
            # Create anchor link (simplified)
            anchor = heading["text"].lower().replace(" ", "-").replace(",", "").replace(".", "")
            toc_lines.append(f"{indent}- [{heading['text']}](#{anchor})")
        
        toc_lines.append("")
        return '\n'.join(toc_lines)
    
    @staticmethod
    def validate_content_structure(content: str, content_type: str) -> Dict[str, Any]:
        """Validate content structure based on type"""
        issues = []
        
        if content_type == "article":
            # Check for basic article structure
            if not content.strip():
                issues.append("Content is empty")
            elif len(content.split()) < 500:
                issues.append("Article is too short (less than 500 words)")
            
            # Check for headings
            headings = ContentFileManager.extract_headings_from_markdown(content)
            if len(headings) < 3:
                issues.append("Article should have at least 3 headings for good structure")
        
        elif content_type == "social_post":
            if not content.strip():
                issues.append("Post content is empty")
            elif len(content) > 2000:
                issues.append("Post is too long for most social platforms")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "content_metrics": ContentFileManager.analyze_content_metrics(content)
        }
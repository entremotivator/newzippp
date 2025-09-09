"""
Local Image Library Management System
Provides comprehensive image storage, categorization, and AI-powered search capabilities
"""

import os
import json
import hashlib
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import base64
from PIL import Image, ImageFilter, ImageEnhance
import streamlit as st

class ImageLibrary:
    """Main class for managing the local image library"""
    
    def __init__(self, library_path: str = "assets/images"):
        self.library_path = Path(library_path)
        self.library_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different categories
        self.categories = {
            "business": "Business & Corporate",
            "icons": "Icons & Symbols", 
            "backgrounds": "Backgrounds & Textures",
            "logos": "Logos & Branding",
            "people": "People & Portraits",
            "objects": "Objects & Products",
            "nature": "Nature & Landscapes",
            "abstract": "Abstract & Artistic",
            "templates": "Templates & Layouts",
            "uploads": "User Uploads"
        }
        
        for category in self.categories.keys():
            (self.library_path / category).mkdir(exist_ok=True)
            (self.library_path / category / "thumbnails").mkdir(exist_ok=True)
        
        # Initialize database
        self.db_path = self.library_path / "library.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database for image metadata"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                original_name TEXT NOT NULL,
                category TEXT NOT NULL,
                file_path TEXT NOT NULL,
                thumbnail_path TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL,
                format TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0,
                favorite BOOLEAN DEFAULT FALSE,
                tags TEXT,
                description TEXT,
                color_palette TEXT,
                dominant_colors TEXT,
                has_transparency BOOLEAN DEFAULT FALSE,
                ai_description TEXT,
                similarity_hash TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_name TEXT UNIQUE NOT NULL,
                usage_count INTEGER DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                image_ids TEXT
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON images(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags ON images(tags)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON images(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_count ON images(usage_count)")
        
        conn.commit()
        conn.close()
    
    def add_image(self, 
                  file_data: bytes, 
                  filename: str, 
                  category: str = "uploads",
                  tags: List[str] = None,
                  description: str = "") -> str:
        """Add a new image to the library"""
        
        if category not in self.categories:
            category = "uploads"
        
        # Generate unique ID based on file content
        file_hash = hashlib.md5(file_data).hexdigest()
        image_id = f"{category}_{file_hash[:12]}"
        
        # Check if image already exists
        if self._image_exists(image_id):
            return image_id
        
        try:
            # Process the image
            image = Image.open(io.BytesIO(file_data))
            
            # Get image info
            width, height = image.size
            format_name = image.format or "PNG"
            has_transparency = image.mode in ('RGBA', 'LA') or 'transparency' in image.info
            
            # Generate file paths
            file_extension = Path(filename).suffix.lower() or f".{format_name.lower()}"
            safe_filename = f"{image_id}{file_extension}"
            file_path = self.library_path / category / safe_filename
            thumbnail_path = self.library_path / category / "thumbnails" / f"{image_id}_thumb.jpg"
            
            # Save original image
            if image.mode == 'RGBA' and format_name.upper() in ['JPEG', 'JPG']:
                # Convert RGBA to RGB for JPEG
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            
            image.save(file_path, format=format_name, quality=95, optimize=True)
            
            # Generate thumbnail
            self._generate_thumbnail(image, thumbnail_path)
            
            # Extract color information
            color_info = self._extract_color_info(image)
            
            # Generate AI description (placeholder for now)
            ai_description = self._generate_ai_description(image)
            
            # Calculate similarity hash
            similarity_hash = self._calculate_similarity_hash(image)
            
            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO images (
                    id, filename, original_name, category, file_path, thumbnail_path,
                    file_size, width, height, format, tags, description,
                    color_palette, dominant_colors, has_transparency,
                    ai_description, similarity_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                image_id, safe_filename, filename, category,
                str(file_path), str(thumbnail_path),
                len(file_data), width, height, format_name,
                json.dumps(tags or []), description,
                json.dumps(color_info['palette']), json.dumps(color_info['dominant']),
                has_transparency, ai_description, similarity_hash
            ))
            
            # Update tag usage
            if tags:
                for tag in tags:
                    cursor.execute("""
                        INSERT OR IGNORE INTO tags (tag_name, usage_count) VALUES (?, 0)
                    """, (tag,))
                    cursor.execute("""
                        UPDATE tags SET usage_count = usage_count + 1 WHERE tag_name = ?
                    """, (tag,))
            
            conn.commit()
            conn.close()
            
            return image_id
            
        except Exception as e:
            st.error(f"Error adding image to library: {str(e)}")
            return None
    
    def _image_exists(self, image_id: str) -> bool:
        """Check if an image already exists in the library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM images WHERE id = ?", (image_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def _generate_thumbnail(self, image: Image.Image, thumbnail_path: Path, size: Tuple[int, int] = (150, 150)):
        """Generate a thumbnail for the image"""
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Create a square thumbnail with padding if needed
        if thumbnail.size != size:
            square_thumb = Image.new('RGB', size, (240, 240, 240))
            paste_x = (size[0] - thumbnail.size[0]) // 2
            paste_y = (size[1] - thumbnail.size[1]) // 2
            square_thumb.paste(thumbnail, (paste_x, paste_y))
            thumbnail = square_thumb
        
        thumbnail.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
    
    def _extract_color_info(self, image: Image.Image) -> Dict[str, Any]:
        """Extract color palette and dominant colors from image"""
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize for faster processing
        small_image = image.resize((100, 100))
        
        # Get color palette
        palette_image = small_image.quantize(colors=8)
        palette = palette_image.getpalette()
        
        # Extract dominant colors
        colors = []
        if palette:
            for i in range(0, min(24, len(palette)), 3):
                if i + 2 < len(palette):
                    colors.append([palette[i], palette[i+1], palette[i+2]])
        
        # Get the most dominant colors
        dominant_colors = colors[:5] if colors else []
        
        return {
            'palette': colors,
            'dominant': dominant_colors
        }
    
    def _generate_ai_description(self, image: Image.Image) -> str:
        """Generate AI description for the image (placeholder implementation)"""
        # This would integrate with an AI vision model
        # For now, return a basic description based on image properties
        
        width, height = image.size
        aspect_ratio = width / height
        
        if aspect_ratio > 1.5:
            orientation = "landscape"
        elif aspect_ratio < 0.75:
            orientation = "portrait"
        else:
            orientation = "square"
        
        # Basic description based on image characteristics
        descriptions = []
        
        if image.mode == 'RGBA':
            descriptions.append("transparent background")
        
        if width > 1920 or height > 1920:
            descriptions.append("high resolution")
        elif width < 500 and height < 500:
            descriptions.append("small size")
        
        descriptions.append(f"{orientation} orientation")
        
        return f"Image with {', '.join(descriptions)}"
    
    def _calculate_similarity_hash(self, image: Image.Image) -> str:
        """Calculate a perceptual hash for image similarity detection"""
        # Simple implementation using average hash
        # Convert to grayscale and resize
        gray = image.convert('L').resize((8, 8), Image.Resampling.LANCZOS)
        
        # Calculate average pixel value
        pixels = list(gray.getdata())
        avg = sum(pixels) / len(pixels)
        
        # Create hash based on whether each pixel is above or below average
        hash_bits = []
        for pixel in pixels:
            hash_bits.append('1' if pixel > avg else '0')
        
        # Convert to hexadecimal
        hash_string = ''.join(hash_bits)
        hash_int = int(hash_string, 2)
        return format(hash_int, '016x')
    
    def search_images(self, 
                     query: str = "",
                     category: str = None,
                     tags: List[str] = None,
                     color: str = None,
                     min_width: int = None,
                     max_width: int = None,
                     min_height: int = None,
                     max_height: int = None,
                     has_transparency: bool = None,
                     favorites_only: bool = False,
                     limit: int = 50) -> List[Dict[str, Any]]:
        """Search images in the library with various filters"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build query
        where_conditions = []
        params = []
        
        if query:
            where_conditions.append("(filename LIKE ? OR description LIKE ? OR ai_description LIKE ? OR tags LIKE ?)")
            query_param = f"%{query}%"
            params.extend([query_param, query_param, query_param, query_param])
        
        if category:
            where_conditions.append("category = ?")
            params.append(category)
        
        if tags:
            for tag in tags:
                where_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
        
        if min_width:
            where_conditions.append("width >= ?")
            params.append(min_width)
        
        if max_width:
            where_conditions.append("width <= ?")
            params.append(max_width)
        
        if min_height:
            where_conditions.append("height >= ?")
            params.append(min_height)
        
        if max_height:
            where_conditions.append("height <= ?")
            params.append(max_height)
        
        if has_transparency is not None:
            where_conditions.append("has_transparency = ?")
            params.append(has_transparency)
        
        if favorites_only:
            where_conditions.append("favorite = 1")
        
        # Construct final query
        base_query = "SELECT * FROM images"
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        base_query += " ORDER BY usage_count DESC, created_at DESC"
        
        if limit:
            base_query += f" LIMIT {limit}"
        
        cursor.execute(base_query, params)
        results = cursor.fetchall()
        
        # Convert to dictionaries
        columns = [description[0] for description in cursor.description]
        images = []
        
        for row in results:
            image_dict = dict(zip(columns, row))
            # Parse JSON fields
            image_dict['tags'] = json.loads(image_dict['tags'] or '[]')
            image_dict['color_palette'] = json.loads(image_dict['color_palette'] or '[]')
            image_dict['dominant_colors'] = json.loads(image_dict['dominant_colors'] or '[]')
            images.append(image_dict)
        
        conn.close()
        return images
    
    def get_image_data(self, image_id: str) -> Optional[bytes]:
        """Get the raw image data for an image ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT file_path FROM images WHERE id = ?", (image_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            file_path = Path(result[0])
            if file_path.exists():
                return file_path.read_bytes()
        
        return None
    
    def get_thumbnail_data(self, image_id: str) -> Optional[bytes]:
        """Get the thumbnail data for an image ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT thumbnail_path FROM images WHERE id = ?", (image_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            thumbnail_path = Path(result[0])
            if thumbnail_path.exists():
                return thumbnail_path.read_bytes()
        
        return None
    
    def update_image_usage(self, image_id: str):
        """Increment the usage count for an image"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE images SET usage_count = usage_count + 1, modified_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (image_id,))
        conn.commit()
        conn.close()
    
    def toggle_favorite(self, image_id: str) -> bool:
        """Toggle favorite status of an image"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current status
        cursor.execute("SELECT favorite FROM images WHERE id = ?", (image_id,))
        result = cursor.fetchone()
        
        if result:
            new_status = not bool(result[0])
            cursor.execute("""
                UPDATE images SET favorite = ?, modified_at = CURRENT_TIMESTAMP WHERE id = ?
            """, (new_status, image_id))
            conn.commit()
            conn.close()
            return new_status
        
        conn.close()
        return False
    
    def delete_image(self, image_id: str) -> bool:
        """Delete an image from the library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get file paths
        cursor.execute("SELECT file_path, thumbnail_path FROM images WHERE id = ?", (image_id,))
        result = cursor.fetchone()
        
        if result:
            file_path, thumbnail_path = result
            
            # Delete files
            try:
                if Path(file_path).exists():
                    Path(file_path).unlink()
                if Path(thumbnail_path).exists():
                    Path(thumbnail_path).unlink()
            except Exception as e:
                st.error(f"Error deleting files: {str(e)}")
            
            # Delete from database
            cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def get_categories_with_counts(self) -> Dict[str, int]:
        """Get all categories with image counts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT category, COUNT(*) FROM images GROUP BY category")
        results = cursor.fetchall()
        conn.close()
        
        categories = {}
        for category, count in results:
            categories[category] = count
        
        return categories
    
    def get_popular_tags(self, limit: int = 20) -> List[Tuple[str, int]]:
        """Get most popular tags"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT tag_name, usage_count FROM tags ORDER BY usage_count DESC LIMIT ?", (limit,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_similar_images(self, image_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find images similar to the given image"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get the similarity hash of the target image
        cursor.execute("SELECT similarity_hash FROM images WHERE id = ?", (image_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return []
        
        target_hash = result[0]
        
        # Get all images with their hashes
        cursor.execute("SELECT id, similarity_hash FROM images WHERE id != ?", (image_id,))
        all_images = cursor.fetchall()
        
        # Calculate Hamming distances
        similarities = []
        for img_id, img_hash in all_images:
            if img_hash:
                distance = self._hamming_distance(target_hash, img_hash)
                similarities.append((img_id, distance))
        
        # Sort by similarity (lower distance = more similar)
        similarities.sort(key=lambda x: x[1])
        
        # Get details for most similar images
        similar_ids = [img_id for img_id, _ in similarities[:limit]]
        
        if similar_ids:
            placeholders = ','.join(['?' for _ in similar_ids])
            cursor.execute(f"SELECT * FROM images WHERE id IN ({placeholders})", similar_ids)
            results = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            similar_images = []
            
            for row in results:
                image_dict = dict(zip(columns, row))
                image_dict['tags'] = json.loads(image_dict['tags'] or '[]')
                image_dict['color_palette'] = json.loads(image_dict['color_palette'] or '[]')
                image_dict['dominant_colors'] = json.loads(image_dict['dominant_colors'] or '[]')
                similar_images.append(image_dict)
        else:
            similar_images = []
        
        conn.close()
        return similar_images
    
    def _hamming_distance(self, hash1: str, hash2: str) -> int:
        """Calculate Hamming distance between two hashes"""
        if len(hash1) != len(hash2):
            return float('inf')
        
        return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
    
    def create_collection(self, name: str, description: str = "", image_ids: List[str] = None) -> int:
        """Create a new image collection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO collections (name, description, image_ids)
            VALUES (?, ?, ?)
        """, (name, description, json.dumps(image_ids or [])))
        
        collection_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return collection_id
    
    def get_collections(self) -> List[Dict[str, Any]]:
        """Get all collections"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections ORDER BY created_at DESC")
        results = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        collections = []
        
        for row in results:
            collection_dict = dict(zip(columns, row))
            collection_dict['image_ids'] = json.loads(collection_dict['image_ids'] or '[]')
            collections.append(collection_dict)
        
        conn.close()
        return collections
    
    def get_library_stats(self) -> Dict[str, Any]:
        """Get library statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total images
        cursor.execute("SELECT COUNT(*) FROM images")
        total_images = cursor.fetchone()[0]
        
        # Total size
        cursor.execute("SELECT SUM(file_size) FROM images")
        total_size = cursor.fetchone()[0] or 0
        
        # Images by category
        cursor.execute("SELECT category, COUNT(*) FROM images GROUP BY category")
        by_category = dict(cursor.fetchall())
        
        # Most used images
        cursor.execute("SELECT filename, usage_count FROM images ORDER BY usage_count DESC LIMIT 5")
        most_used = cursor.fetchall()
        
        # Recent additions
        cursor.execute("SELECT filename, created_at FROM images ORDER BY created_at DESC LIMIT 5")
        recent = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_images': total_images,
            'total_size': total_size,
            'by_category': by_category,
            'most_used': most_used,
            'recent': recent
        }


class ImageLibraryUI:
    """UI components for the image library"""
    
    def __init__(self, library: ImageLibrary):
        self.library = library
    
    def render_library_panel(self) -> str:
        """Render the complete library panel HTML"""
        return f"""
        <div class="library-panel-enhanced">
            {self._render_search_section()}
            {self._render_filter_section()}
            {self._render_upload_section()}
            {self._render_image_grid()}
            {self._render_collections_section()}
        </div>
        
        <style>
        .library-panel-enhanced {{
            height: 100%;
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 12px;
        }}
        
        .library-search-section {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .library-search-advanced {{
            display: none;
            background: var(--bg-tertiary);
            border-radius: 4px;
            padding: 8px;
            margin-top: 4px;
        }}
        
        .library-search-advanced.show {{
            display: block;
        }}
        
        .search-row {{
            display: flex;
            gap: 8px;
            align-items: center;
            margin-bottom: 6px;
        }}
        
        .search-row label {{
            min-width: 60px;
            font-size: 10px;
            color: var(--text-secondary);
        }}
        
        .search-row input, .search-row select {{
            flex: 1;
            background: var(--bg-primary);
            border: 1px solid var(--border-primary);
            border-radius: 3px;
            padding: 4px 6px;
            color: var(--text-primary);
            font-size: 10px;
        }}
        
        .library-filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }}
        
        .filter-chip {{
            padding: 4px 8px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            font-size: 9px;
            cursor: pointer;
            transition: var(--transition-fast);
        }}
        
        .filter-chip:hover {{
            background: var(--bg-hover);
        }}
        
        .filter-chip.active {{
            background: var(--bg-active);
            border-color: var(--border-active);
            color: var(--text-primary);
        }}
        
        .library-upload-zone {{
            border: 2px dashed var(--border-primary);
            border-radius: 4px;
            padding: 16px;
            text-align: center;
            cursor: pointer;
            transition: var(--transition-fast);
        }}
        
        .library-upload-zone:hover {{
            border-color: var(--border-active);
            background: var(--bg-hover);
        }}
        
        .library-upload-zone.dragover {{
            border-color: var(--bg-active);
            background: var(--bg-active);
            opacity: 0.8;
        }}
        
        .library-grid-container {{
            flex: 1;
            overflow-y: auto;
        }}
        
        .library-grid-enhanced {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 6px;
        }}
        
        .library-item-enhanced {{
            position: relative;
            aspect-ratio: 1;
            border-radius: 4px;
            overflow: hidden;
            cursor: pointer;
            transition: var(--transition-fast);
            border: 2px solid transparent;
        }}
        
        .library-item-enhanced:hover {{
            transform: scale(1.05);
            border-color: var(--border-secondary);
            z-index: 10;
        }}
        
        .library-item-enhanced.selected {{
            border-color: var(--bg-active);
        }}
        
        .library-item-enhanced img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .library-item-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(to bottom, transparent 60%, rgba(0,0,0,0.8) 100%);
            opacity: 0;
            transition: var(--transition-fast);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 4px;
        }}
        
        .library-item-enhanced:hover .library-item-overlay {{
            opacity: 1;
        }}
        
        .library-item-info {{
            color: white;
            font-size: 8px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        }}
        
        .library-item-actions {{
            position: absolute;
            top: 4px;
            right: 4px;
            display: flex;
            gap: 2px;
            opacity: 0;
            transition: var(--transition-fast);
        }}
        
        .library-item-enhanced:hover .library-item-actions {{
            opacity: 1;
        }}
        
        .library-action-btn {{
            width: 16px;
            height: 16px;
            background: rgba(0,0,0,0.7);
            border: none;
            border-radius: 2px;
            color: white;
            font-size: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .library-action-btn:hover {{
            background: var(--bg-active);
        }}
        
        .collections-section {{
            border-top: 1px solid var(--border-primary);
            padding-top: 8px;
        }}
        
        .collection-item {{
            display: flex;
            align-items: center;
            padding: 4px 8px;
            margin: 2px 0;
            background: var(--bg-tertiary);
            border-radius: 3px;
            cursor: pointer;
            font-size: 10px;
        }}
        
        .collection-item:hover {{
            background: var(--bg-hover);
        }}
        
        .collection-item.active {{
            background: var(--bg-active);
        }}
        </style>
        
        <script>
        // Library JavaScript functionality
        let currentLibraryFilter = 'all';
        let selectedImages = new Set();
        let librarySearchTimeout;
        
        function initializeLibrary() {{
            // Set up drag and drop
            const uploadZone = document.getElementById('library-upload-zone');
            if (uploadZone) {{
                uploadZone.addEventListener('dragover', handleDragOver);
                uploadZone.addEventListener('dragleave', handleDragLeave);
                uploadZone.addEventListener('drop', handleDrop);
            }}
            
            // Load initial images
            loadLibraryImages();
        }}
        
        function handleDragOver(e) {{
            e.preventDefault();
            e.currentTarget.classList.add('dragover');
        }}
        
        function handleDragLeave(e) {{
            e.currentTarget.classList.remove('dragover');
        }}
        
        function handleDrop(e) {{
            e.preventDefault();
            e.currentTarget.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files);
            uploadMultipleImages(files);
        }}
        
        function uploadMultipleImages(files) {{
            files.forEach(file => {{
                if (file.type.startsWith('image/')) {{
                    uploadImageToLibrary(file);
                }}
            }});
        }}
        
        function uploadImageToLibrary(file) {{
            const reader = new FileReader();
            reader.onload = function(e) {{
                // Send to Python backend for processing
                const imageData = e.target.result;
                addImageToLibrary(imageData, file.name, currentLibraryFilter);
            }};
            reader.readAsDataURL(file);
        }}
        
        function addImageToLibrary(imageData, filename, category) {{
            // This would communicate with the Python backend
            console.log('Adding image to library:', filename, category);
            
            // For now, add to UI immediately
            const grid = document.getElementById('library-grid');
            const item = createLibraryItem(imageData, filename, 'temp_' + Date.now());
            grid.appendChild(item);
        }}
        
        function createLibraryItem(imageData, filename, imageId) {{
            const item = document.createElement('div');
            item.className = 'library-item-enhanced';
            item.dataset.imageId = imageId;
            
            item.innerHTML = `
                <img src="${{imageData}}" alt="${{filename}}" loading="lazy">
                <div class="library-item-overlay">
                    <div class="library-item-info">${{filename}}</div>
                </div>
                <div class="library-item-actions">
                    <button class="library-action-btn" onclick="toggleImageFavorite('${{imageId}}')" title="Favorite">⭐</button>
                    <button class="library-action-btn" onclick="deleteLibraryImage('${{imageId}}')" title="Delete">🗑</button>
                </div>
            `;
            
            item.onclick = () => selectLibraryImage(imageId);
            item.ondblclick = () => addImageToCanvas(imageData);
            
            return item;
        }}
        
        function selectLibraryImage(imageId) {{
            const item = document.querySelector(`[data-image-id="${{imageId}}"]`);
            if (!item) return;
            
            if (selectedImages.has(imageId)) {{
                selectedImages.delete(imageId);
                item.classList.remove('selected');
            }} else {{
                selectedImages.add(imageId);
                item.classList.add('selected');
            }}
            
            updateSelectionInfo();
        }}
        
        function updateSelectionInfo() {{
            const count = selectedImages.size;
            const info = document.getElementById('selection-info');
            if (info) {{
                info.textContent = count > 0 ? `${{count}} selected` : 'No selection';
            }}
        }}
        
        function filterLibraryImages(category) {{
            currentLibraryFilter = category;
            
            // Update filter UI
            document.querySelectorAll('.filter-chip').forEach(chip => {{
                chip.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Filter images
            const items = document.querySelectorAll('.library-item-enhanced');
            items.forEach(item => {{
                const itemCategory = item.dataset.category || 'uploads';
                if (category === 'all' || itemCategory === category) {{
                    item.style.display = 'block';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }}
        
        function searchLibraryImages() {{
            clearTimeout(librarySearchTimeout);
            librarySearchTimeout = setTimeout(() => {{
                const query = document.getElementById('library-search').value.toLowerCase();
                const items = document.querySelectorAll('.library-item-enhanced');
                
                items.forEach(item => {{
                    const filename = item.querySelector('img').alt.toLowerCase();
                    const visible = !query || filename.includes(query);
                    item.style.display = visible ? 'block' : 'none';
                }});
            }}, 300);
        }}
        
        function toggleAdvancedSearch() {{
            const advanced = document.getElementById('library-search-advanced');
            advanced.classList.toggle('show');
        }}
        
        function applyAdvancedSearch() {{
            const filters = {{
                minWidth: document.getElementById('min-width').value,
                maxWidth: document.getElementById('max-width').value,
                minHeight: document.getElementById('min-height').value,
                maxHeight: document.getElementById('max-height').value,
                hasTransparency: document.getElementById('has-transparency').checked,
                format: document.getElementById('format-filter').value
            }};
            
            console.log('Applying advanced search:', filters);
            // Implementation would filter based on these criteria
        }}
        
        function toggleImageFavorite(imageId) {{
            console.log('Toggle favorite:', imageId);
            // This would communicate with Python backend
        }}
        
        function deleteLibraryImage(imageId) {{
            if (confirm('Delete this image from library?')) {{
                const item = document.querySelector(`[data-image-id="${{imageId}}"]`);
                if (item) {{
                    item.remove();
                    selectedImages.delete(imageId);
                    updateSelectionInfo();
                }}
                console.log('Delete image:', imageId);
            }}
        }}
        
        function addImageToCanvas(imageData) {{
            // Add image to the main canvas
            fabric.Image.fromURL(imageData, function(img) {{
                img.scale(0.5);
                img.set({{
                    left: 100,
                    top: 100
                }});
                canvas.add(img);
                canvas.setActiveObject(img);
                saveToHistory();
            }});
        }}
        
        function loadLibraryImages() {{
            // This would load images from the Python backend
            console.log('Loading library images...');
        }}
        
        function createNewCollection() {{
            const name = prompt('Collection name:');
            if (name) {{
                const selectedIds = Array.from(selectedImages);
                console.log('Creating collection:', name, selectedIds);
                // This would communicate with Python backend
            }}
        }}
        
        // Initialize library when DOM is ready
        document.addEventListener('DOMContentLoaded', initializeLibrary);
        </script>
        """
    
    def _render_search_section(self) -> str:
        """Render the search section"""
        return """
        <div class="library-search-section">
            <input type="text" 
                   id="library-search" 
                   class="library-search" 
                   placeholder="Search images..." 
                   oninput="searchLibraryImages()">
            
            <button class="tool-button" onclick="toggleAdvancedSearch()" title="Advanced Search">🔍+</button>
            
            <div id="library-search-advanced" class="library-search-advanced">
                <div class="search-row">
                    <label>Width:</label>
                    <input type="number" id="min-width" placeholder="Min" style="width: 60px;">
                    <span>-</span>
                    <input type="number" id="max-width" placeholder="Max" style="width: 60px;">
                </div>
                <div class="search-row">
                    <label>Height:</label>
                    <input type="number" id="min-height" placeholder="Min" style="width: 60px;">
                    <span>-</span>
                    <input type="number" id="max-height" placeholder="Max" style="width: 60px;">
                </div>
                <div class="search-row">
                    <label>Format:</label>
                    <select id="format-filter">
                        <option value="">Any</option>
                        <option value="PNG">PNG</option>
                        <option value="JPEG">JPEG</option>
                        <option value="SVG">SVG</option>
                        <option value="GIF">GIF</option>
                    </select>
                </div>
                <div class="search-row">
                    <label>
                        <input type="checkbox" id="has-transparency"> Transparent
                    </label>
                    <label>
                        <input type="checkbox" id="favorites-only"> Favorites only
                    </label>
                </div>
                <button class="tool-button large" onclick="applyAdvancedSearch()">Apply Filters</button>
            </div>
        </div>
        """
    
    def _render_filter_section(self) -> str:
        """Render the category filter section"""
        return """
        <div class="library-filters">
            <div class="filter-chip active" onclick="filterLibraryImages('all')">All</div>
            <div class="filter-chip" onclick="filterLibraryImages('business')">Business</div>
            <div class="filter-chip" onclick="filterLibraryImages('icons')">Icons</div>
            <div class="filter-chip" onclick="filterLibraryImages('backgrounds')">Backgrounds</div>
            <div class="filter-chip" onclick="filterLibraryImages('logos')">Logos</div>
            <div class="filter-chip" onclick="filterLibraryImages('people')">People</div>
            <div class="filter-chip" onclick="filterLibraryImages('objects')">Objects</div>
            <div class="filter-chip" onclick="filterLibraryImages('nature')">Nature</div>
            <div class="filter-chip" onclick="filterLibraryImages('abstract')">Abstract</div>
            <div class="filter-chip" onclick="filterLibraryImages('uploads')">Uploads</div>
        </div>
        """
    
    def _render_upload_section(self) -> str:
        """Render the upload section"""
        return """
        <div class="library-upload-zone" id="library-upload-zone" onclick="document.getElementById('library-file-input').click()">
            <div>📁 Drop images here or click to upload</div>
            <div class="text-small text-muted">Supports: PNG, JPG, SVG, GIF</div>
            <input type="file" id="library-file-input" multiple accept="image/*" style="display: none;" onchange="uploadMultipleImages(Array.from(this.files))">
        </div>
        """
    
    def _render_image_grid(self) -> str:
        """Render the image grid"""
        return """
        <div class="library-grid-container">
            <div class="library-grid-enhanced" id="library-grid">
                <!-- Images will be populated here -->
            </div>
        </div>
        """
    
    def _render_collections_section(self) -> str:
        """Render the collections section"""
        return """
        <div class="collections-section">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="text-small">Collections</span>
                <button class="tool-button" onclick="createNewCollection()" title="New Collection">➕</button>
            </div>
            <div id="collections-list">
                <div class="collection-item active" onclick="filterLibraryImages('all')">
                    📁 All Images
                </div>
                <div class="collection-item" onclick="filterLibraryImages('favorites')">
                    ⭐ Favorites
                </div>
                <div class="collection-item" onclick="filterLibraryImages('recent')">
                    🕒 Recent
                </div>
            </div>
        </div>
        """


# Import required modules for image processing
import io
try:
    from PIL import Image, ImageFilter, ImageEnhance, ImageOps
except ImportError:
    st.error("PIL (Pillow) is required for image processing. Please install it with: pip install Pillow")
    st.stop()

# Initialize the image library
@st.cache_resource
def get_image_library():
    """Get or create the image library instance"""
    return ImageLibrary()

# Example usage and integration functions
def integrate_with_streamlit():
    """Integration functions for Streamlit app"""
    
    library = get_image_library()
    
    # File uploader for adding images
    uploaded_files = st.file_uploader(
        "Upload images to library",
        type=['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.read()
            
            # Add to library
            image_id = library.add_image(
                file_bytes, 
                uploaded_file.name,
                category="uploads",
                tags=["uploaded", "user-content"],
                description=f"Uploaded image: {uploaded_file.name}"
            )
            
            if image_id:
                st.success(f"Added {uploaded_file.name} to library")
            else:
                st.error(f"Failed to add {uploaded_file.name}")
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search images", placeholder="Enter keywords...")
    with col2:
        category_filter = st.selectbox("Category", ["All"] + list(library.categories.keys()))
    
    # Display search results
    if search_query or category_filter != "All":
        category = category_filter.lower() if category_filter != "All" else None
        results = library.search_images(
            query=search_query,
            category=category,
            limit=20
        )
        
        if results:
            # Display in grid
            cols = st.columns(4)
            for i, image in enumerate(results):
                with cols[i % 4]:
                    # Display thumbnail
                    thumbnail_data = library.get_thumbnail_data(image['id'])
                    if thumbnail_data:
                        st.image(thumbnail_data, caption=image['filename'], use_column_width=True)
                        
                        # Action buttons
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("Use", key=f"use_{image['id']}"):
                                # Add to canvas (would integrate with main app)
                                st.success(f"Added {image['filename']} to canvas")
                        with col_b:
                            if st.button("❤️", key=f"fav_{image['id']}"):
                                library.toggle_favorite(image['id'])
                                st.rerun()
        else:
            st.info("No images found matching your criteria.")
    
    # Library statistics
    with st.expander("Library Statistics"):
        stats = library.get_library_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Images", stats['total_images'])
        with col2:
            st.metric("Total Size", f"{stats['total_size'] / (1024*1024):.1f} MB")
        with col3:
            st.metric("Categories", len(stats['by_category']))
        
        # Category breakdown
        if stats['by_category']:
            st.subheader("By Category")
            for category, count in stats['by_category'].items():
                st.write(f"**{library.categories.get(category, category)}**: {count} images")


"""
Canvas Sizes and Templates System
Comprehensive collection of canvas sizes for various design purposes
"""

from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum

@dataclass
class CanvasSize:
    """Canvas size definition with metadata"""
    name: str
    width: int
    height: int
    category: str
    description: str
    dpi: int = 300
    units: str = "px"
    orientation: str = "landscape"  # landscape, portrait, square
    common_use: str = ""
    bleed: Optional[Tuple[int, int]] = None  # (width_bleed, height_bleed) in pixels
    safe_area: Optional[Tuple[int, int, int, int]] = None  # (left, top, right, bottom) margins
    
    def __post_init__(self):
        """Calculate orientation and derived properties"""
        if self.width == self.height:
            self.orientation = "square"
        elif self.width > self.height:
            self.orientation = "landscape"
        else:
            self.orientation = "portrait"
    
    @property
    def aspect_ratio(self) -> float:
        """Calculate aspect ratio"""
        return self.width / self.height
    
    @property
    def size_tuple(self) -> Tuple[int, int]:
        """Return size as tuple"""
        return (self.width, self.height)
    
    @property
    def area(self) -> int:
        """Calculate total area in pixels"""
        return self.width * self.height
    
    def to_inches(self) -> Tuple[float, float]:
        """Convert to inches at current DPI"""
        return (self.width / self.dpi, self.height / self.dpi)
    
    def to_mm(self) -> Tuple[float, float]:
        """Convert to millimeters at current DPI"""
        inches = self.to_inches()
        return (inches[0] * 25.4, inches[1] * 25.4)
    
    def with_bleed(self) -> Tuple[int, int]:
        """Return size including bleed area"""
        if self.bleed:
            return (self.width + self.bleed[0] * 2, self.height + self.bleed[1] * 2)
        return self.size_tuple


class CanvasCategory(Enum):
    """Canvas size categories"""
    BUSINESS_CARDS = "business_cards"
    SOCIAL_MEDIA = "social_media"
    PRINT_MATERIALS = "print_materials"
    WEB_GRAPHICS = "web_graphics"
    PRESENTATIONS = "presentations"
    MOBILE_APPS = "mobile_apps"
    ADVERTISING = "advertising"
    PHOTOGRAPHY = "photography"
    DOCUMENTS = "documents"
    CUSTOM = "custom"


class CanvasSizeManager:
    """Manages all available canvas sizes and templates"""
    
    def __init__(self):
        self.sizes = self._initialize_sizes()
        self.templates = self._initialize_templates()
    
    def _initialize_sizes(self) -> Dict[str, CanvasSize]:
        """Initialize comprehensive collection of canvas sizes"""
        
        sizes = {}
        
        # Business Cards (International Standards)
        business_cards = [
            # Standard sizes
            CanvasSize("US Business Card", 1050, 600, "business_cards", 
                      "Standard US business card (3.5\" × 2\")", 300, "px", 
                      common_use="Professional business cards", 
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
            
            CanvasSize("EU Business Card", 1063, 638, "business_cards", 
                      "European standard (85mm × 55mm)", 300, "px",
                      common_use="European business cards",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
            
            CanvasSize("UK Business Card", 1063, 669, "business_cards", 
                      "UK standard (85mm × 55mm)", 300, "px",
                      common_use="UK business cards",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
            
            CanvasSize("Japan Business Card", 1093, 649, "business_cards", 
                      "Japanese standard (91mm × 55mm)", 300, "px",
                      common_use="Japanese business cards",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
            
            CanvasSize("Square Business Card", 1050, 1050, "business_cards", 
                      "Modern square format (3.5\" × 3.5\")", 300, "px",
                      common_use="Creative business cards",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
            
            CanvasSize("Mini Business Card", 787, 472, "business_cards", 
                      "Compact size (2.625\" × 1.575\")", 300, "px",
                      common_use="Compact business cards",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
            
            CanvasSize("Slim Business Card", 1312, 394, "business_cards", 
                      "Slim format (4.375\" × 1.3125\")", 300, "px",
                      common_use="Modern slim cards",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
        ]
        
        # Social Media Formats
        social_media = [
            # Instagram
            CanvasSize("Instagram Post", 1080, 1080, "social_media", 
                      "Instagram square post", 72, "px",
                      common_use="Instagram feed posts"),
            
            CanvasSize("Instagram Story", 1080, 1920, "social_media", 
                      "Instagram story format", 72, "px",
                      common_use="Instagram stories and reels"),
            
            CanvasSize("Instagram Reel Cover", 1080, 1920, "social_media", 
                      "Instagram reel cover", 72, "px",
                      common_use="Reel thumbnails"),
            
            # Facebook
            CanvasSize("Facebook Post", 1200, 630, "social_media", 
                      "Facebook feed post", 72, "px",
                      common_use="Facebook posts and shares"),
            
            CanvasSize("Facebook Cover", 1200, 315, "social_media", 
                      "Facebook page cover photo", 72, "px",
                      common_use="Facebook page headers"),
            
            CanvasSize("Facebook Story", 1080, 1920, "social_media", 
                      "Facebook story format", 72, "px",
                      common_use="Facebook stories"),
            
            # Twitter/X
            CanvasSize("Twitter Post", 1200, 675, "social_media", 
                      "Twitter/X post image", 72, "px",
                      common_use="Twitter posts and cards"),
            
            CanvasSize("Twitter Header", 1500, 500, "social_media", 
                      "Twitter/X profile header", 72, "px",
                      common_use="Twitter profile banners"),
            
            # LinkedIn
            CanvasSize("LinkedIn Post", 1200, 627, "social_media", 
                      "LinkedIn feed post", 72, "px",
                      common_use="LinkedIn posts and articles"),
            
            CanvasSize("LinkedIn Cover", 1584, 396, "social_media", 
                      "LinkedIn profile cover", 72, "px",
                      common_use="LinkedIn profile headers"),
            
            # YouTube
            CanvasSize("YouTube Thumbnail", 1280, 720, "social_media", 
                      "YouTube video thumbnail", 72, "px",
                      common_use="YouTube video previews"),
            
            CanvasSize("YouTube Banner", 2560, 1440, "social_media", 
                      "YouTube channel banner", 72, "px",
                      common_use="YouTube channel headers"),
            
            # TikTok
            CanvasSize("TikTok Video", 1080, 1920, "social_media", 
                      "TikTok video format", 72, "px",
                      common_use="TikTok videos and covers"),
            
            # Pinterest
            CanvasSize("Pinterest Pin", 1000, 1500, "social_media", 
                      "Pinterest pin format", 72, "px",
                      common_use="Pinterest pins and boards"),
        ]
        
        # Print Materials
        print_materials = [
            # Flyers and Posters
            CanvasSize("A4 Flyer", 2480, 3508, "print_materials", 
                      "A4 size flyer (210mm × 297mm)", 300, "px",
                      common_use="Flyers, documents, letters",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            CanvasSize("US Letter Flyer", 2550, 3300, "print_materials", 
                      "US Letter size (8.5\" × 11\")", 300, "px",
                      common_use="US standard documents",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            CanvasSize("A3 Poster", 3508, 4961, "print_materials", 
                      "A3 poster (297mm × 420mm)", 300, "px",
                      common_use="Small posters, presentations",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            CanvasSize("A2 Poster", 4961, 7016, "print_materials", 
                      "A2 poster (420mm × 594mm)", 300, "px",
                      common_use="Medium posters, displays",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            CanvasSize("A1 Poster", 7016, 9933, "print_materials", 
                      "A1 poster (594mm × 841mm)", 300, "px",
                      common_use="Large posters, banners",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            # Postcards
            CanvasSize("Standard Postcard", 1800, 1200, "print_materials", 
                      "Standard postcard (6\" × 4\")", 300, "px",
                      common_use="Postcards, mailers",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
            
            CanvasSize("Large Postcard", 2100, 1500, "print_materials", 
                      "Large postcard (7\" × 5\")", 300, "px",
                      common_use="Premium postcards",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
            
            # Brochures
            CanvasSize("Tri-fold Brochure", 3600, 2400, "print_materials", 
                      "Tri-fold brochure (12\" × 8\")", 300, "px",
                      common_use="Marketing brochures",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            CanvasSize("Bi-fold Brochure", 2400, 3600, "print_materials", 
                      "Bi-fold brochure (8\" × 12\")", 300, "px",
                      common_use="Simple brochures",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
        ]
        
        # Web Graphics
        web_graphics = [
            # Website Headers
            CanvasSize("Website Header", 1920, 400, "web_graphics", 
                      "Website header banner", 72, "px",
                      common_use="Website headers, hero sections"),
            
            CanvasSize("Blog Header", 1200, 600, "web_graphics", 
                      "Blog post header image", 72, "px",
                      common_use="Blog featured images"),
            
            CanvasSize("Email Header", 600, 200, "web_graphics", 
                      "Email newsletter header", 72, "px",
                      common_use="Email marketing headers"),
            
            # Web Banners
            CanvasSize("Leaderboard Banner", 728, 90, "web_graphics", 
                      "Standard web banner", 72, "px",
                      common_use="Website advertising banners"),
            
            CanvasSize("Rectangle Banner", 300, 250, "web_graphics", 
                      "Medium rectangle banner", 72, "px",
                      common_use="Sidebar advertisements"),
            
            CanvasSize("Skyscraper Banner", 160, 600, "web_graphics", 
                      "Vertical banner format", 72, "px",
                      common_use="Sidebar vertical ads"),
            
            # Icons and Buttons
            CanvasSize("App Icon", 512, 512, "web_graphics", 
                      "Application icon", 72, "px",
                      common_use="App icons, favicons"),
            
            CanvasSize("Button Large", 300, 100, "web_graphics", 
                      "Large web button", 72, "px",
                      common_use="Call-to-action buttons"),
            
            CanvasSize("Button Medium", 200, 60, "web_graphics", 
                      "Medium web button", 72, "px",
                      common_use="Standard buttons"),
        ]
        
        # Presentation Formats
        presentations = [
            CanvasSize("PowerPoint 16:9", 1920, 1080, "presentations", 
                      "Standard PowerPoint slide", 72, "px",
                      common_use="Modern presentations"),
            
            CanvasSize("PowerPoint 4:3", 1024, 768, "presentations", 
                      "Classic PowerPoint slide", 72, "px",
                      common_use="Traditional presentations"),
            
            CanvasSize("Keynote", 1920, 1080, "presentations", 
                      "Apple Keynote slide", 72, "px",
                      common_use="Mac presentations"),
            
            CanvasSize("Google Slides", 1920, 1080, "presentations", 
                      "Google Slides format", 72, "px",
                      common_use="Online presentations"),
        ]
        
        # Mobile App Formats
        mobile_apps = [
            # iOS
            CanvasSize("iPhone Screen", 828, 1792, "mobile_apps", 
                      "iPhone screen (iPhone 11)", 72, "px",
                      common_use="iOS app screenshots"),
            
            CanvasSize("iPhone Pro Screen", 1170, 2532, "mobile_apps", 
                      "iPhone Pro screen", 72, "px",
                      common_use="iOS Pro app screenshots"),
            
            CanvasSize("iPad Screen", 1620, 2160, "mobile_apps", 
                      "iPad screen", 72, "px",
                      common_use="iPad app screenshots"),
            
            # Android
            CanvasSize("Android Phone", 1080, 1920, "mobile_apps", 
                      "Standard Android phone", 72, "px",
                      common_use="Android app screenshots"),
            
            CanvasSize("Android Tablet", 1600, 2560, "mobile_apps", 
                      "Android tablet screen", 72, "px",
                      common_use="Android tablet apps"),
        ]
        
        # Advertising Formats
        advertising = [
            CanvasSize("Billboard", 14400, 4800, "advertising", 
                      "Standard billboard (48' × 14')", 150, "px",
                      common_use="Outdoor advertising",
                      bleed=(18, 18), safe_area=(72, 72, 72, 72)),
            
            CanvasSize("Bus Shelter", 1800, 1200, "advertising", 
                      "Bus shelter ad", 150, "px",
                      common_use="Transit advertising",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            CanvasSize("Magazine Ad Full", 2550, 3300, "advertising", 
                      "Full page magazine ad", 300, "px",
                      common_use="Magazine advertisements",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            CanvasSize("Magazine Ad Half", 2550, 1650, "advertising", 
                      "Half page magazine ad", 300, "px",
                      common_use="Magazine half-page ads",
                      bleed=(9, 9), safe_area=(36, 36, 36, 36)),
            
            CanvasSize("Newspaper Ad", 1800, 1200, "advertising", 
                      "Newspaper advertisement", 300, "px",
                      common_use="Newspaper ads",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
        ]
        
        # Photography Formats
        photography = [
            CanvasSize("Photo 4x6", 1800, 1200, "photography", 
                      "Standard photo print (4\" × 6\")", 300, "px",
                      common_use="Photo prints"),
            
            CanvasSize("Photo 5x7", 2100, 1500, "photography", 
                      "Medium photo print (5\" × 7\")", 300, "px",
                      common_use="Photo prints"),
            
            CanvasSize("Photo 8x10", 3000, 2400, "photography", 
                      "Large photo print (8\" × 10\")", 300, "px",
                      common_use="Photo prints"),
            
            CanvasSize("Photo 11x14", 4200, 3300, "photography", 
                      "Extra large photo (11\" × 14\")", 300, "px",
                      common_use="Large photo prints"),
            
            CanvasSize("Square Photo", 1800, 1800, "photography", 
                      "Square photo format", 300, "px",
                      common_use="Instagram-style photos"),
        ]
        
        # Document Formats
        documents = [
            CanvasSize("Resume", 2550, 3300, "documents", 
                      "Standard resume (8.5\" × 11\")", 300, "px",
                      common_use="Resumes, CVs"),
            
            CanvasSize("Invoice", 2550, 3300, "documents", 
                      "Business invoice", 300, "px",
                      common_use="Invoices, receipts"),
            
            CanvasSize("Certificate", 3300, 2550, "documents", 
                      "Certificate format", 300, "px",
                      common_use="Certificates, awards"),
            
            CanvasSize("ID Card", 1012, 638, "documents", 
                      "ID card format", 300, "px",
                      common_use="ID cards, badges",
                      bleed=(9, 9), safe_area=(18, 18, 18, 18)),
        ]
        
        # Combine all sizes
        all_sizes = (business_cards + social_media + print_materials + 
                    web_graphics + presentations + mobile_apps + 
                    advertising + photography + documents)
        
        # Convert to dictionary with unique keys
        for size in all_sizes:
            key = size.name.lower().replace(" ", "_").replace("-", "_")
            sizes[key] = size
        
        return sizes
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize design templates for different canvas sizes"""
        
        templates = {
            "business_card_classic": {
                "name": "Classic Business Card",
                "description": "Traditional business card layout",
                "canvas_size": "us_business_card",
                "elements": [
                    {
                        "type": "rectangle",
                        "x": 0, "y": 0, "width": 1050, "height": 600,
                        "fill": "#ffffff", "stroke": "#cccccc", "strokeWidth": 2
                    },
                    {
                        "type": "text",
                        "x": 50, "y": 100, "text": "Your Name",
                        "fontSize": 24, "fontFamily": "Arial", "fill": "#333333"
                    },
                    {
                        "type": "text",
                        "x": 50, "y": 140, "text": "Job Title",
                        "fontSize": 16, "fontFamily": "Arial", "fill": "#666666"
                    },
                    {
                        "type": "text",
                        "x": 50, "y": 200, "text": "Company Name",
                        "fontSize": 18, "fontFamily": "Arial", "fill": "#333333"
                    },
                    {
                        "type": "text",
                        "x": 50, "y": 450, "text": "email@company.com",
                        "fontSize": 14, "fontFamily": "Arial", "fill": "#666666"
                    },
                    {
                        "type": "text",
                        "x": 50, "y": 480, "text": "+1 (555) 123-4567",
                        "fontSize": 14, "fontFamily": "Arial", "fill": "#666666"
                    },
                    {
                        "type": "text",
                        "x": 50, "y": 510, "text": "www.company.com",
                        "fontSize": 14, "fontFamily": "Arial", "fill": "#666666"
                    }
                ]
            },
            
            "business_card_modern": {
                "name": "Modern Business Card",
                "description": "Contemporary business card design",
                "canvas_size": "us_business_card",
                "elements": [
                    {
                        "type": "rectangle",
                        "x": 0, "y": 0, "width": 1050, "height": 600,
                        "fill": "#2c3e50", "stroke": "none"
                    },
                    {
                        "type": "rectangle",
                        "x": 0, "y": 0, "width": 300, "height": 600,
                        "fill": "#3498db", "stroke": "none"
                    },
                    {
                        "type": "text",
                        "x": 350, "y": 100, "text": "YOUR NAME",
                        "fontSize": 28, "fontFamily": "Arial", "fill": "#ffffff", "fontWeight": "bold"
                    },
                    {
                        "type": "text",
                        "x": 350, "y": 140, "text": "Professional Title",
                        "fontSize": 16, "fontFamily": "Arial", "fill": "#ecf0f1"
                    },
                    {
                        "type": "text",
                        "x": 350, "y": 400, "text": "email@company.com",
                        "fontSize": 14, "fontFamily": "Arial", "fill": "#ecf0f1"
                    },
                    {
                        "type": "text",
                        "x": 350, "y": 430, "text": "+1 (555) 123-4567",
                        "fontSize": 14, "fontFamily": "Arial", "fill": "#ecf0f1"
                    },
                    {
                        "type": "text",
                        "x": 350, "y": 460, "text": "www.company.com",
                        "fontSize": 14, "fontFamily": "Arial", "fill": "#ecf0f1"
                    }
                ]
            },
            
            "instagram_post_template": {
                "name": "Instagram Post Template",
                "description": "Clean Instagram post layout",
                "canvas_size": "instagram_post",
                "elements": [
                    {
                        "type": "rectangle",
                        "x": 0, "y": 0, "width": 1080, "height": 1080,
                        "fill": "#ffffff", "stroke": "none"
                    },
                    {
                        "type": "text",
                        "x": 540, "y": 400, "text": "Your Message Here",
                        "fontSize": 48, "fontFamily": "Arial", "fill": "#333333",
                        "textAlign": "center", "originX": "center"
                    },
                    {
                        "type": "text",
                        "x": 540, "y": 680, "text": "@yourusername",
                        "fontSize": 24, "fontFamily": "Arial", "fill": "#666666",
                        "textAlign": "center", "originX": "center"
                    }
                ]
            },
            
            "flyer_template": {
                "name": "Event Flyer Template",
                "description": "Professional event flyer layout",
                "canvas_size": "a4_flyer",
                "elements": [
                    {
                        "type": "rectangle",
                        "x": 0, "y": 0, "width": 2480, "height": 3508,
                        "fill": "#ffffff", "stroke": "none"
                    },
                    {
                        "type": "rectangle",
                        "x": 0, "y": 0, "width": 2480, "height": 800,
                        "fill": "#3498db", "stroke": "none"
                    },
                    {
                        "type": "text",
                        "x": 1240, "y": 300, "text": "EVENT TITLE",
                        "fontSize": 72, "fontFamily": "Arial", "fill": "#ffffff",
                        "textAlign": "center", "originX": "center", "fontWeight": "bold"
                    },
                    {
                        "type": "text",
                        "x": 1240, "y": 400, "text": "Subtitle or Date",
                        "fontSize": 36, "fontFamily": "Arial", "fill": "#ecf0f1",
                        "textAlign": "center", "originX": "center"
                    },
                    {
                        "type": "text",
                        "x": 200, "y": 1200, "text": "Event Description",
                        "fontSize": 24, "fontFamily": "Arial", "fill": "#333333"
                    }
                ]
            }
        }
        
        return templates
    
    def get_sizes_by_category(self, category: str) -> List[CanvasSize]:
        """Get all sizes in a specific category"""
        return [size for size in self.sizes.values() if size.category == category]
    
    def get_size(self, name: str) -> Optional[CanvasSize]:
        """Get a specific canvas size by name"""
        key = name.lower().replace(" ", "_").replace("-", "_")
        return self.sizes.get(key)
    
    def search_sizes(self, query: str) -> List[CanvasSize]:
        """Search for canvas sizes by name or description"""
        query = query.lower()
        results = []
        
        for size in self.sizes.values():
            if (query in size.name.lower() or 
                query in size.description.lower() or 
                query in size.common_use.lower()):
                results.append(size)
        
        return results
    
    def get_similar_sizes(self, reference_size: CanvasSize, tolerance: float = 0.1) -> List[CanvasSize]:
        """Find sizes with similar aspect ratios"""
        target_ratio = reference_size.aspect_ratio
        similar = []
        
        for size in self.sizes.values():
            if size.name != reference_size.name:
                ratio_diff = abs(size.aspect_ratio - target_ratio) / target_ratio
                if ratio_diff <= tolerance:
                    similar.append(size)
        
        return sorted(similar, key=lambda s: abs(s.aspect_ratio - target_ratio))
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        categories = set(size.category for size in self.sizes.values())
        return sorted(list(categories))
    
    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific template by name"""
        return self.templates.get(name)
    
    def get_templates_for_size(self, canvas_size_name: str) -> List[Dict[str, Any]]:
        """Get all templates for a specific canvas size"""
        size_key = canvas_size_name.lower().replace(" ", "_").replace("-", "_")
        return [template for template in self.templates.values() 
                if template.get("canvas_size") == size_key]
    
    def create_custom_size(self, name: str, width: int, height: int, 
                          description: str = "", dpi: int = 300) -> CanvasSize:
        """Create a custom canvas size"""
        custom_size = CanvasSize(
            name=name,
            width=width,
            height=height,
            category="custom",
            description=description or f"Custom size {width}×{height}",
            dpi=dpi,
            common_use="Custom design"
        )
        
        # Add to sizes collection
        key = name.lower().replace(" ", "_").replace("-", "_")
        self.sizes[key] = custom_size
        
        return custom_size


class CanvasSizeUI:
    """UI components for canvas size selection"""
    
    def __init__(self, size_manager: CanvasSizeManager):
        self.size_manager = size_manager
    
    def render_size_selector(self) -> str:
        """Render the canvas size selector UI"""
        
        categories = self.size_manager.get_categories()
        
        return f"""
        <div class="canvas-size-selector">
            <div class="size-selector-header">
                <h3>📐 Canvas Size</h3>
                <button class="tool-button" onclick="showCustomSizeDialog()" title="Custom Size">➕</button>
            </div>
            
            <div class="size-search">
                <input type="text" id="size-search" placeholder="Search sizes..." 
                       oninput="searchCanvasSizes(this.value)">
            </div>
            
            <div class="size-categories">
                <select id="size-category" onchange="filterSizesByCategory(this.value)">
                    <option value="">All Categories</option>
                    {self._render_category_options(categories)}
                </select>
            </div>
            
            <div class="size-grid" id="size-grid">
                {self._render_size_grid()}
            </div>
            
            <div class="size-info" id="size-info">
                <div class="info-row">
                    <span>Selected:</span>
                    <span id="selected-size-name">None</span>
                </div>
                <div class="info-row">
                    <span>Dimensions:</span>
                    <span id="selected-size-dims">-</span>
                </div>
                <div class="info-row">
                    <span>Aspect Ratio:</span>
                    <span id="selected-aspect-ratio">-</span>
                </div>
            </div>
            
            <div class="size-actions">
                <button class="tool-button large" onclick="applyCanvasSize()" id="apply-size-btn" disabled>
                    Apply Size
                </button>
                <button class="tool-button" onclick="showSizePreview()" id="preview-size-btn" disabled>
                    Preview
                </button>
            </div>
        </div>
        
        <!-- Custom Size Dialog -->
        <div id="custom-size-dialog" class="modal-dialog" style="display: none;">
            <div class="modal-content">
                <div class="modal-header">
                    <h4>Custom Canvas Size</h4>
                    <button class="close-btn" onclick="hideCustomSizeDialog()">×</button>
                </div>
                <div class="modal-body">
                    <div class="form-row">
                        <label>Name:</label>
                        <input type="text" id="custom-name" placeholder="My Custom Size">
                    </div>
                    <div class="form-row">
                        <label>Width:</label>
                        <input type="number" id="custom-width" placeholder="1920" min="1">
                        <span>px</span>
                    </div>
                    <div class="form-row">
                        <label>Height:</label>
                        <input type="number" id="custom-height" placeholder="1080" min="1">
                        <span>px</span>
                    </div>
                    <div class="form-row">
                        <label>DPI:</label>
                        <select id="custom-dpi">
                            <option value="72">72 (Web)</option>
                            <option value="150">150 (Draft Print)</option>
                            <option value="300" selected>300 (Print)</option>
                            <option value="600">600 (High Quality)</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Description:</label>
                        <textarea id="custom-description" placeholder="Optional description"></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="tool-button" onclick="hideCustomSizeDialog()">Cancel</button>
                    <button class="tool-button primary" onclick="createCustomSize()">Create</button>
                </div>
            </div>
        </div>
        
        <style>
        .canvas-size-selector {{
            padding: 12px;
            height: 100%;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .size-selector-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .size-selector-header h3 {{
            margin: 0;
            font-size: 14px;
            color: var(--text-primary);
        }}
        
        .size-search input, .size-categories select {{
            width: 100%;
            padding: 6px 8px;
            background: var(--bg-primary);
            border: 1px solid var(--border-primary);
            border-radius: 4px;
            color: var(--text-primary);
            font-size: 11px;
        }}
        
        .size-grid {{
            flex: 1;
            overflow-y: auto;
            display: grid;
            grid-template-columns: 1fr;
            gap: 4px;
            max-height: 400px;
        }}
        
        .size-item {{
            padding: 8px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 4px;
            cursor: pointer;
            transition: var(--transition-fast);
            font-size: 10px;
        }}
        
        .size-item:hover {{
            background: var(--bg-hover);
            border-color: var(--border-secondary);
        }}
        
        .size-item.selected {{
            background: var(--bg-active);
            border-color: var(--border-active);
            color: var(--text-primary);
        }}
        
        .size-item-name {{
            font-weight: 500;
            margin-bottom: 2px;
            color: var(--text-primary);
        }}
        
        .size-item-dims {{
            color: var(--text-secondary);
            font-size: 9px;
        }}
        
        .size-item-category {{
            color: var(--text-muted);
            font-size: 8px;
            text-transform: uppercase;
            margin-top: 2px;
        }}
        
        .size-info {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 4px;
            padding: 8px;
            font-size: 10px;
        }}
        
        .info-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }}
        
        .info-row:last-child {{
            margin-bottom: 0;
        }}
        
        .size-actions {{
            display: flex;
            gap: 8px;
        }}
        
        .tool-button.large {{
            flex: 1;
            padding: 8px 12px;
        }}
        
        .modal-dialog {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        }}
        
        .modal-content {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            width: 400px;
            max-width: 90vw;
            box-shadow: var(--shadow-panel);
        }}
        
        .modal-header {{
            padding: 16px;
            border-bottom: 1px solid var(--border-primary);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .modal-header h4 {{
            margin: 0;
            color: var(--text-primary);
        }}
        
        .close-btn {{
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: var(--text-secondary);
            padding: 0;
            width: 24px;
            height: 24px;
        }}
        
        .modal-body {{
            padding: 16px;
        }}
        
        .form-row {{
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .form-row label {{
            min-width: 80px;
            font-size: 11px;
            color: var(--text-primary);
        }}
        
        .form-row input, .form-row select, .form-row textarea {{
            flex: 1;
            padding: 6px 8px;
            background: var(--bg-primary);
            border: 1px solid var(--border-primary);
            border-radius: 4px;
            color: var(--text-primary);
            font-size: 11px;
        }}
        
        .form-row textarea {{
            resize: vertical;
            min-height: 60px;
        }}
        
        .modal-footer {{
            padding: 16px;
            border-top: 1px solid var(--border-primary);
            display: flex;
            justify-content: flex-end;
            gap: 8px;
        }}
        
        .tool-button.primary {{
            background: var(--bg-active);
            color: var(--text-primary);
        }}
        </style>
        
        <script>
        // Canvas Size Selector JavaScript
        let selectedCanvasSize = null;
        let allCanvasSizes = [];
        
        function initializeCanvasSizes() {{
            // This would be populated from Python backend
            loadCanvasSizes();
        }}
        
        function loadCanvasSizes() {{
            // Simulate loading canvas sizes
            console.log('Loading canvas sizes...');
            // In real implementation, this would fetch from Python backend
        }}
        
        function searchCanvasSizes(query) {{
            const items = document.querySelectorAll('.size-item');
            items.forEach(item => {{
                const name = item.querySelector('.size-item-name').textContent.toLowerCase();
                const visible = !query || name.includes(query.toLowerCase());
                item.style.display = visible ? 'block' : 'none';
            }});
        }}
        
        function filterSizesByCategory(category) {{
            const items = document.querySelectorAll('.size-item');
            items.forEach(item => {{
                const itemCategory = item.dataset.category;
                const visible = !category || itemCategory === category;
                item.style.display = visible ? 'block' : 'none';
            }});
        }}
        
        function selectCanvasSize(sizeData) {{
            selectedCanvasSize = sizeData;
            
            // Update UI
            document.querySelectorAll('.size-item').forEach(item => {{
                item.classList.remove('selected');
            }});
            event.currentTarget.classList.add('selected');
            
            // Update info panel
            document.getElementById('selected-size-name').textContent = sizeData.name;
            document.getElementById('selected-size-dims').textContent = 
                `${{sizeData.width}} × ${{sizeData.height}} px`;
            document.getElementById('selected-aspect-ratio').textContent = 
                (sizeData.width / sizeData.height).toFixed(2);
            
            // Enable buttons
            document.getElementById('apply-size-btn').disabled = false;
            document.getElementById('preview-size-btn').disabled = false;
        }}
        
        function applyCanvasSize() {{
            if (selectedCanvasSize) {{
                console.log('Applying canvas size:', selectedCanvasSize);
                
                // Resize canvas
                canvas.setDimensions({{
                    width: selectedCanvasSize.width,
                    height: selectedCanvasSize.height
                }});
                
                // Update canvas container
                updateCanvasContainer();
                
                // Save to history
                saveToHistory();
                
                // Show confirmation
                showNotification(`Canvas resized to ${{selectedCanvasSize.name}}`);
            }}
        }}
        
        function showSizePreview() {{
            if (selectedCanvasSize) {{
                console.log('Showing size preview:', selectedCanvasSize);
                // Implementation would show preview overlay
            }}
        }}
        
        function showCustomSizeDialog() {{
            document.getElementById('custom-size-dialog').style.display = 'flex';
        }}
        
        function hideCustomSizeDialog() {{
            document.getElementById('custom-size-dialog').style.display = 'none';
            // Clear form
            document.getElementById('custom-name').value = '';
            document.getElementById('custom-width').value = '';
            document.getElementById('custom-height').value = '';
            document.getElementById('custom-description').value = '';
        }}
        
        function createCustomSize() {{
            const name = document.getElementById('custom-name').value;
            const width = parseInt(document.getElementById('custom-width').value);
            const height = parseInt(document.getElementById('custom-height').value);
            const dpi = parseInt(document.getElementById('custom-dpi').value);
            const description = document.getElementById('custom-description').value;
            
            if (!name || !width || !height) {{
                alert('Please fill in all required fields');
                return;
            }}
            
            const customSize = {{
                name: name,
                width: width,
                height: height,
                dpi: dpi,
                description: description,
                category: 'custom'
            }};
            
            console.log('Creating custom size:', customSize);
            
            // Add to size grid
            addCustomSizeToGrid(customSize);
            
            // Hide dialog
            hideCustomSizeDialog();
            
            // Show confirmation
            showNotification(`Custom size "${{name}}" created`);
        }}
        
        function addCustomSizeToGrid(sizeData) {{
            const grid = document.getElementById('size-grid');
            const item = document.createElement('div');
            item.className = 'size-item';
            item.dataset.category = sizeData.category;
            item.onclick = () => selectCanvasSize(sizeData);
            
            item.innerHTML = `
                <div class="size-item-name">${{sizeData.name}}</div>
                <div class="size-item-dims">${{sizeData.width}} × ${{sizeData.height}} px</div>
                <div class="size-item-category">${{sizeData.category}}</div>
            `;
            
            grid.appendChild(item);
        }}
        
        function showNotification(message) {{
            // Simple notification system
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--bg-active);
                color: var(--text-primary);
                padding: 12px 16px;
                border-radius: 4px;
                z-index: 10001;
                font-size: 12px;
                box-shadow: var(--shadow-panel);
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {{
                notification.remove();
            }}, 3000);
        }}
        
        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', initializeCanvasSizes);
        </script>
        """
    
    def _render_category_options(self, categories: List[str]) -> str:
        """Render category options for select dropdown"""
        options = []
        for category in categories:
            display_name = category.replace("_", " ").title()
            options.append(f'<option value="{category}">{display_name}</option>')
        return "\n".join(options)
    
    def _render_size_grid(self) -> str:
        """Render the initial size grid"""
        # This would be populated dynamically via JavaScript
        # For now, return a placeholder
        return """
        <div class="size-item" data-category="business_cards" onclick="selectCanvasSize({name: 'US Business Card', width: 1050, height: 600, category: 'business_cards'})">
            <div class="size-item-name">US Business Card</div>
            <div class="size-item-dims">1050 × 600 px</div>
            <div class="size-item-category">business cards</div>
        </div>
        <div class="size-item" data-category="social_media" onclick="selectCanvasSize({name: 'Instagram Post', width: 1080, height: 1080, category: 'social_media'})">
            <div class="size-item-name">Instagram Post</div>
            <div class="size-item-dims">1080 × 1080 px</div>
            <div class="size-item-category">social media</div>
        </div>
        <div class="size-item" data-category="print_materials" onclick="selectCanvasSize({name: 'A4 Flyer', width: 2480, height: 3508, category: 'print_materials'})">
            <div class="size-item-name">A4 Flyer</div>
            <div class="size-item-dims">2480 × 3508 px</div>
            <div class="size-item-category">print materials</div>
        </div>
        """


# Example usage and integration
def demonstrate_canvas_sizes():
    """Demonstrate the canvas size system"""
    
    # Initialize the manager
    manager = CanvasSizeManager()
    
    # Get business card sizes
    business_cards = manager.get_sizes_by_category("business_cards")
    print(f"Found {len(business_cards)} business card sizes:")
    for card in business_cards[:3]:
        print(f"  - {card.name}: {card.width}×{card.height}px ({card.to_inches()[0]:.2f}\"×{card.to_inches()[1]:.2f}\")")
    
    # Search for Instagram sizes
    instagram_sizes = manager.search_sizes("instagram")
    print(f"\nFound {len(instagram_sizes)} Instagram-related sizes:")
    for size in instagram_sizes:
        print(f"  - {size.name}: {size.width}×{size.height}px")
    
    # Get similar aspect ratios to 16:9
    reference = manager.get_size("powerpoint_16_9")
    if reference:
        similar = manager.get_similar_sizes(reference)
        print(f"\nSizes similar to {reference.name} (16:9 aspect ratio):")
        for size in similar[:5]:
            print(f"  - {size.name}: {size.aspect_ratio:.2f}")
    
    # Create custom size
    custom = manager.create_custom_size("My Custom Size", 1200, 800, "Custom design size")
    print(f"\nCreated custom size: {custom.name} - {custom.width}×{custom.height}px")
    
    # Get template
    template = manager.get_template("business_card_modern")
    if template:
        print(f"\nTemplate: {template['name']}")
        print(f"Elements: {len(template['elements'])}")

if __name__ == "__main__":
    demonstrate_canvas_sizes()


"""
Magic Eraser and Advanced Image Editing Tools
AI-powered selection, background removal, and advanced editing capabilities
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import cv2
from typing import Tuple, List, Optional, Dict, Any, Union
from sklearn.cluster import KMeans
from scipy import ndimage
import io
import base64

class MagicEraser:
    """AI-powered magic eraser tool with intelligent selection"""
    
    def __init__(self):
        self.tolerance = 32
        self.contiguous = True
        self.sample_all_layers = False
        self.anti_alias = True
        self.feather_radius = 1
    
    def magic_select(self, 
                    image: Image.Image, 
                    point: Tuple[int, int],
                    tolerance: int = None,
                    contiguous: bool = None) -> Image.Image:
        """
        Magic selection tool - selects similar colors from a point
        Returns a mask image where white = selected, black = not selected
        """
        
        tolerance = tolerance or self.tolerance
        contiguous = contiguous if contiguous is not None else self.contiguous
        
        # Convert to numpy array
        img_array = np.array(image.convert('RGB'))
        height, width = img_array.shape[:2]
        
        # Get the target color at the clicked point
        if point[0] >= width or point[1] >= height or point[0] < 0 or point[1] < 0:
            return Image.new('L', image.size, 0)
        
        target_color = img_array[point[1], point[0]]
        
        # Create mask
        mask = np.zeros((height, width), dtype=np.uint8)
        
        if contiguous:
            # Flood fill algorithm for contiguous selection
            mask = self._flood_fill_select(img_array, point, target_color, tolerance)
        else:
            # Select all similar colors in the image
            mask = self._global_color_select(img_array, target_color, tolerance)
        
        # Apply anti-aliasing if enabled
        if self.anti_alias:
            mask = self._apply_anti_aliasing(mask)
        
        # Apply feathering if enabled
        if self.feather_radius > 0:
            mask = self._apply_feathering(mask, self.feather_radius)
        
        return Image.fromarray(mask, 'L')
    
    def _flood_fill_select(self, 
                          img_array: np.ndarray, 
                          start_point: Tuple[int, int], 
                          target_color: np.ndarray, 
                          tolerance: int) -> np.ndarray:
        """Flood fill algorithm for contiguous color selection"""
        
        height, width = img_array.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        visited = np.zeros((height, width), dtype=bool)
        
        # Stack for flood fill
        stack = [start_point]
        
        while stack:
            x, y = stack.pop()
            
            if x < 0 or x >= width or y < 0 or y >= height or visited[y, x]:
                continue
            
            current_color = img_array[y, x]
            color_distance = np.sqrt(np.sum((current_color - target_color) ** 2))
            
            if color_distance <= tolerance:
                visited[y, x] = True
                mask[y, x] = 255
                
                # Add neighboring pixels to stack
                stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
        
        return mask
    
    def _global_color_select(self, 
                           img_array: np.ndarray, 
                           target_color: np.ndarray, 
                           tolerance: int) -> np.ndarray:
        """Select all pixels with similar color globally"""
        
        # Calculate color distance for all pixels
        color_diff = np.sqrt(np.sum((img_array - target_color) ** 2, axis=2))
        
        # Create mask based on tolerance
        mask = (color_diff <= tolerance).astype(np.uint8) * 255
        
        return mask
    
    def _apply_anti_aliasing(self, mask: np.ndarray) -> np.ndarray:
        """Apply anti-aliasing to mask edges"""
        
        # Apply Gaussian blur for smooth edges
        blurred = cv2.GaussianBlur(mask, (3, 3), 0.5)
        return blurred
    
    def _apply_feathering(self, mask: np.ndarray, radius: int) -> np.ndarray:
        """Apply feathering (soft edges) to mask"""
        
        if radius <= 0:
            return mask
        
        # Apply Gaussian blur with specified radius
        kernel_size = radius * 2 + 1
        blurred = cv2.GaussianBlur(mask, (kernel_size, kernel_size), radius / 3)
        
        return blurred
    
    def erase_selection(self, 
                       image: Image.Image, 
                       mask: Image.Image,
                       erase_mode: str = 'transparent') -> Image.Image:
        """
        Erase the selected area from the image
        erase_mode: 'transparent', 'white', 'black', or color tuple
        """
        
        # Ensure image has alpha channel
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        img_array = np.array(image)
        mask_array = np.array(mask.convert('L'))
        
        if erase_mode == 'transparent':
            # Set alpha channel based on inverted mask
            img_array[:, :, 3] = np.where(mask_array > 128, 0, img_array[:, :, 3])
        
        elif erase_mode == 'white':
            # Replace selected areas with white
            white_mask = mask_array > 128
            img_array[white_mask] = [255, 255, 255, 255]
        
        elif erase_mode == 'black':
            # Replace selected areas with black
            black_mask = mask_array > 128
            img_array[black_mask] = [0, 0, 0, 255]
        
        elif isinstance(erase_mode, tuple) and len(erase_mode) in [3, 4]:
            # Replace with custom color
            color_mask = mask_array > 128
            if len(erase_mode) == 3:
                erase_mode = erase_mode + (255,)
            img_array[color_mask] = erase_mode
        
        return Image.fromarray(img_array, 'RGBA')
    
    def smart_background_removal(self, image: Image.Image) -> Image.Image:
        """
        Intelligent background removal using multiple techniques
        """
        
        # Convert to RGB for processing
        rgb_image = image.convert('RGB')
        img_array = np.array(rgb_image)
        
        # Method 1: Edge-based background detection
        edge_mask = self._edge_based_background_detection(img_array)
        
        # Method 2: Color clustering
        cluster_mask = self._color_clustering_background_detection(img_array)
        
        # Method 3: Corner-based background detection
        corner_mask = self._corner_based_background_detection(img_array)
        
        # Combine masks using weighted average
        combined_mask = (edge_mask * 0.4 + cluster_mask * 0.4 + corner_mask * 0.2)
        combined_mask = (combined_mask * 255).astype(np.uint8)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        
        # Apply Gaussian blur for smooth edges
        combined_mask = cv2.GaussianBlur(combined_mask, (5, 5), 2)
        
        # Create final image with transparency
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        result_array = np.array(image)
        result_array[:, :, 3] = combined_mask
        
        return Image.fromarray(result_array, 'RGBA')
    
    def _edge_based_background_detection(self, img_array: np.ndarray) -> np.ndarray:
        """Detect foreground using edge detection"""
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection using Canny
        edges = cv2.Canny(blurred, 50, 150)
        
        # Dilate edges to create foreground mask
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=2)
        
        # Fill holes in the mask
        filled = ndimage.binary_fill_holes(dilated).astype(np.uint8)
        
        return filled
    
    def _color_clustering_background_detection(self, img_array: np.ndarray) -> np.ndarray:
        """Detect background using color clustering"""
        
        # Reshape image for clustering
        height, width = img_array.shape[:2]
        reshaped = img_array.reshape(-1, 3)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        labels = kmeans.fit_predict(reshaped)
        
        # Reshape labels back to image shape
        label_image = labels.reshape(height, width)
        
        # Assume the most common cluster in corners is background
        corner_labels = [
            label_image[0, 0], label_image[0, -1], 
            label_image[-1, 0], label_image[-1, -1]
        ]
        background_label = max(set(corner_labels), key=corner_labels.count)
        
        # Create foreground mask (inverse of background)
        foreground_mask = (label_image != background_label).astype(np.uint8)
        
        return foreground_mask
    
    def _corner_based_background_detection(self, img_array: np.ndarray) -> np.ndarray:
        """Detect background based on corner similarity"""
        
        height, width = img_array.shape[:2]
        
        # Get corner colors
        corners = [
            img_array[0, 0],           # Top-left
            img_array[0, width-1],     # Top-right
            img_array[height-1, 0],    # Bottom-left
            img_array[height-1, width-1]  # Bottom-right
        ]
        
        # Calculate average corner color
        avg_corner_color = np.mean(corners, axis=0)
        
        # Calculate color distance from average corner color
        color_diff = np.sqrt(np.sum((img_array - avg_corner_color) ** 2, axis=2))
        
        # Create foreground mask (areas different from corner colors)
        threshold = np.percentile(color_diff, 70)  # Adaptive threshold
        foreground_mask = (color_diff > threshold).astype(np.uint8)
        
        return foreground_mask


class AdvancedSelectionTools:
    """Advanced selection tools for precise editing"""
    
    @staticmethod
    def lasso_select(image: Image.Image, points: List[Tuple[int, int]]) -> Image.Image:
        """Create selection from lasso path"""
        
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        
        if len(points) > 2:
            draw.polygon(points, fill=255)
        
        return mask
    
    @staticmethod
    def rectangular_select(image: Image.Image, 
                          start: Tuple[int, int], 
                          end: Tuple[int, int]) -> Image.Image:
        """Create rectangular selection"""
        
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        
        # Ensure proper rectangle coordinates
        x1, y1 = min(start[0], end[0]), min(start[1], end[1])
        x2, y2 = max(start[0], end[0]), max(start[1], end[1])
        
        draw.rectangle([x1, y1, x2, y2], fill=255)
        
        return mask
    
    @staticmethod
    def elliptical_select(image: Image.Image, 
                         center: Tuple[int, int], 
                         radii: Tuple[int, int]) -> Image.Image:
        """Create elliptical selection"""
        
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        
        x, y = center
        rx, ry = radii
        
        draw.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)
        
        return mask
    
    @staticmethod
    def quick_select(image: Image.Image, 
                    seed_point: Tuple[int, int],
                    tolerance: int = 30) -> Image.Image:
        """Quick selection based on color similarity"""
        
        magic_eraser = MagicEraser()
        magic_eraser.tolerance = tolerance
        magic_eraser.contiguous = False
        
        return magic_eraser.magic_select(image, seed_point)
    
    @staticmethod
    def grow_selection(mask: Image.Image, pixels: int = 5) -> Image.Image:
        """Grow/expand selection by specified pixels"""
        
        mask_array = np.array(mask)
        
        # Create structuring element
        kernel = np.ones((pixels * 2 + 1, pixels * 2 + 1), np.uint8)
        
        # Apply dilation
        grown = cv2.dilate(mask_array, kernel, iterations=1)
        
        return Image.fromarray(grown, 'L')
    
    @staticmethod
    def shrink_selection(mask: Image.Image, pixels: int = 5) -> Image.Image:
        """Shrink/contract selection by specified pixels"""
        
        mask_array = np.array(mask)
        
        # Create structuring element
        kernel = np.ones((pixels * 2 + 1, pixels * 2 + 1), np.uint8)
        
        # Apply erosion
        shrunk = cv2.erode(mask_array, kernel, iterations=1)
        
        return Image.fromarray(shrunk, 'L')
    
    @staticmethod
    def feather_selection(mask: Image.Image, radius: int = 5) -> Image.Image:
        """Apply feathering to selection edges"""
        
        if radius <= 0:
            return mask
        
        mask_array = np.array(mask)
        
        # Apply Gaussian blur
        kernel_size = radius * 2 + 1
        feathered = cv2.GaussianBlur(mask_array, (kernel_size, kernel_size), radius / 3)
        
        return Image.fromarray(feathered, 'L')
    
    @staticmethod
    def invert_selection(mask: Image.Image) -> Image.Image:
        """Invert the selection mask"""
        
        mask_array = np.array(mask)
        inverted = 255 - mask_array
        
        return Image.fromarray(inverted, 'L')
    
    @staticmethod
    def combine_selections(mask1: Image.Image, 
                          mask2: Image.Image, 
                          operation: str = 'union') -> Image.Image:
        """Combine two selection masks"""
        
        array1 = np.array(mask1)
        array2 = np.array(mask2)
        
        if operation == 'union':
            result = np.maximum(array1, array2)
        elif operation == 'intersection':
            result = np.minimum(array1, array2)
        elif operation == 'difference':
            result = np.where(array1 > array2, array1 - array2, 0)
        elif operation == 'symmetric_difference':
            result = np.abs(array1 - array2)
        else:
            result = array1
        
        return Image.fromarray(result.astype(np.uint8), 'L')


class ContentAwareFill:
    """Content-aware fill for seamless object removal"""
    
    @staticmethod
    def fill_selection(image: Image.Image, 
                      mask: Image.Image,
                      method: str = 'telea') -> Image.Image:
        """Fill selected area using content-aware algorithms"""
        
        # Convert to OpenCV format
        img_array = np.array(image.convert('RGB'))
        mask_array = np.array(mask.convert('L'))
        
        # Convert PIL to OpenCV color format
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Apply inpainting
        if method == 'telea':
            result = cv2.inpaint(img_cv, mask_array, 3, cv2.INPAINT_TELEA)
        elif method == 'ns':
            result = cv2.inpaint(img_cv, mask_array, 3, cv2.INPAINT_NS)
        else:
            result = img_cv
        
        # Convert back to PIL format
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(result_rgb, 'RGB')
    
    @staticmethod
    def patch_match_fill(image: Image.Image, 
                        mask: Image.Image,
                        patch_size: int = 9) -> Image.Image:
        """Fill using patch-based texture synthesis"""
        
        img_array = np.array(image.convert('RGB'))
        mask_array = np.array(mask.convert('L')) > 128
        
        height, width = img_array.shape[:2]
        result = img_array.copy()
        
        # Find pixels to fill
        fill_pixels = np.where(mask_array)
        
        for y, x in zip(fill_pixels[0], fill_pixels[1]):
            # Find best matching patch
            best_patch = ContentAwareFill._find_best_patch(
                img_array, mask_array, (x, y), patch_size
            )
            
            if best_patch is not None:
                # Copy patch center pixel
                patch_center = patch_size // 2
                result[y, x] = best_patch[patch_center, patch_center]
        
        return Image.fromarray(result, 'RGB')
    
    @staticmethod
    def _find_best_patch(image: np.ndarray, 
                        mask: np.ndarray, 
                        target_pos: Tuple[int, int],
                        patch_size: int) -> Optional[np.ndarray]:
        """Find the best matching patch for texture synthesis"""
        
        x, y = target_pos
        height, width = image.shape[:2]
        half_size = patch_size // 2
        
        # Extract target patch area
        y1, y2 = max(0, y - half_size), min(height, y + half_size + 1)
        x1, x2 = max(0, x - half_size), min(width, x + half_size + 1)
        
        target_patch = image[y1:y2, x1:x2]
        target_mask = mask[y1:y2, x1:x2]
        
        best_score = float('inf')
        best_patch = None
        
        # Search for similar patches in non-masked areas
        for sy in range(half_size, height - half_size):
            for sx in range(half_size, width - half_size):
                # Skip if this area is masked
                if mask[sy, sx]:
                    continue
                
                # Extract candidate patch
                candidate = image[sy-half_size:sy+half_size+1, sx-half_size:sx+half_size+1]
                
                if candidate.shape != target_patch.shape:
                    continue
                
                # Calculate similarity score (only for non-masked pixels)
                valid_pixels = ~target_mask
                if np.any(valid_pixels):
                    diff = np.sum((candidate[valid_pixels] - target_patch[valid_pixels]) ** 2)
                    
                    if diff < best_score:
                        best_score = diff
                        best_patch = candidate
        
        return best_patch


class SmartCrop:
    """Intelligent cropping with composition analysis"""
    
    @staticmethod
    def auto_crop(image: Image.Image, 
                 composition_rule: str = 'rule_of_thirds') -> Image.Image:
        """Automatically crop image using composition rules"""
        
        if composition_rule == 'rule_of_thirds':
            return SmartCrop._rule_of_thirds_crop(image)
        elif composition_rule == 'golden_ratio':
            return SmartCrop._golden_ratio_crop(image)
        elif composition_rule == 'center_weighted':
            return SmartCrop._center_weighted_crop(image)
        else:
            return image
    
    @staticmethod
    def _rule_of_thirds_crop(image: Image.Image) -> Image.Image:
        """Crop using rule of thirds"""
        
        width, height = image.size
        
        # Calculate rule of thirds points
        third_w, third_h = width // 3, height // 3
        
        # Find the most interesting region
        img_array = np.array(image.convert('RGB'))
        
        # Calculate edge density in different regions
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        best_score = 0
        best_crop = (0, 0, width, height)
        
        # Test different crop regions aligned with rule of thirds
        for x in [0, third_w]:
            for y in [0, third_h]:
                crop_w = min(width - x, third_w * 2)
                crop_h = min(height - y, third_h * 2)
                
                if crop_w > width // 2 and crop_h > height // 2:
                    crop_region = edges[y:y+crop_h, x:x+crop_w]
                    score = np.sum(crop_region)
                    
                    if score > best_score:
                        best_score = score
                        best_crop = (x, y, x + crop_w, y + crop_h)
        
        return image.crop(best_crop)
    
    @staticmethod
    def _golden_ratio_crop(image: Image.Image) -> Image.Image:
        """Crop using golden ratio (1.618:1)"""
        
        width, height = image.size
        golden_ratio = 1.618
        
        # Determine crop dimensions based on golden ratio
        if width / height > golden_ratio:
            # Image is too wide
            new_width = int(height * golden_ratio)
            crop_x = (width - new_width) // 2
            crop_box = (crop_x, 0, crop_x + new_width, height)
        else:
            # Image is too tall
            new_height = int(width / golden_ratio)
            crop_y = (height - new_height) // 2
            crop_box = (0, crop_y, width, crop_y + new_height)
        
        return image.crop(crop_box)
    
    @staticmethod
    def _center_weighted_crop(image: Image.Image) -> Image.Image:
        """Crop focusing on center with some padding"""
        
        width, height = image.size
        
        # Calculate center region (80% of original)
        crop_width = int(width * 0.8)
        crop_height = int(height * 0.8)
        
        crop_x = (width - crop_width) // 2
        crop_y = (height - crop_height) // 2
        
        crop_box = (crop_x, crop_y, crop_x + crop_width, crop_y + crop_height)
        
        return image.crop(crop_box)
    
    @staticmethod
    def smart_resize_crop(image: Image.Image, 
                         target_size: Tuple[int, int],
                         focus_point: Optional[Tuple[int, int]] = None) -> Image.Image:
        """Intelligently resize and crop to target size"""
        
        current_width, current_height = image.size
        target_width, target_height = target_size
        
        # Calculate aspect ratios
        current_ratio = current_width / current_height
        target_ratio = target_width / target_height
        
        if focus_point is None:
            # Use center as focus point
            focus_point = (current_width // 2, current_height // 2)
        
        if current_ratio > target_ratio:
            # Image is wider than target - crop width
            new_width = int(current_height * target_ratio)
            crop_x = max(0, min(current_width - new_width, 
                               focus_point[0] - new_width // 2))
            crop_box = (crop_x, 0, crop_x + new_width, current_height)
        else:
            # Image is taller than target - crop height
            new_height = int(current_width / target_ratio)
            crop_y = max(0, min(current_height - new_height,
                               focus_point[1] - new_height // 2))
            crop_box = (0, crop_y, current_width, crop_y + new_height)
        
        # Crop and resize
        cropped = image.crop(crop_box)
        return cropped.resize(target_size, Image.Resampling.LANCZOS)


class MagicEraserUI:
    """UI components for magic eraser and advanced editing tools"""
    
    @staticmethod
    def render_magic_eraser_panel() -> str:
        """Render the magic eraser tool panel"""
        
        return """
        <div class="magic-eraser-panel">
            <div class="tool-section">
                <h4>🪄 Magic Eraser</h4>
                
                <div class="property-row">
                    <label>Tolerance:</label>
                    <input type="range" id="magic-tolerance" min="1" max="100" value="32" 
                           oninput="updateMagicTolerance(this.value)">
                    <span id="tolerance-value">32</span>
                </div>
                
                <div class="property-row">
                    <label>
                        <input type="checkbox" id="magic-contiguous" checked> Contiguous
                    </label>
                    <label>
                        <input type="checkbox" id="magic-anti-alias" checked> Anti-alias
                    </label>
                </div>
                
                <div class="property-row">
                    <label>Feather:</label>
                    <input type="range" id="magic-feather" min="0" max="20" value="1">
                    <span id="feather-value">1px</span>
                </div>
                
                <div class="button-row">
                    <button class="tool-button" onclick="activateMagicEraser()">🪄 Magic Eraser</button>
                    <button class="tool-button" onclick="smartBackgroundRemoval()">🎯 Smart BG Remove</button>
                </div>
            </div>
            
            <div class="tool-section">
                <h4>✂️ Selection Tools</h4>
                
                <div class="tool-grid">
                    <button class="tool-option" onclick="selectTool('rectangular-select')" title="Rectangle Select">
                        <div>⬜</div><div>Rectangle</div>
                    </button>
                    <button class="tool-option" onclick="selectTool('elliptical-select')" title="Ellipse Select">
                        <div>⭕</div><div>Ellipse</div>
                    </button>
                    <button class="tool-option" onclick="selectTool('lasso-select')" title="Lasso Select">
                        <div>🎯</div><div>Lasso</div>
                    </button>
                    <button class="tool-option" onclick="selectTool('quick-select')" title="Quick Select">
                        <div>⚡</div><div>Quick</div>
                    </button>
                </div>
            </div>
            
            <div class="tool-section">
                <h4>🔧 Selection Modify</h4>
                
                <div class="property-row">
                    <label>Grow/Shrink:</label>
                    <input type="number" id="modify-pixels" value="5" min="1" max="50" style="width: 50px;">
                    <span>px</span>
                </div>
                
                <div class="button-row">
                    <button class="tool-button small" onclick="growSelection()">➕ Grow</button>
                    <button class="tool-button small" onclick="shrinkSelection()">➖ Shrink</button>
                </div>
                
                <div class="button-row">
                    <button class="tool-button small" onclick="featherSelection()">🌟 Feather</button>
                    <button class="tool-button small" onclick="invertSelection()">🔄 Invert</button>
                </div>
            </div>
            
            <div class="tool-section">
                <h4>🎨 Content-Aware Fill</h4>
                
                <div class="property-row">
                    <label>Method:</label>
                    <select id="fill-method">
                        <option value="telea">Telea</option>
                        <option value="ns">Navier-Stokes</option>
                        <option value="patch">Patch Match</option>
                    </select>
                </div>
                
                <button class="tool-button large" onclick="contentAwareFill()">🪄 Fill Selection</button>
            </div>
            
            <div class="tool-section">
                <h4>✂️ Smart Crop</h4>
                
                <div class="property-row">
                    <label>Rule:</label>
                    <select id="crop-rule">
                        <option value="rule_of_thirds">Rule of Thirds</option>
                        <option value="golden_ratio">Golden Ratio</option>
                        <option value="center_weighted">Center Weighted</option>
                    </select>
                </div>
                
                <button class="tool-button large" onclick="smartCrop()">✂️ Auto Crop</button>
            </div>
        </div>
        
        <style>
        .magic-eraser-panel {
            padding: 12px;
            max-height: 100%;
            overflow-y: auto;
        }
        
        .tool-section {
            margin-bottom: 16px;
            padding: 8px;
            background: var(--bg-tertiary);
            border-radius: 4px;
            border: 1px solid var(--border-primary);
        }
        
        .tool-section h4 {
            margin: 0 0 8px 0;
            color: var(--text-primary);
            font-size: 11px;
            border-bottom: 1px solid var(--border-primary);
            padding-bottom: 4px;
        }
        
        .button-row {
            display: flex;
            gap: 4px;
            margin: 4px 0;
        }
        
        .tool-button.small {
            flex: 1;
            padding: 4px 6px;
            font-size: 9px;
        }
        
        .tool-button.large {
            width: 100%;
            padding: 6px 8px;
            font-size: 10px;
        }
        </style>
        
        <script>
        // Magic Eraser JavaScript functionality
        let currentSelection = null;
        let selectionMode = 'magic-eraser';
        let isSelecting = false;
        let selectionPath = [];
        
        function updateMagicTolerance(value) {
            document.getElementById('tolerance-value').textContent = value;
        }
        
        function updateFeatherValue() {
            const value = document.getElementById('magic-feather').value;
            document.getElementById('feather-value').textContent = value + 'px';
        }
        
        function activateMagicEraser() {
            currentTool = 'magic-eraser';
            selectTool('magic-eraser');
            updateCanvasCursor();
        }
        
        function smartBackgroundRemoval() {
            const activeObj = canvas.getActiveObject();
            if (activeObj && activeObj.type === 'image') {
                // This would call the Python backend for smart background removal
                console.log('Smart background removal for:', activeObj);
                // Placeholder: show processing indicator
                showProcessingIndicator('Removing background...');
                
                // Simulate processing delay
                setTimeout(() => {
                    hideProcessingIndicator();
                    console.log('Background removal complete');
                }, 2000);
            } else {
                alert('Please select an image first');
            }
        }
        
        function growSelection() {
            if (currentSelection) {
                const pixels = parseInt(document.getElementById('modify-pixels').value);
                console.log('Growing selection by', pixels, 'pixels');
                // Implementation would modify the current selection
            }
        }
        
        function shrinkSelection() {
            if (currentSelection) {
                const pixels = parseInt(document.getElementById('modify-pixels').value);
                console.log('Shrinking selection by', pixels, 'pixels');
                // Implementation would modify the current selection
            }
        }
        
        function featherSelection() {
            if (currentSelection) {
                const radius = parseInt(document.getElementById('magic-feather').value);
                console.log('Feathering selection with radius', radius);
                // Implementation would apply feathering to current selection
            }
        }
        
        function invertSelection() {
            if (currentSelection) {
                console.log('Inverting selection');
                // Implementation would invert the current selection
            }
        }
        
        function contentAwareFill() {
            if (currentSelection) {
                const method = document.getElementById('fill-method').value;
                console.log('Content-aware fill using method:', method);
                showProcessingIndicator('Filling selection...');
                
                // Simulate processing
                setTimeout(() => {
                    hideProcessingIndicator();
                    console.log('Content-aware fill complete');
                }, 3000);
            } else {
                alert('Please make a selection first');
            }
        }
        
        function smartCrop() {
            const activeObj = canvas.getActiveObject();
            if (activeObj && activeObj.type === 'image') {
                const rule = document.getElementById('crop-rule').value;
                console.log('Smart crop using rule:', rule);
                showProcessingIndicator('Analyzing composition...');
                
                setTimeout(() => {
                    hideProcessingIndicator();
                    console.log('Smart crop complete');
                }, 1500);
            } else {
                alert('Please select an image first');
            }
        }
        
        function showProcessingIndicator(message) {
            // Create or update processing indicator
            let indicator = document.getElementById('processing-indicator');
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.id = 'processing-indicator';
                indicator.style.cssText = `
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: var(--bg-secondary);
                    border: 1px solid var(--border-primary);
                    border-radius: 8px;
                    padding: 20px;
                    z-index: 10000;
                    color: var(--text-primary);
                    font-size: 14px;
                    box-shadow: var(--shadow-panel);
                `;
                document.body.appendChild(indicator);
            }
            indicator.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 20px; height: 20px; border: 2px solid var(--bg-active); border-top: 2px solid transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                    <span>${message}</span>
                </div>
            `;
        }
        
        function hideProcessingIndicator() {
            const indicator = document.getElementById('processing-indicator');
            if (indicator) {
                indicator.remove();
            }
        }
        
        // Enhanced mouse handlers for selection tools
        function handleSelectionMouseDown(event) {
            if (currentTool.includes('select')) {
                isSelecting = true;
                const pointer = canvas.getPointer(event.e);
                
                if (currentTool === 'lasso-select') {
                    selectionPath = [pointer];
                } else {
                    selectionStart = pointer;
                }
            }
        }
        
        function handleSelectionMouseMove(event) {
            if (isSelecting && currentTool.includes('select')) {
                const pointer = canvas.getPointer(event.e);
                
                if (currentTool === 'lasso-select') {
                    selectionPath.push(pointer);
                    // Draw temporary path
                    drawSelectionPreview();
                }
            }
        }
        
        function handleSelectionMouseUp(event) {
            if (isSelecting && currentTool.includes('select')) {
                isSelecting = false;
                const pointer = canvas.getPointer(event.e);
                
                switch(currentTool) {
                    case 'rectangular-select':
                        createRectangularSelection(selectionStart, pointer);
                        break;
                    case 'elliptical-select':
                        createEllipticalSelection(selectionStart, pointer);
                        break;
                    case 'lasso-select':
                        createLassoSelection(selectionPath);
                        break;
                    case 'quick-select':
                        createQuickSelection(pointer);
                        break;
                }
            }
        }
        
        function createRectangularSelection(start, end) {
            console.log('Creating rectangular selection from', start, 'to', end);
            // Implementation would create rectangular selection
        }
        
        function createEllipticalSelection(start, end) {
            console.log('Creating elliptical selection from', start, 'to', end);
            // Implementation would create elliptical selection
        }
        
        function createLassoSelection(path) {
            console.log('Creating lasso selection with', path.length, 'points');
            // Implementation would create lasso selection
        }
        
        function createQuickSelection(point) {
            const tolerance = parseInt(document.getElementById('magic-tolerance').value);
            console.log('Creating quick selection at', point, 'with tolerance', tolerance);
            // Implementation would create quick selection
        }
        
        function drawSelectionPreview() {
            // Implementation would draw selection preview
        }
        
        // Add CSS animation for spinner
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
        
        // Initialize feather value display
        document.getElementById('magic-feather').addEventListener('input', updateFeatherValue);
        updateFeatherValue();
        
        console.log('Magic Eraser UI initialized');
        </script>
        """


# Integration functions
def integrate_magic_eraser_with_streamlit():
    """Integration example for Streamlit"""
    
    import streamlit as st
    
    st.subheader("🪄 Magic Eraser Tools")
    
    # Tool selection
    tool = st.selectbox(
        "Select Tool",
        ["Magic Eraser", "Smart Background Removal", "Content-Aware Fill", "Smart Crop"]
    )
    
    if tool == "Magic Eraser":
        col1, col2 = st.columns(2)
        with col1:
            tolerance = st.slider("Tolerance", 1, 100, 32)
            contiguous = st.checkbox("Contiguous Selection", True)
        with col2:
            anti_alias = st.checkbox("Anti-aliasing", True)
            feather = st.slider("Feather Radius", 0, 20, 1)
    
    elif tool == "Smart Background Removal":
        st.info("Click on the image to automatically remove the background")
    
    elif tool == "Content-Aware Fill":
        fill_method = st.selectbox(
            "Fill Method",
            ["Telea", "Navier-Stokes", "Patch Match"]
        )
    
    elif tool == "Smart Crop":
        crop_rule = st.selectbox(
            "Composition Rule",
            ["Rule of Thirds", "Golden Ratio", "Center Weighted"]
        )
    
    # File uploader for testing
    uploaded_file = st.file_uploader("Upload image to test", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original")
            st.image(image, use_column_width=True)
        
        with col2:
            st.subheader("Result")
            
            if tool == "Magic Eraser":
                # Demo magic eraser (would need click coordinates in real implementation)
                magic_eraser = MagicEraser()
                magic_eraser.tolerance = tolerance
                magic_eraser.contiguous = contiguous
                magic_eraser.anti_alias = anti_alias
                magic_eraser.feather_radius = feather
                
                # Use center point as demo
                center_point = (image.width // 2, image.height // 2)
                mask = magic_eraser.magic_select(image, center_point)
                result = magic_eraser.erase_selection(image, mask)
                st.image(result, use_column_width=True)
            
            elif tool == "Smart Background Removal":
                magic_eraser = MagicEraser()
                result = magic_eraser.smart_background_removal(image)
                st.image(result, use_column_width=True)
            
            elif tool == "Smart Crop":
                smart_crop = SmartCrop()
                result = smart_crop.auto_crop(image, crop_rule.lower().replace(' ', '_'))
                st.image(result, use_column_width=True)
            
            else:
                st.image(image, use_column_width=True)


"""
Image Processing Utilities
Advanced image manipulation and processing functions
"""

import io
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
from typing import Tuple, List, Optional, Dict, Any
import cv2
import base64

class ImageProcessor:
    """Advanced image processing utilities"""
    
    @staticmethod
    def resize_image(image: Image.Image, 
                    target_size: Tuple[int, int], 
                    maintain_aspect: bool = True,
                    resample: int = Image.Resampling.LANCZOS) -> Image.Image:
        """Resize image with various options"""
        
        if maintain_aspect:
            # Calculate the ratio to maintain aspect ratio
            ratio = min(target_size[0] / image.width, target_size[1] / image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            resized = image.resize(new_size, resample)
            
            # Create a new image with target size and paste the resized image
            result = Image.new('RGBA', target_size, (0, 0, 0, 0))
            paste_x = (target_size[0] - new_size[0]) // 2
            paste_y = (target_size[1] - new_size[1]) // 2
            result.paste(resized, (paste_x, paste_y))
            
            return result
        else:
            return image.resize(target_size, resample)
    
    @staticmethod
    def crop_image(image: Image.Image, 
                  crop_box: Tuple[int, int, int, int]) -> Image.Image:
        """Crop image to specified box (left, top, right, bottom)"""
        return image.crop(crop_box)
    
    @staticmethod
    def rotate_image(image: Image.Image, 
                    angle: float, 
                    expand: bool = True,
                    fill_color: Tuple[int, int, int, int] = (255, 255, 255, 0)) -> Image.Image:
        """Rotate image by specified angle"""
        return image.rotate(angle, expand=expand, fillcolor=fill_color)
    
    @staticmethod
    def flip_image(image: Image.Image, direction: str = 'horizontal') -> Image.Image:
        """Flip image horizontally or vertically"""
        if direction.lower() == 'horizontal':
            return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        elif direction.lower() == 'vertical':
            return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
    
    @staticmethod
    def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
        """Adjust image brightness (1.0 = no change, >1.0 = brighter, <1.0 = darker)"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
        """Adjust image contrast (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_saturation(image: Image.Image, factor: float) -> Image.Image:
        """Adjust image saturation (1.0 = no change, >1.0 = more saturated, <1.0 = less saturated)"""
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_sharpness(image: Image.Image, factor: float) -> Image.Image:
        """Adjust image sharpness (1.0 = no change, >1.0 = sharper, <1.0 = blurred)"""
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def apply_blur(image: Image.Image, radius: float = 1.0) -> Image.Image:
        """Apply Gaussian blur to image"""
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    @staticmethod
    def apply_sharpen(image: Image.Image) -> Image.Image:
        """Apply sharpening filter to image"""
        return image.filter(ImageFilter.SHARPEN)
    
    @staticmethod
    def apply_edge_enhance(image: Image.Image) -> Image.Image:
        """Apply edge enhancement filter"""
        return image.filter(ImageFilter.EDGE_ENHANCE)
    
    @staticmethod
    def apply_emboss(image: Image.Image) -> Image.Image:
        """Apply emboss effect"""
        return image.filter(ImageFilter.EMBOSS)
    
    @staticmethod
    def convert_to_grayscale(image: Image.Image) -> Image.Image:
        """Convert image to grayscale"""
        return image.convert('L').convert('RGB')
    
    @staticmethod
    def convert_to_sepia(image: Image.Image) -> Image.Image:
        """Convert image to sepia tone"""
        # Convert to grayscale first
        grayscale = image.convert('L')
        
        # Create sepia effect
        sepia = Image.new('RGB', grayscale.size)
        pixels = sepia.load()
        gray_pixels = grayscale.load()
        
        for i in range(grayscale.width):
            for j in range(grayscale.height):
                gray_value = gray_pixels[i, j]
                # Apply sepia tone
                r = min(255, int(gray_value * 1.0))
                g = min(255, int(gray_value * 0.8))
                b = min(255, int(gray_value * 0.6))
                pixels[i, j] = (r, g, b)
        
        return sepia
    
    @staticmethod
    def remove_background_simple(image: Image.Image, 
                                tolerance: int = 30,
                                target_color: Tuple[int, int, int] = None) -> Image.Image:
        """Simple background removal based on color similarity"""
        
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        data = np.array(image)
        
        # If no target color specified, use the corner pixels
        if target_color is None:
            # Use the most common corner color
            corners = [
                tuple(data[0, 0, :3]),  # Top-left
                tuple(data[0, -1, :3]), # Top-right
                tuple(data[-1, 0, :3]), # Bottom-left
                tuple(data[-1, -1, :3]) # Bottom-right
            ]
            target_color = max(set(corners), key=corners.count)
        
        # Calculate color distance
        target = np.array(target_color)
        distances = np.sqrt(np.sum((data[:, :, :3] - target) ** 2, axis=2))
        
        # Create mask
        mask = distances <= tolerance
        
        # Set alpha channel
        data[:, :, 3] = np.where(mask, 0, 255)
        
        return Image.fromarray(data, 'RGBA')
    
    @staticmethod
    def create_drop_shadow(image: Image.Image,
                          offset: Tuple[int, int] = (5, 5),
                          blur_radius: int = 3,
                          shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 128)) -> Image.Image:
        """Create drop shadow effect"""
        
        # Create shadow layer
        shadow = Image.new('RGBA', 
                          (image.width + abs(offset[0]) + blur_radius * 2,
                           image.height + abs(offset[1]) + blur_radius * 2),
                          (0, 0, 0, 0))
        
        # Create shadow shape
        shadow_shape = Image.new('RGBA', image.size, (0, 0, 0, 0))
        if image.mode == 'RGBA':
            # Use alpha channel as mask
            shadow_shape.paste(shadow_color, (0, 0), image)
        else:
            # Create shadow from opaque image
            shadow_shape.paste(shadow_color, (0, 0))
        
        # Apply blur to shadow
        shadow_shape = shadow_shape.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # Position shadow
        shadow_x = blur_radius + max(0, offset[0])
        shadow_y = blur_radius + max(0, offset[1])
        shadow.paste(shadow_shape, (shadow_x, shadow_y), shadow_shape)
        
        # Position original image
        image_x = blur_radius + max(0, -offset[0])
        image_y = blur_radius + max(0, -offset[1])
        shadow.paste(image, (image_x, image_y), image if image.mode == 'RGBA' else None)
        
        return shadow
    
    @staticmethod
    def create_border(image: Image.Image,
                     border_width: int = 5,
                     border_color: Tuple[int, int, int] = (0, 0, 0),
                     border_style: str = 'solid') -> Image.Image:
        """Add border to image"""
        
        if border_style == 'solid':
            return ImageOps.expand(image, border=border_width, fill=border_color)
        
        elif border_style == 'rounded':
            # Create rounded border (simplified version)
            bordered = ImageOps.expand(image, border=border_width, fill=border_color)
            return bordered
        
        else:
            return image
    
    @staticmethod
    def apply_vignette(image: Image.Image,
                      strength: float = 0.5,
                      radius: float = 0.8) -> Image.Image:
        """Apply vignette effect"""
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create vignette mask
        width, height = image.size
        center_x, center_y = width // 2, height // 2
        
        # Create gradient mask
        mask = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(mask)
        
        # Calculate vignette parameters
        max_distance = min(width, height) * radius / 2
        
        for x in range(width):
            for y in range(height):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if distance > max_distance:
                    fade = max(0, 255 - int((distance - max_distance) * strength * 255 / max_distance))
                    mask.putpixel((x, y), fade)
        
        # Apply mask
        result = Image.new('RGB', image.size)
        result.paste(image, (0, 0))
        
        # Blend with darkened version
        darkened = ImageEnhance.Brightness(image).enhance(1 - strength)
        result = Image.composite(result, darkened, mask)
        
        return result
    
    @staticmethod
    def color_replace(image: Image.Image,
                     target_color: Tuple[int, int, int],
                     replacement_color: Tuple[int, int, int],
                     tolerance: int = 30) -> Image.Image:
        """Replace specific color in image"""
        
        data = np.array(image.convert('RGB'))
        target = np.array(target_color)
        replacement = np.array(replacement_color)
        
        # Calculate color distance
        distances = np.sqrt(np.sum((data - target) ** 2, axis=2))
        
        # Create mask for pixels within tolerance
        mask = distances <= tolerance
        
        # Replace colors
        data[mask] = replacement
        
        return Image.fromarray(data, 'RGB')
    
    @staticmethod
    def extract_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from image"""
        
        # Resize image for faster processing
        small_image = image.resize((100, 100))
        
        # Convert to RGB if necessary
        if small_image.mode != 'RGB':
            small_image = small_image.convert('RGB')
        
        # Use quantization to find dominant colors
        quantized = small_image.quantize(colors=num_colors)
        palette = quantized.getpalette()
        
        # Extract colors
        colors = []
        if palette:
            for i in range(0, min(num_colors * 3, len(palette)), 3):
                if i + 2 < len(palette):
                    colors.append((palette[i], palette[i+1], palette[i+2]))
        
        return colors
    
    @staticmethod
    def create_gradient(size: Tuple[int, int],
                       start_color: Tuple[int, int, int],
                       end_color: Tuple[int, int, int],
                       direction: str = 'horizontal') -> Image.Image:
        """Create gradient image"""
        
        gradient = Image.new('RGB', size)
        draw = ImageDraw.Draw(gradient)
        
        if direction == 'horizontal':
            for x in range(size[0]):
                ratio = x / size[0]
                color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio) for i in range(3))
                draw.line([(x, 0), (x, size[1])], fill=color)
        
        elif direction == 'vertical':
            for y in range(size[1]):
                ratio = y / size[1]
                color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio) for i in range(3))
                draw.line([(0, y), (size[0], y)], fill=color)
        
        elif direction == 'radial':
            center_x, center_y = size[0] // 2, size[1] // 2
            max_distance = min(size[0], size[1]) // 2
            
            for x in range(size[0]):
                for y in range(size[1]):
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    ratio = min(1.0, distance / max_distance)
                    color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio) for i in range(3))
                    draw.point((x, y), fill=color)
        
        return gradient
    
    @staticmethod
    def apply_noise(image: Image.Image, intensity: float = 0.1) -> Image.Image:
        """Add noise to image"""
        
        data = np.array(image)
        noise = np.random.randint(-int(255 * intensity), int(255 * intensity), data.shape)
        
        # Add noise and clamp values
        noisy_data = np.clip(data.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        return Image.fromarray(noisy_data, image.mode)
    
    @staticmethod
    def create_texture(size: Tuple[int, int], texture_type: str = 'noise') -> Image.Image:
        """Create texture patterns"""
        
        texture = Image.new('RGB', size, (128, 128, 128))
        
        if texture_type == 'noise':
            return ImageProcessor.apply_noise(texture, 0.3)
        
        elif texture_type == 'lines':
            draw = ImageDraw.Draw(texture)
            for y in range(0, size[1], 4):
                draw.line([(0, y), (size[0], y)], fill=(100, 100, 100))
            return texture
        
        elif texture_type == 'dots':
            draw = ImageDraw.Draw(texture)
            for x in range(0, size[0], 10):
                for y in range(0, size[1], 10):
                    draw.ellipse([x-2, y-2, x+2, y+2], fill=(80, 80, 80))
            return texture
        
        elif texture_type == 'grid':
            draw = ImageDraw.Draw(texture)
            for x in range(0, size[0], 20):
                draw.line([(x, 0), (x, size[1])], fill=(100, 100, 100))
            for y in range(0, size[1], 20):
                draw.line([(0, y), (size[0], y)], fill=(100, 100, 100))
            return texture
        
        return texture
    
    @staticmethod
    def image_to_base64(image: Image.Image, format: str = 'PNG') -> str:
        """Convert PIL Image to base64 string"""
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/{format.lower()};base64,{img_str}"
    
    @staticmethod
    def base64_to_image(base64_string: str) -> Image.Image:
        """Convert base64 string to PIL Image"""
        # Remove data URL prefix if present
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_data))
    
    @staticmethod
    def get_image_info(image: Image.Image) -> Dict[str, Any]:
        """Get comprehensive image information"""
        
        info = {
            'size': image.size,
            'width': image.width,
            'height': image.height,
            'mode': image.mode,
            'format': image.format,
            'has_transparency': image.mode in ('RGBA', 'LA') or 'transparency' in image.info
        }
        
        # Calculate file size estimate
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        info['estimated_size'] = len(buffer.getvalue())
        
        # Get color statistics
        if image.mode == 'RGB':
            colors = image.getcolors(maxcolors=256*256*256)
            if colors:
                info['unique_colors'] = len(colors)
                info['most_common_color'] = colors[0][1]  # Most frequent color
        
        return info


class AdvancedImageProcessor:
    """More advanced image processing using OpenCV"""
    
    @staticmethod
    def pil_to_cv2(image: Image.Image) -> np.ndarray:
        """Convert PIL Image to OpenCV format"""
        if image.mode == 'RGB':
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        elif image.mode == 'RGBA':
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGRA)
        else:
            return np.array(image)
    
    @staticmethod
    def cv2_to_pil(image: np.ndarray) -> Image.Image:
        """Convert OpenCV format to PIL Image"""
        if len(image.shape) == 3:
            if image.shape[2] == 3:
                return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            elif image.shape[2] == 4:
                return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA))
        return Image.fromarray(image)
    
    @staticmethod
    def edge_detection(image: Image.Image, 
                      method: str = 'canny',
                      threshold1: int = 100,
                      threshold2: int = 200) -> Image.Image:
        """Apply edge detection"""
        
        cv_image = AdvancedImageProcessor.pil_to_cv2(image)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        if method == 'canny':
            edges = cv2.Canny(gray, threshold1, threshold2)
        elif method == 'sobel':
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            edges = np.sqrt(sobelx**2 + sobely**2)
            edges = np.uint8(edges / edges.max() * 255)
        elif method == 'laplacian':
            edges = cv2.Laplacian(gray, cv2.CV_64F)
            edges = np.uint8(np.absolute(edges))
        else:
            edges = gray
        
        return Image.fromarray(edges, 'L')
    
    @staticmethod
    def morphological_operations(image: Image.Image,
                               operation: str = 'opening',
                               kernel_size: int = 5) -> Image.Image:
        """Apply morphological operations"""
        
        cv_image = AdvancedImageProcessor.pil_to_cv2(image)
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        if operation == 'erosion':
            result = cv2.erode(cv_image, kernel, iterations=1)
        elif operation == 'dilation':
            result = cv2.dilate(cv_image, kernel, iterations=1)
        elif operation == 'opening':
            result = cv2.morphologyEx(cv_image, cv2.MORPH_OPEN, kernel)
        elif operation == 'closing':
            result = cv2.morphologyEx(cv_image, cv2.MORPH_CLOSE, kernel)
        elif operation == 'gradient':
            result = cv2.morphologyEx(cv_image, cv2.MORPH_GRADIENT, kernel)
        else:
            result = cv_image
        
        return Image.fromarray(result, 'L')
    
    @staticmethod
    def histogram_equalization(image: Image.Image) -> Image.Image:
        """Apply histogram equalization"""
        
        cv_image = AdvancedImageProcessor.pil_to_cv2(image)
        
        if len(cv_image.shape) == 3:
            # Convert to YUV and equalize Y channel
            yuv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2YUV)
            yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
            result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        else:
            result = cv2.equalizeHist(cv_image)
        
        return AdvancedImageProcessor.cv2_to_pil(result)
    
    @staticmethod
    def adaptive_threshold(image: Image.Image,
                          max_value: int = 255,
                          adaptive_method: str = 'gaussian',
                          threshold_type: str = 'binary',
                          block_size: int = 11,
                          c: int = 2) -> Image.Image:
        """Apply adaptive thresholding"""
        
        cv_image = AdvancedImageProcessor.pil_to_cv2(image)
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        adaptive_method_cv = cv2.ADAPTIVE_THRESH_GAUSSIAN_C if adaptive_method == 'gaussian' else cv2.ADAPTIVE_THRESH_MEAN_C
        threshold_type_cv = cv2.THRESH_BINARY if threshold_type == 'binary' else cv2.THRESH_BINARY_INV
        
        result = cv2.adaptiveThreshold(cv_image, max_value, adaptive_method_cv, threshold_type_cv, block_size, c)
        
        return Image.fromarray(result, 'L')
    
    @staticmethod
    def contour_detection(image: Image.Image,
                         min_area: int = 100) -> Tuple[Image.Image, List[Dict]]:
        """Detect and return contours"""
        
        cv_image = AdvancedImageProcessor.pil_to_cv2(image)
        if len(cv_image.shape) == 3:
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv_image
        
        # Find contours
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area
        filtered_contours = [c for c in contours if cv2.contourArea(c) > min_area]
        
        # Draw contours on image
        result = cv_image.copy()
        cv2.drawContours(result, filtered_contours, -1, (0, 255, 0), 2)
        
        # Extract contour information
        contour_info = []
        for contour in filtered_contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            x, y, w, h = cv2.boundingRect(contour)
            
            contour_info.append({
                'area': area,
                'perimeter': perimeter,
                'bounding_box': (x, y, w, h),
                'center': (x + w//2, y + h//2)
            })
        
        return AdvancedImageProcessor.cv2_to_pil(result), contour_info


# Utility functions for integration
def create_image_filters():
    """Create a collection of predefined image filters"""
    
    filters = {
        'vintage': lambda img: ImageProcessor.convert_to_sepia(
            ImageProcessor.adjust_contrast(
                ImageProcessor.apply_vignette(img, 0.3), 0.9
            )
        ),
        
        'black_white': lambda img: ImageProcessor.convert_to_grayscale(
            ImageProcessor.adjust_contrast(img, 1.2)
        ),
        
        'bright_pop': lambda img: ImageProcessor.adjust_saturation(
            ImageProcessor.adjust_brightness(img, 1.2), 1.3
        ),
        
        'soft_glow': lambda img: ImageProcessor.apply_blur(
            ImageProcessor.adjust_brightness(img, 1.1), 0.5
        ),
        
        'sharp_detail': lambda img: ImageProcessor.apply_sharpen(
            ImageProcessor.adjust_contrast(img, 1.1)
        ),
        
        'cool_tone': lambda img: ImageProcessor.color_replace(
            img, (255, 255, 255), (240, 248, 255), 50
        ),
        
        'warm_tone': lambda img: ImageProcessor.color_replace(
            img, (255, 255, 255), (255, 248, 240), 50
        )
    }
    
    return filters

def batch_process_images(images: List[Image.Image], 
                        operations: List[callable]) -> List[Image.Image]:
    """Apply a series of operations to multiple images"""
    
    results = []
    for image in images:
        processed = image
        for operation in operations:
            processed = operation(processed)
        results.append(processed)
    
    return results


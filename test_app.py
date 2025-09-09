"""
Test version of Enhanced Business Card Editor
Simplified version to verify core functionality
"""

import streamlit as st
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

st.set_page_config(
    page_title="Enhanced Business Card Editor - Test",
    page_icon="🎨",
    layout="wide"
)

def main():
    st.title("🎨 Enhanced Business Card Editor")
    st.markdown("### Professional Design Tool - Test Version")
    
    # Test basic functionality
    st.markdown("---")
    st.subheader("✅ System Status")
    
    # Test imports
    try:
        import streamlit
        st.success(f"✓ Streamlit {streamlit.__version__}")
    except Exception as e:
        st.error(f"✗ Streamlit import failed: {e}")
    
    try:
        from PIL import Image
        st.success("✓ PIL/Pillow")
    except Exception as e:
        st.error(f"✗ PIL import failed: {e}")
    
    try:
        import numpy as np
        st.success(f"✓ NumPy {np.__version__}")
    except Exception as e:
        st.error(f"✗ NumPy import failed: {e}")
    
    try:
        import cv2
        st.success(f"✓ OpenCV {cv2.__version__}")
    except Exception as e:
        st.error(f"✗ OpenCV import failed: {e}")
    
    try:
        from sklearn import __version__ as sklearn_version
        st.success(f"✓ scikit-learn {sklearn_version}")
    except Exception as e:
        st.error(f"✗ scikit-learn import failed: {e}")
    
    # Test component imports
    st.markdown("---")
    st.subheader("🧩 Component Status")
    
    try:
        from utils.canvas_sizes import CanvasSizeManager
        manager = CanvasSizeManager()
        sizes_count = len(manager.sizes)
        st.success(f"✓ Canvas Size Manager - {sizes_count} sizes available")
    except Exception as e:
        st.error(f"✗ Canvas Size Manager failed: {e}")
    
    try:
        from utils.image_processing import ImageProcessor
        st.success("✓ Image Processor")
    except Exception as e:
        st.error(f"✗ Image Processor failed: {e}")
    
    try:
        from components.image_library import ImageLibrary
        library = ImageLibrary()
        st.success("✓ Image Library")
    except Exception as e:
        st.error(f"✗ Image Library failed: {e}")
    
    try:
        from components.magic_eraser import MagicEraser
        eraser = MagicEraser()
        st.success("✓ Magic Eraser")
    except Exception as e:
        st.error(f"✗ Magic Eraser failed: {e}")
    
    # Test UI components
    st.markdown("---")
    st.subheader("🎨 UI Demo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Tools")
        if st.button("🔍 Select", use_container_width=True):
            st.info("Select tool activated")
        if st.button("✋ Move", use_container_width=True):
            st.info("Move tool activated")
        if st.button("🪄 Magic Eraser", use_container_width=True):
            st.info("Magic Eraser activated")
    
    with col2:
        st.markdown("#### Canvas")
        canvas_size = st.selectbox(
            "Canvas Size",
            ["US Business Card (1050×600)", "Instagram Post (1080×1080)", "A4 Flyer (2480×3508)"]
        )
        
        # Simple canvas placeholder
        st.markdown("""
        <div style="border: 2px solid #ccc; height: 300px; background: #f9f9f9; 
                    display: flex; align-items: center; justify-content: center; 
                    border-radius: 8px; margin: 10px 0;">
            <div style="text-align: center; color: #666;">
                <div style="font-size: 48px; margin-bottom: 10px;">🎨</div>
                <div>Canvas Area</div>
                <div style="font-size: 12px; margin-top: 5px;">{}</div>
            </div>
        </div>
        """.format(canvas_size), unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### Properties")
        color = st.color_picker("Color", "#3498db")
        opacity = st.slider("Opacity", 0, 100, 100)
        font_size = st.slider("Font Size", 8, 72, 16)
        
        st.markdown("#### Export")
        export_format = st.selectbox("Format", ["PNG", "JPG", "PDF", "SVG"])
        if st.button("📤 Export", use_container_width=True):
            st.success(f"Exporting as {export_format}...")
    
    # Feature showcase
    st.markdown("---")
    st.subheader("🚀 Features")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        **🎨 Design Tools:**
        - 60+ Canvas Sizes
        - Professional Layout
        - Advanced Typography
        - Layer Management
        
        **🪄 Magic Features:**
        - AI-Powered Selection
        - Smart Background Removal
        - Content-Aware Fill
        - Intelligent Cropping
        """)
    
    with features_col2:
        st.markdown("""
        **📚 Asset Management:**
        - Local Image Library
        - Smart Categorization
        - Advanced Search
        - Batch Operations
        
        **📤 Export Options:**
        - Multiple Formats
        - Print Quality
        - Professional Settings
        - Batch Export
        """)
    
    # File upload test
    st.markdown("---")
    st.subheader("📁 File Upload Test")
    
    uploaded_file = st.file_uploader(
        "Test image upload",
        type=['png', 'jpg', 'jpeg', 'gif'],
        help="Upload an image to test the processing pipeline"
    )
    
    if uploaded_file:
        try:
            from PIL import Image
            import io
            
            # Display original
            image = Image.open(uploaded_file)
            st.success(f"✓ Image loaded: {image.size[0]}×{image.size[1]} pixels")
            
            col_orig, col_processed = st.columns(2)
            
            with col_orig:
                st.markdown("**Original**")
                st.image(image, use_column_width=True)
            
            with col_processed:
                st.markdown("**Processed**")
                # Simple processing test
                try:
                    from utils.image_processing import ImageProcessor
                    processed = ImageProcessor.adjust_brightness(image, 1.2)
                    st.image(processed, use_column_width=True)
                    st.success("✓ Image processing successful")
                except Exception as e:
                    st.error(f"✗ Processing failed: {e}")
                    st.image(image, use_column_width=True)
        
        except Exception as e:
            st.error(f"✗ Image loading failed: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        Enhanced Business Card Editor v2.0 - Test Version<br>
        🎨 Professional Design Tool with Advanced Features
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


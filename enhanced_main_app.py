"""
Enhanced Business Card Editor - Main Application
Comprehensive design tool with advanced features
"""

import streamlit as st
import json
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional
import io
from PIL import Image
import numpy as np

# Import our custom components
from components.ui_components import UIComponentManager
from components.image_library import ImageLibrary, ImageLibraryUI
from components.magic_eraser import MagicEraser, MagicEraserUI, AdvancedSelectionTools
from utils.canvas_sizes import CanvasSizeManager, CanvasSizeUI
from utils.image_processing import ImageProcessor, AdvancedImageProcessor

# Configure Streamlit page
st.set_page_config(
    page_title="Enhanced Business Card Editor",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

class EnhancedBusinessCardEditor:
    """Main application class for the enhanced business card editor"""
    
    def __init__(self):
        self.initialize_session_state()
        self.ui_manager = UIComponentManager()
        self.image_library = self.get_image_library()
        self.library_ui = ImageLibraryUI(self.image_library)
        self.size_manager = CanvasSizeManager()
        self.size_ui = CanvasSizeUI(self.size_manager)
        self.magic_eraser = MagicEraser()
        
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        
        if 'current_project' not in st.session_state:
            st.session_state.current_project = {
                'name': 'Untitled Project',
                'canvas_size': 'us_business_card',
                'elements': [],
                'history': [],
                'current_tool': 'select',
                'zoom_level': 100,
                'grid_enabled': True,
                'snap_enabled': True,
                'rulers_enabled': True
            }
        
        if 'ui_settings' not in st.session_state:
            st.session_state.ui_settings = {
                'theme': 'dark',
                'panel_layout': 'default',
                'toolbar_position': 'top',
                'show_properties': True,
                'show_layers': True,
                'show_history': True,
                'show_library': True
            }
        
        if 'export_settings' not in st.session_state:
            st.session_state.export_settings = {
                'format': 'PNG',
                'quality': 95,
                'dpi': 300,
                'include_bleed': False,
                'color_profile': 'sRGB'
            }
    
    @st.cache_resource
    def get_image_library(_self):
        """Get cached image library instance"""
        return ImageLibrary()
    
    def render_main_interface(self):
        """Render the main application interface"""
        
        # Apply custom CSS
        self.apply_custom_styles()
        
        # Render menu bar
        self.render_menu_bar()
        
        # Create main layout
        col_left, col_center, col_right = st.columns([2, 6, 2])
        
        with col_left:
            self.render_left_panel()
        
        with col_center:
            self.render_canvas_area()
        
        with col_right:
            self.render_right_panel()
        
        # Render status bar
        self.render_status_bar()
        
        # Render modals and dialogs
        self.render_dialogs()
    
    def apply_custom_styles(self):
        """Apply custom CSS styles"""
        
        with open('static/css/photoshop_theme.css', 'r') as f:
            css_content = f.read()
        
        st.markdown(f"""
        <style>
        {css_content}
        
        /* Additional Streamlit-specific styles */
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: none;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 32px;
            padding: 0 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 4px 4px 0 0;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--bg-secondary);
            border-bottom-color: var(--bg-secondary);
        }}
        
        .enhanced-editor {{
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_menu_bar(self):
        """Render the top menu bar"""
        
        menu_col1, menu_col2, menu_col3, menu_col4, menu_col5 = st.columns([1, 1, 1, 1, 6])
        
        with menu_col1:
            if st.button("📁 File", use_container_width=True):
                st.session_state.show_file_menu = True
        
        with menu_col2:
            if st.button("✏️ Edit", use_container_width=True):
                st.session_state.show_edit_menu = True
        
        with menu_col3:
            if st.button("👁️ View", use_container_width=True):
                st.session_state.show_view_menu = True
        
        with menu_col4:
            if st.button("🔧 Tools", use_container_width=True):
                st.session_state.show_tools_menu = True
        
        with menu_col5:
            # Project name and save status
            col_name, col_save = st.columns([4, 1])
            with col_name:
                project_name = st.text_input(
                    "Project Name", 
                    value=st.session_state.current_project['name'],
                    label_visibility="collapsed",
                    key="project_name_input"
                )
                if project_name != st.session_state.current_project['name']:
                    st.session_state.current_project['name'] = project_name
            
            with col_save:
                if st.button("💾 Save", use_container_width=True):
                    self.save_project()
    
    def render_left_panel(self):
        """Render the left panel with tools and properties"""
        
        st.markdown("### 🛠️ Tools & Properties")
        
        # Tool selection tabs
        tool_tab, props_tab, magic_tab = st.tabs(["Tools", "Properties", "Magic"])
        
        with tool_tab:
            self.render_tools_panel()
        
        with props_tab:
            self.render_properties_panel()
        
        with magic_tab:
            st.markdown(MagicEraserUI.render_magic_eraser_panel(), unsafe_allow_html=True)
    
    def render_tools_panel(self):
        """Render the tools panel"""
        
        st.markdown("#### Selection Tools")
        tool_cols = st.columns(3)
        
        with tool_cols[0]:
            if st.button("🔍", help="Select Tool", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'select'
        
        with tool_cols[1]:
            if st.button("✋", help="Move Tool", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'move'
        
        with tool_cols[2]:
            if st.button("🔄", help="Rotate Tool", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'rotate'
        
        st.markdown("#### Shape Tools")
        shape_cols = st.columns(4)
        
        with shape_cols[0]:
            if st.button("⬜", help="Rectangle", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'rectangle'
        
        with shape_cols[1]:
            if st.button("⭕", help="Circle", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'circle'
        
        with shape_cols[2]:
            if st.button("📝", help="Text", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'text'
        
        with shape_cols[3]:
            if st.button("📏", help="Line", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'line'
        
        st.markdown("#### Advanced Tools")
        adv_cols = st.columns(2)
        
        with adv_cols[0]:
            if st.button("🪄 Magic Eraser", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'magic_eraser'
        
        with adv_cols[1]:
            if st.button("🎨 Brush", use_container_width=True):
                st.session_state.current_project['current_tool'] = 'brush'
    
    def render_properties_panel(self):
        """Render the properties panel"""
        
        current_tool = st.session_state.current_project['current_tool']
        
        if current_tool in ['rectangle', 'circle']:
            st.markdown("#### Shape Properties")
            
            fill_color = st.color_picker("Fill Color", "#3498db")
            stroke_color = st.color_picker("Stroke Color", "#2c3e50")
            stroke_width = st.slider("Stroke Width", 0, 20, 2)
            opacity = st.slider("Opacity", 0, 100, 100)
            
        elif current_tool == 'text':
            st.markdown("#### Text Properties")
            
            font_family = st.selectbox("Font Family", [
                "Arial", "Helvetica", "Times New Roman", "Georgia", 
                "Verdana", "Tahoma", "Impact", "Comic Sans MS"
            ])
            font_size = st.slider("Font Size", 8, 72, 16)
            font_weight = st.selectbox("Font Weight", ["normal", "bold"])
            text_color = st.color_picker("Text Color", "#333333")
            text_align = st.selectbox("Text Align", ["left", "center", "right"])
            
        elif current_tool == 'magic_eraser':
            st.markdown("#### Magic Eraser Settings")
            
            tolerance = st.slider("Tolerance", 1, 100, 32)
            contiguous = st.checkbox("Contiguous", True)
            anti_alias = st.checkbox("Anti-alias", True)
            feather = st.slider("Feather", 0, 20, 1)
        
        # Common properties
        st.markdown("#### Canvas Settings")
        
        grid_enabled = st.checkbox(
            "Show Grid", 
            st.session_state.current_project['grid_enabled']
        )
        if grid_enabled != st.session_state.current_project['grid_enabled']:
            st.session_state.current_project['grid_enabled'] = grid_enabled
        
        snap_enabled = st.checkbox(
            "Snap to Grid", 
            st.session_state.current_project['snap_enabled']
        )
        if snap_enabled != st.session_state.current_project['snap_enabled']:
            st.session_state.current_project['snap_enabled'] = snap_enabled
        
        rulers_enabled = st.checkbox(
            "Show Rulers", 
            st.session_state.current_project['rulers_enabled']
        )
        if rulers_enabled != st.session_state.current_project['rulers_enabled']:
            st.session_state.current_project['rulers_enabled'] = rulers_enabled
    
    def render_canvas_area(self):
        """Render the main canvas area"""
        
        # Canvas toolbar
        self.render_canvas_toolbar()
        
        # Canvas size selector
        with st.expander("📐 Canvas Size", expanded=False):
            self.render_canvas_size_selector()
        
        # Main canvas
        st.markdown("### 🎨 Canvas")
        
        # Canvas container
        canvas_container = st.container()
        
        with canvas_container:
            # Render the Fabric.js canvas
            self.render_fabric_canvas()
        
        # Canvas controls
        self.render_canvas_controls()
    
    def render_canvas_toolbar(self):
        """Render the canvas toolbar"""
        
        toolbar_cols = st.columns([1, 1, 1, 1, 1, 1, 2, 1])
        
        with toolbar_cols[0]:
            if st.button("↶", help="Undo", use_container_width=True):
                self.undo_action()
        
        with toolbar_cols[1]:
            if st.button("↷", help="Redo", use_container_width=True):
                self.redo_action()
        
        with toolbar_cols[2]:
            if st.button("📋", help="Copy", use_container_width=True):
                self.copy_selection()
        
        with toolbar_cols[3]:
            if st.button("📄", help="Paste", use_container_width=True):
                self.paste_selection()
        
        with toolbar_cols[4]:
            if st.button("🗑️", help="Delete", use_container_width=True):
                self.delete_selection()
        
        with toolbar_cols[5]:
            if st.button("🔍+", help="Zoom In", use_container_width=True):
                self.zoom_in()
        
        with toolbar_cols[6]:
            zoom_level = st.slider(
                "Zoom", 
                10, 500, 
                st.session_state.current_project['zoom_level'],
                label_visibility="collapsed"
            )
            if zoom_level != st.session_state.current_project['zoom_level']:
                st.session_state.current_project['zoom_level'] = zoom_level
        
        with toolbar_cols[7]:
            if st.button("🔍-", help="Zoom Out", use_container_width=True):
                self.zoom_out()
    
    def render_canvas_size_selector(self):
        """Render canvas size selection interface"""
        
        # Category filter
        categories = self.size_manager.get_categories()
        selected_category = st.selectbox(
            "Category",
            ["All"] + [cat.replace("_", " ").title() for cat in categories]
        )
        
        # Size search
        search_query = st.text_input("Search sizes", placeholder="Type to search...")
        
        # Get sizes based on filters
        if selected_category == "All":
            available_sizes = list(self.size_manager.sizes.values())
        else:
            category_key = selected_category.lower().replace(" ", "_")
            available_sizes = self.size_manager.get_sizes_by_category(category_key)
        
        if search_query:
            available_sizes = [
                size for size in available_sizes 
                if search_query.lower() in size.name.lower()
            ]
        
        # Size selection
        if available_sizes:
            size_options = [f"{size.name} ({size.width}×{size.height})" for size in available_sizes]
            selected_size_idx = st.selectbox(
                "Canvas Size",
                range(len(size_options)),
                format_func=lambda x: size_options[x]
            )
            
            selected_size = available_sizes[selected_size_idx]
            
            # Size info
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.metric("Dimensions", f"{selected_size.width}×{selected_size.height}px")
            with col_info2:
                inches = selected_size.to_inches()
                st.metric("Print Size", f"{inches[0]:.1f}\"×{inches[1]:.1f}\"")
            
            # Apply size button
            if st.button("Apply Canvas Size", use_container_width=True):
                self.apply_canvas_size(selected_size)
                st.success(f"Canvas resized to {selected_size.name}")
        
        # Custom size option
        with st.expander("Custom Size"):
            col_w, col_h = st.columns(2)
            with col_w:
                custom_width = st.number_input("Width (px)", min_value=1, value=1050)
            with col_h:
                custom_height = st.number_input("Height (px)", min_value=1, value=600)
            
            custom_name = st.text_input("Custom Size Name", value="My Custom Size")
            
            if st.button("Create Custom Size", use_container_width=True):
                custom_size = self.size_manager.create_custom_size(
                    custom_name, custom_width, custom_height
                )
                self.apply_canvas_size(custom_size)
                st.success(f"Created and applied custom size: {custom_name}")
    
    def render_fabric_canvas(self):
        """Render the Fabric.js canvas"""
        
        current_size = self.get_current_canvas_size()
        
        canvas_html = f"""
        <div id="canvas-container" style="border: 1px solid #ccc; background: #fff; position: relative;">
            <canvas id="main-canvas" width="{current_size.width}" height="{current_size.height}"></canvas>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js"></script>
        <script>
        // Initialize Fabric.js canvas
        const canvas = new fabric.Canvas('main-canvas', {{
            backgroundColor: '#ffffff',
            selection: true,
            preserveObjectStacking: true
        }});
        
        // Set canvas size
        canvas.setDimensions({{
            width: {current_size.width},
            height: {current_size.height}
        }});
        
        // Grid settings
        const gridSize = 20;
        let gridEnabled = {str(st.session_state.current_project['grid_enabled']).lower()};
        
        function drawGrid() {{
            if (!gridEnabled) return;
            
            const ctx = canvas.getContext();
            ctx.strokeStyle = '#e0e0e0';
            ctx.lineWidth = 1;
            
            // Vertical lines
            for (let i = 0; i <= canvas.width; i += gridSize) {{
                ctx.beginPath();
                ctx.moveTo(i, 0);
                ctx.lineTo(i, canvas.height);
                ctx.stroke();
            }}
            
            // Horizontal lines
            for (let i = 0; i <= canvas.height; i += gridSize) {{
                ctx.beginPath();
                ctx.moveTo(0, i);
                ctx.lineTo(canvas.width, i);
                ctx.stroke();
            }}
        }}
        
        // Redraw grid when canvas renders
        canvas.on('after:render', drawGrid);
        
        // Tool handlers
        let currentTool = '{st.session_state.current_project['current_tool']}';
        
        function setTool(tool) {{
            currentTool = tool;
            updateCanvasCursor();
        }}
        
        function updateCanvasCursor() {{
            switch(currentTool) {{
                case 'select':
                    canvas.defaultCursor = 'default';
                    canvas.hoverCursor = 'move';
                    break;
                case 'magic_eraser':
                    canvas.defaultCursor = 'crosshair';
                    break;
                default:
                    canvas.defaultCursor = 'crosshair';
            }}
        }}
        
        // Mouse event handlers
        canvas.on('mouse:down', function(options) {{
            if (currentTool === 'magic_eraser') {{
                handleMagicEraserClick(options);
            }}
        }});
        
        function handleMagicEraserClick(options) {{
            const pointer = canvas.getPointer(options.e);
            console.log('Magic eraser clicked at:', pointer);
            // This would integrate with the Python magic eraser
        }}
        
        // Add sample elements for demonstration
        function addSampleElements() {{
            // Add a text element
            const text = new fabric.Text('Your Name', {{
                left: 50,
                top: 50,
                fontSize: 24,
                fill: '#333333',
                fontFamily: 'Arial'
            }});
            canvas.add(text);
            
            // Add a rectangle
            const rect = new fabric.Rect({{
                left: 50,
                top: 100,
                width: 200,
                height: 100,
                fill: '#3498db',
                stroke: '#2c3e50',
                strokeWidth: 2
            }});
            canvas.add(rect);
        }}
        
        // Initialize with sample elements
        addSampleElements();
        
        // History management
        let history = [];
        let historyIndex = -1;
        
        function saveToHistory() {{
            const state = JSON.stringify(canvas.toJSON());
            history = history.slice(0, historyIndex + 1);
            history.push(state);
            historyIndex = history.length - 1;
        }}
        
        function undo() {{
            if (historyIndex > 0) {{
                historyIndex--;
                canvas.loadFromJSON(history[historyIndex], canvas.renderAll.bind(canvas));
            }}
        }}
        
        function redo() {{
            if (historyIndex < history.length - 1) {{
                historyIndex++;
                canvas.loadFromJSON(history[historyIndex], canvas.renderAll.bind(canvas));
            }}
        }}
        
        // Save initial state
        saveToHistory();
        
        // Auto-save on changes
        canvas.on('object:modified', saveToHistory);
        canvas.on('object:added', saveToHistory);
        canvas.on('object:removed', saveToHistory);
        
        // Export functions
        function exportCanvas(format, quality) {{
            switch(format.toLowerCase()) {{
                case 'png':
                    return canvas.toDataURL('image/png');
                case 'jpg':
                case 'jpeg':
                    return canvas.toDataURL('image/jpeg', quality / 100);
                case 'svg':
                    return canvas.toSVG();
                default:
                    return canvas.toDataURL('image/png');
            }}
        }}
        
        // Make functions globally available
        window.canvas = canvas;
        window.setTool = setTool;
        window.undo = undo;
        window.redo = redo;
        window.exportCanvas = exportCanvas;
        window.saveToHistory = saveToHistory;
        
        console.log('Enhanced Business Card Editor initialized');
        </script>
        """
        
        st.components.v1.html(canvas_html, height=600)
    
    def render_canvas_controls(self):
        """Render canvas control buttons"""
        
        control_cols = st.columns(4)
        
        with control_cols[0]:
            if st.button("🔄 Reset Canvas", use_container_width=True):
                self.reset_canvas()
        
        with control_cols[1]:
            if st.button("📤 Export", use_container_width=True):
                self.show_export_dialog()
        
        with control_cols[2]:
            if st.button("👁️ Preview", use_container_width=True):
                self.show_preview()
        
        with control_cols[3]:
            if st.button("📱 Responsive Test", use_container_width=True):
                self.show_responsive_test()
    
    def render_right_panel(self):
        """Render the right panel with layers, history, and library"""
        
        st.markdown("### 📚 Panels")
        
        # Panel tabs
        layers_tab, history_tab, library_tab, templates_tab = st.tabs([
            "Layers", "History", "Library", "Templates"
        ])
        
        with layers_tab:
            self.render_layers_panel()
        
        with history_tab:
            self.render_history_panel()
        
        with library_tab:
            self.render_library_panel()
        
        with templates_tab:
            self.render_templates_panel()
    
    def render_layers_panel(self):
        """Render the layers panel"""
        
        st.markdown("#### 🗂️ Layers")
        
        # Layer controls
        layer_cols = st.columns(3)
        with layer_cols[0]:
            if st.button("➕", help="Add Layer", use_container_width=True):
                self.add_layer()
        with layer_cols[1]:
            if st.button("🗑️", help="Delete Layer", use_container_width=True):
                self.delete_layer()
        with layer_cols[2]:
            if st.button("📋", help="Duplicate Layer", use_container_width=True):
                self.duplicate_layer()
        
        # Layer list (placeholder)
        layers = [
            {"name": "Background", "visible": True, "locked": False},
            {"name": "Text Layer", "visible": True, "locked": False},
            {"name": "Shape Layer", "visible": True, "locked": False}
        ]
        
        for i, layer in enumerate(layers):
            layer_col1, layer_col2, layer_col3, layer_col4 = st.columns([3, 1, 1, 1])
            
            with layer_col1:
                st.text(layer["name"])
            
            with layer_col2:
                visible = st.checkbox("👁️", value=layer["visible"], key=f"layer_vis_{i}", label_visibility="collapsed")
            
            with layer_col3:
                locked = st.checkbox("🔒", value=layer["locked"], key=f"layer_lock_{i}", label_visibility="collapsed")
            
            with layer_col4:
                if st.button("⚙️", key=f"layer_settings_{i}", help="Layer Settings"):
                    st.session_state[f"show_layer_settings_{i}"] = True
    
    def render_history_panel(self):
        """Render the history panel"""
        
        st.markdown("#### 📜 History")
        
        # History controls
        hist_cols = st.columns(2)
        with hist_cols[0]:
            if st.button("↶ Undo", use_container_width=True):
                self.undo_action()
        with hist_cols[1]:
            if st.button("↷ Redo", use_container_width=True):
                self.redo_action()
        
        # History list (placeholder)
        history_items = [
            "Canvas Created",
            "Text Added",
            "Rectangle Added", 
            "Object Moved",
            "Color Changed"
        ]
        
        for i, item in enumerate(history_items):
            if st.button(f"{len(history_items)-i}. {item}", key=f"history_{i}", use_container_width=True):
                self.restore_history_state(i)
    
    def render_library_panel(self):
        """Render the image library panel"""
        
        st.markdown("#### 📁 Image Library")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload Images",
            type=['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'],
            accept_multiple_files=True,
            key="library_uploader"
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                image_id = self.image_library.add_image(
                    file_bytes,
                    uploaded_file.name,
                    category="uploads",
                    tags=["uploaded"],
                    description=f"Uploaded: {uploaded_file.name}"
                )
                if image_id:
                    st.success(f"Added {uploaded_file.name}")
        
        # Search and filter
        search_query = st.text_input("Search images", key="library_search")
        category_filter = st.selectbox(
            "Category", 
            ["All"] + list(self.image_library.categories.keys()),
            key="library_category"
        )
        
        # Get and display images
        category = None if category_filter == "All" else category_filter
        images = self.image_library.search_images(
            query=search_query,
            category=category,
            limit=20
        )
        
        if images:
            # Display images in grid
            for i in range(0, len(images), 2):
                cols = st.columns(2)
                for j, col in enumerate(cols):
                    if i + j < len(images):
                        image = images[i + j]
                        with col:
                            # Display thumbnail
                            thumbnail_data = self.image_library.get_thumbnail_data(image['id'])
                            if thumbnail_data:
                                st.image(thumbnail_data, caption=image['filename'], use_column_width=True)
                                
                                # Action buttons
                                btn_cols = st.columns(2)
                                with btn_cols[0]:
                                    if st.button("Use", key=f"use_{image['id']}", use_container_width=True):
                                        self.add_image_to_canvas(image['id'])
                                with btn_cols[1]:
                                    if st.button("❤️", key=f"fav_{image['id']}", use_container_width=True):
                                        self.image_library.toggle_favorite(image['id'])
                                        st.rerun()
        else:
            st.info("No images found. Upload some images to get started!")
    
    def render_templates_panel(self):
        """Render the templates panel"""
        
        st.markdown("#### 📋 Templates")
        
        # Template categories
        template_categories = [
            "Business Cards",
            "Social Media", 
            "Print Materials",
            "Web Graphics"
        ]
        
        selected_template_category = st.selectbox(
            "Template Category",
            template_categories,
            key="template_category"
        )
        
        # Template grid (placeholder)
        templates = [
            {"name": "Classic Business Card", "preview": "🏢"},
            {"name": "Modern Business Card", "preview": "🎨"},
            {"name": "Creative Business Card", "preview": "✨"},
            {"name": "Minimal Business Card", "preview": "⚪"}
        ]
        
        for i in range(0, len(templates), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(templates):
                    template = templates[i + j]
                    with col:
                        st.markdown(f"""
                        <div style="border: 1px solid #ccc; padding: 10px; text-align: center; border-radius: 4px;">
                            <div style="font-size: 24px; margin-bottom: 5px;">{template['preview']}</div>
                            <div style="font-size: 12px;">{template['name']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("Apply", key=f"template_{i+j}", use_container_width=True):
                            self.apply_template(template['name'])
    
    def render_status_bar(self):
        """Render the bottom status bar"""
        
        st.markdown("---")
        
        status_cols = st.columns([2, 1, 1, 1, 1, 2])
        
        with status_cols[0]:
            current_size = self.get_current_canvas_size()
            st.text(f"Canvas: {current_size.name} ({current_size.width}×{current_size.height})")
        
        with status_cols[1]:
            st.text(f"Tool: {st.session_state.current_project['current_tool'].title()}")
        
        with status_cols[2]:
            st.text(f"Zoom: {st.session_state.current_project['zoom_level']}%")
        
        with status_cols[3]:
            elements_count = len(st.session_state.current_project['elements'])
            st.text(f"Elements: {elements_count}")
        
        with status_cols[4]:
            st.text("Ready")
        
        with status_cols[5]:
            st.text(f"Project: {st.session_state.current_project['name']}")
    
    def render_dialogs(self):
        """Render modal dialogs"""
        
        # Export dialog
        if st.session_state.get('show_export_dialog', False):
            self.render_export_dialog()
        
        # Settings dialog
        if st.session_state.get('show_settings_dialog', False):
            self.render_settings_dialog()
    
    def render_export_dialog(self):
        """Render the export dialog"""
        
        with st.expander("📤 Export Settings", expanded=True):
            
            export_cols = st.columns(2)
            
            with export_cols[0]:
                export_format = st.selectbox(
                    "Format",
                    ["PNG", "JPG", "PDF", "SVG"],
                    index=0
                )
                
                if export_format in ["PNG", "JPG"]:
                    quality = st.slider("Quality", 10, 100, 95)
                    dpi = st.selectbox("DPI", [72, 150, 300, 600], index=2)
                
                include_bleed = st.checkbox("Include Bleed Area", False)
            
            with export_cols[1]:
                color_profile = st.selectbox(
                    "Color Profile",
                    ["sRGB", "Adobe RGB", "CMYK"],
                    index=0
                )
                
                transparent_bg = st.checkbox("Transparent Background", False)
                
                if export_format == "PDF":
                    pdf_preset = st.selectbox(
                        "PDF Preset",
                        ["Print Quality", "Web Quality", "Smallest File"],
                        index=0
                    )
            
            # Export buttons
            export_btn_cols = st.columns(3)
            
            with export_btn_cols[0]:
                if st.button("📥 Download", use_container_width=True):
                    self.export_and_download(export_format, quality if 'quality' in locals() else 95)
            
            with export_btn_cols[1]:
                if st.button("👁️ Preview", use_container_width=True):
                    self.show_export_preview(export_format)
            
            with export_btn_cols[2]:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_export_dialog = False
                    st.rerun()
    
    # Helper methods
    def get_current_canvas_size(self):
        """Get the current canvas size object"""
        size_name = st.session_state.current_project['canvas_size']
        return self.size_manager.get_size(size_name) or self.size_manager.get_size('us_business_card')
    
    def apply_canvas_size(self, canvas_size):
        """Apply a new canvas size"""
        st.session_state.current_project['canvas_size'] = canvas_size.name.lower().replace(" ", "_")
    
    def save_project(self):
        """Save the current project"""
        project_data = st.session_state.current_project.copy()
        # In a real implementation, this would save to a database or file
        st.success("Project saved successfully!")
    
    def undo_action(self):
        """Undo the last action"""
        # This would integrate with the canvas history
        st.info("Undo action performed")
    
    def redo_action(self):
        """Redo the last undone action"""
        # This would integrate with the canvas history
        st.info("Redo action performed")
    
    def zoom_in(self):
        """Zoom in on the canvas"""
        current_zoom = st.session_state.current_project['zoom_level']
        new_zoom = min(500, current_zoom + 25)
        st.session_state.current_project['zoom_level'] = new_zoom
    
    def zoom_out(self):
        """Zoom out on the canvas"""
        current_zoom = st.session_state.current_project['zoom_level']
        new_zoom = max(10, current_zoom - 25)
        st.session_state.current_project['zoom_level'] = new_zoom
    
    def add_image_to_canvas(self, image_id):
        """Add an image from the library to the canvas"""
        # This would integrate with the canvas to add the image
        self.image_library.update_image_usage(image_id)
        st.success("Image added to canvas!")
    
    def apply_template(self, template_name):
        """Apply a template to the canvas"""
        template = self.size_manager.get_template(template_name.lower().replace(" ", "_"))
        if template:
            # This would apply the template to the canvas
            st.success(f"Applied template: {template_name}")
        else:
            st.error("Template not found")
    
    def export_and_download(self, format, quality):
        """Export and download the canvas"""
        # This would integrate with the canvas export functionality
        st.success(f"Exporting as {format} with {quality}% quality...")
    
    def show_export_dialog(self):
        """Show the export dialog"""
        st.session_state.show_export_dialog = True
    
    def reset_canvas(self):
        """Reset the canvas to empty state"""
        st.session_state.current_project['elements'] = []
        st.success("Canvas reset!")
    
    def show_preview(self):
        """Show canvas preview"""
        st.info("Preview mode activated")
    
    def show_responsive_test(self):
        """Show responsive design test"""
        st.info("Testing responsive design...")
    
    # Additional helper methods for layer management
    def add_layer(self):
        """Add a new layer"""
        st.info("New layer added")
    
    def delete_layer(self):
        """Delete the selected layer"""
        st.info("Layer deleted")
    
    def duplicate_layer(self):
        """Duplicate the selected layer"""
        st.info("Layer duplicated")
    
    def copy_selection(self):
        """Copy the selected elements"""
        st.info("Selection copied")
    
    def paste_selection(self):
        """Paste the copied elements"""
        st.info("Selection pasted")
    
    def delete_selection(self):
        """Delete the selected elements"""
        st.info("Selection deleted")
    
    def restore_history_state(self, index):
        """Restore a specific history state"""
        st.info(f"Restored to history state {index}")


def main():
    """Main application entry point"""
    
    # Initialize the application
    app = EnhancedBusinessCardEditor()
    
    # Render the main interface
    app.render_main_interface()
    
    # Add footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
        Enhanced Business Card Editor v2.0 | 
        🎨 Professional Design Tool with Advanced Features | 
        Built with Streamlit & Fabric.js
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


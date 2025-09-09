"""
UI Components for Enhanced Business Card Editor
Provides reusable Streamlit components with Photoshop-like styling
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import List, Dict, Any, Optional, Tuple
import json

class PhotoshopUI:
    """Main UI component that creates the Photoshop-like interface"""
    
    @staticmethod
    def render_main_interface(canvas_config: Dict[str, Any]) -> str:
        """Render the main Photoshop-like interface"""
        
        # Load CSS
        with open('static/css/photoshop_theme.css', 'r') as f:
            css = f.read()
        
        # Generate the HTML interface
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Enhanced Business Card Editor</title>
            <style>{css}</style>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jscolor/2.5.1/jscolor.min.js"></script>
        </head>
        <body>
            <div class="app-container">
                {PhotoshopUI._render_menu_bar()}
                {PhotoshopUI._render_toolbar()}
                
                <div class="main-content">
                    {PhotoshopUI._render_left_panel()}
                    {PhotoshopUI._render_canvas_area(canvas_config)}
                    {PhotoshopUI._render_right_panel()}
                </div>
                
                {PhotoshopUI._render_status_bar()}
            </div>
            
            <script>
                {PhotoshopUI._render_javascript(canvas_config)}
            </script>
        </body>
        </html>
        """
        
        return html
    
    @staticmethod
    def _render_menu_bar() -> str:
        """Render the top menu bar"""
        return """
        <div class="menu-bar">
            <div class="menu-item" onclick="showFileMenu()">File</div>
            <div class="menu-item" onclick="showEditMenu()">Edit</div>
            <div class="menu-item" onclick="showImageMenu()">Image</div>
            <div class="menu-item" onclick="showLayerMenu()">Layer</div>
            <div class="menu-item" onclick="showSelectMenu()">Select</div>
            <div class="menu-item" onclick="showFilterMenu()">Filter</div>
            <div class="menu-item" onclick="showViewMenu()">View</div>
            <div class="menu-item" onclick="showHelpMenu()">Help</div>
        </div>
        """
    
    @staticmethod
    def _render_toolbar() -> str:
        """Render the main toolbar"""
        return """
        <div class="toolbar">
            <!-- File Operations -->
            <div class="toolbar-group">
                <button class="tool-button large" onclick="newDocument()" title="New">📄 New</button>
                <button class="tool-button large" onclick="openDocument()" title="Open">📁 Open</button>
                <button class="tool-button large" onclick="saveDocument()" title="Save">💾 Save</button>
            </div>
            
            <div class="toolbar-separator"></div>
            
            <!-- Edit Operations -->
            <div class="toolbar-group">
                <button class="tool-button" onclick="undo()" title="Undo">↶</button>
                <button class="tool-button" onclick="redo()" title="Redo">↷</button>
                <button class="tool-button" onclick="copy()" title="Copy">📋</button>
                <button class="tool-button" onclick="paste()" title="Paste">📋</button>
            </div>
            
            <div class="toolbar-separator"></div>
            
            <!-- Transform Operations -->
            <div class="toolbar-group">
                <button class="tool-button" onclick="flipHorizontal()" title="Flip Horizontal">⇄</button>
                <button class="tool-button" onclick="flipVertical()" title="Flip Vertical">⇅</button>
                <button class="tool-button" onclick="rotateLeft()" title="Rotate Left">↺</button>
                <button class="tool-button" onclick="rotateRight()" title="Rotate Right">↻</button>
            </div>
            
            <div class="toolbar-separator"></div>
            
            <!-- Zoom Controls -->
            <div class="toolbar-group">
                <button class="tool-button" onclick="zoomIn()" title="Zoom In">🔍+</button>
                <button class="tool-button" onclick="zoomOut()" title="Zoom Out">🔍-</button>
                <button class="tool-button" onclick="zoomFit()" title="Fit to Window">⬜</button>
                <span class="zoom-display" id="zoom-display">100%</span>
            </div>
            
            <div class="toolbar-separator"></div>
            
            <!-- Export -->
            <div class="toolbar-group">
                <button class="tool-button large" onclick="exportImage()" title="Export">📤 Export</button>
                <button class="tool-button large" onclick="printDocument()" title="Print">🖨️ Print</button>
            </div>
        </div>
        """
    
    @staticmethod
    def _render_left_panel() -> str:
        """Render the left panel with tools and properties"""
        return """
        <div class="left-panel">
            <!-- Toolbox -->
            <div class="toolbox">
                <div class="tool-grid">
                    <div class="tool-option active" onclick="selectTool('select')" title="Selection Tool">
                        <div>🔲</div>
                        <div>Select</div>
                    </div>
                    <div class="tool-option" onclick="selectTool('move')" title="Move Tool">
                        <div>✋</div>
                        <div>Move</div>
                    </div>
                    <div class="tool-option" onclick="selectTool('brush')" title="Brush Tool">
                        <div>🖌️</div>
                        <div>Brush</div>
                    </div>
                    <div class="tool-option" onclick="selectTool('eraser')" title="Eraser Tool">
                        <div>🧽</div>
                        <div>Eraser</div>
                    </div>
                    <div class="tool-option" onclick="selectTool('magic-eraser')" title="Magic Eraser">
                        <div>✨</div>
                        <div>Magic</div>
                    </div>
                    <div class="tool-option" onclick="selectTool('text')" title="Text Tool">
                        <div>📝</div>
                        <div>Text</div>
                    </div>
                    <div class="tool-option" onclick="selectTool('shape')" title="Shape Tool">
                        <div>⬜</div>
                        <div>Shape</div>
                    </div>
                    <div class="tool-option" onclick="selectTool('eyedropper')" title="Eyedropper">
                        <div>💧</div>
                        <div>Color</div>
                    </div>
                </div>
            </div>
            
            <!-- Properties Panel -->
            <div class="properties-panel">
                <div class="property-group">
                    <div class="property-header" onclick="togglePropertyGroup(this)">
                        <span>🎨 Tool Options</span>
                        <span>▼</span>
                    </div>
                    <div class="property-content" id="tool-options">
                        <div class="property-row">
                            <span class="property-label">Size:</span>
                            <input type="range" class="property-input" id="brush-size" min="1" max="100" value="10">
                            <span id="brush-size-value">10px</span>
                        </div>
                        <div class="property-row">
                            <span class="property-label">Opacity:</span>
                            <input type="range" class="property-input" id="brush-opacity" min="0" max="100" value="100">
                            <span id="brush-opacity-value">100%</span>
                        </div>
                        <div class="property-row">
                            <span class="property-label">Hardness:</span>
                            <input type="range" class="property-input" id="brush-hardness" min="0" max="100" value="100">
                            <span id="brush-hardness-value">100%</span>
                        </div>
                    </div>
                </div>
                
                <div class="property-group">
                    <div class="property-header" onclick="togglePropertyGroup(this)">
                        <span>🎯 Transform</span>
                        <span>▼</span>
                    </div>
                    <div class="property-content" id="transform-options">
                        <div class="property-row">
                            <span class="property-label">X:</span>
                            <input type="number" class="property-input" id="object-x" value="0">
                        </div>
                        <div class="property-row">
                            <span class="property-label">Y:</span>
                            <input type="number" class="property-input" id="object-y" value="0">
                        </div>
                        <div class="property-row">
                            <span class="property-label">Width:</span>
                            <input type="number" class="property-input" id="object-width" value="100">
                        </div>
                        <div class="property-row">
                            <span class="property-label">Height:</span>
                            <input type="number" class="property-input" id="object-height" value="100">
                        </div>
                        <div class="property-row">
                            <span class="property-label">Rotation:</span>
                            <input type="number" class="property-input" id="object-rotation" value="0" min="0" max="360">
                        </div>
                    </div>
                </div>
                
                <div class="property-group">
                    <div class="property-header" onclick="togglePropertyGroup(this)">
                        <span>🌈 Colors</span>
                        <span>▼</span>
                    </div>
                    <div class="property-content" id="color-options">
                        <div class="property-row">
                            <span class="property-label">Foreground:</span>
                            <div class="color-picker">
                                <div class="color-swatch" id="fg-color" style="background: #000000;" onclick="pickColor('fg')"></div>
                            </div>
                        </div>
                        <div class="property-row">
                            <span class="property-label">Background:</span>
                            <div class="color-picker">
                                <div class="color-swatch" id="bg-color" style="background: #ffffff;" onclick="pickColor('bg')"></div>
                            </div>
                        </div>
                        <div class="property-row">
                            <button class="tool-button large" onclick="swapColors()">⇄ Swap</button>
                            <button class="tool-button large" onclick="resetColors()">⚫⚪ Reset</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def _render_canvas_area(canvas_config: Dict[str, Any]) -> str:
        """Render the main canvas area"""
        return f"""
        <div class="canvas-area">
            <div class="canvas-container" id="canvas-container">
                <div class="canvas-rulers">
                    <div class="ruler-horizontal" id="ruler-h"></div>
                    <div class="ruler-vertical" id="ruler-v"></div>
                </div>
                <canvas id="main-canvas" 
                        width="{canvas_config.get('width', 1050)}" 
                        height="{canvas_config.get('height', 600)}">
                </canvas>
            </div>
        </div>
        """
    
    @staticmethod
    def _render_right_panel() -> str:
        """Render the right panel with layers, history, and library"""
        return """
        <div class="right-panel">
            <div class="panel-tabs">
                <div class="panel-tab active" onclick="showPanel('layers')">Layers</div>
                <div class="panel-tab" onclick="showPanel('history')">History</div>
                <div class="panel-tab" onclick="showPanel('library')">Library</div>
            </div>
            
            <div class="panel-content">
                <!-- Layers Panel -->
                <div id="layers-panel" class="layers-panel">
                    <div class="layer-controls mb-2">
                        <button class="tool-button" onclick="addLayer()" title="Add Layer">➕</button>
                        <button class="tool-button" onclick="deleteLayer()" title="Delete Layer">🗑️</button>
                        <button class="tool-button" onclick="duplicateLayer()" title="Duplicate Layer">📋</button>
                        <button class="tool-button" onclick="mergeDown()" title="Merge Down">⬇️</button>
                    </div>
                    
                    <div id="layer-list">
                        <div class="layer-item active">
                            <div class="layer-thumbnail"></div>
                            <div class="layer-name">Background</div>
                            <div class="layer-controls">
                                <button class="layer-control" onclick="toggleLayerVisibility(this)" title="Toggle Visibility">👁</button>
                                <button class="layer-control" onclick="lockLayer(this)" title="Lock Layer">🔓</button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- History Panel -->
                <div id="history-panel" class="history-panel hidden">
                    <div id="history-list">
                        <div class="history-item active">New Document</div>
                    </div>
                </div>
                
                <!-- Library Panel -->
                <div id="library-panel" class="library-panel hidden">
                    <input type="text" class="library-search" placeholder="Search images..." id="library-search">
                    
                    <div class="library-categories">
                        <div class="library-category active" onclick="filterLibrary('all')">All</div>
                        <div class="library-category" onclick="filterLibrary('business')">Business</div>
                        <div class="library-category" onclick="filterLibrary('icons')">Icons</div>
                        <div class="library-category" onclick="filterLibrary('backgrounds')">Backgrounds</div>
                        <div class="library-category" onclick="filterLibrary('textures')">Textures</div>
                    </div>
                    
                    <div class="library-grid" id="library-grid">
                        <!-- Library items will be populated here -->
                    </div>
                    
                    <div class="library-upload mt-3">
                        <input type="file" id="library-upload" multiple accept="image/*" style="display: none;">
                        <button class="tool-button large" onclick="document.getElementById('library-upload').click()">
                            📁 Upload Images
                        </button>
                    </div>
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def _render_status_bar() -> str:
        """Render the bottom status bar"""
        return """
        <div class="status-bar">
            <div class="status-left">
                <span id="status-message">Ready</span>
                <span>•</span>
                <span id="canvas-info">Canvas: 1050 × 600 px</span>
                <span>•</span>
                <span id="color-mode">RGB</span>
                <span>•</span>
                <span id="resolution">300 DPI</span>
            </div>
            <div class="status-right">
                <span id="memory-usage">Memory: 45.2 MB</span>
                <span>•</span>
                <span id="mouse-position">0, 0</span>
                <span>•</span>
                <span id="selection-info">No selection</span>
            </div>
        </div>
        """
    
    @staticmethod
    def _render_javascript(canvas_config: Dict[str, Any]) -> str:
        """Render the main JavaScript functionality"""
        return f"""
        // Enhanced Business Card Editor - Main JavaScript
        
        // Global variables
        let canvas;
        let currentTool = 'select';
        let currentLayer = null;
        let layers = [];
        let history = [];
        let historyIndex = -1;
        let isDrawing = false;
        let lastPoint = null;
        
        // Canvas configuration
        const canvasConfig = {json.dumps(canvas_config)};
        
        // Initialize the application
        function initializeApp() {{
            // Initialize Fabric.js canvas
            canvas = new fabric.Canvas('main-canvas', {{
                backgroundColor: '#ffffff',
                selection: true,
                preserveObjectStacking: true
            }});
            
            // Set up event listeners
            setupEventListeners();
            
            // Initialize panels
            initializePanels();
            
            // Create initial layer
            createInitialLayer();
            
            // Update status bar
            updateStatusBar();
            
            console.log('Enhanced Business Card Editor initialized');
        }}
        
        // Set up event listeners
        function setupEventListeners() {{
            // Canvas events
            canvas.on('mouse:down', onMouseDown);
            canvas.on('mouse:move', onMouseMove);
            canvas.on('mouse:up', onMouseUp);
            canvas.on('object:added', onObjectAdded);
            canvas.on('object:removed', onObjectRemoved);
            canvas.on('selection:created', onSelectionCreated);
            canvas.on('selection:updated', onSelectionUpdated);
            canvas.on('selection:cleared', onSelectionCleared);
            
            // Keyboard shortcuts
            document.addEventListener('keydown', handleKeyboardShortcuts);
            
            // Property inputs
            document.getElementById('brush-size').addEventListener('input', updateBrushSize);
            document.getElementById('brush-opacity').addEventListener('input', updateBrushOpacity);
            document.getElementById('brush-hardness').addEventListener('input', updateBrushHardness);
            
            // Transform inputs
            document.getElementById('object-x').addEventListener('input', updateObjectPosition);
            document.getElementById('object-y').addEventListener('input', updateObjectPosition);
            document.getElementById('object-width').addEventListener('input', updateObjectSize);
            document.getElementById('object-height').addEventListener('input', updateObjectSize);
            document.getElementById('object-rotation').addEventListener('input', updateObjectRotation);
            
            // Library upload
            document.getElementById('library-upload').addEventListener('change', handleLibraryUpload);
            document.getElementById('library-search').addEventListener('input', searchLibrary);
        }}
        
        // Tool selection
        function selectTool(tool) {{
            currentTool = tool;
            
            // Update UI
            document.querySelectorAll('.tool-option').forEach(el => el.classList.remove('active'));
            document.querySelector(`[onclick="selectTool('${{tool}}')"]`).classList.add('active');
            
            // Update cursor
            updateCanvasCursor();
            
            // Update tool options panel
            updateToolOptions();
            
            console.log('Selected tool:', tool);
        }}
        
        // Update canvas cursor based on current tool
        function updateCanvasCursor() {{
            const cursors = {{
                'select': 'default',
                'move': 'move',
                'brush': 'crosshair',
                'eraser': 'crosshair',
                'magic-eraser': 'crosshair',
                'text': 'text',
                'shape': 'crosshair',
                'eyedropper': 'crosshair'
            }};
            
            canvas.defaultCursor = cursors[currentTool] || 'default';
        }}
        
        // Mouse event handlers
        function onMouseDown(event) {{
            const pointer = canvas.getPointer(event.e);
            lastPoint = pointer;
            isDrawing = true;
            
            switch(currentTool) {{
                case 'brush':
                    startBrush(pointer);
                    break;
                case 'eraser':
                    startEraser(pointer);
                    break;
                case 'magic-eraser':
                    useMagicEraser(pointer);
                    break;
                case 'text':
                    addText(pointer);
                    break;
                case 'shape':
                    startShape(pointer);
                    break;
                case 'eyedropper':
                    pickColorFromCanvas(pointer);
                    break;
            }}
        }}
        
        function onMouseMove(event) {{
            const pointer = canvas.getPointer(event.e);
            
            // Update mouse position in status bar
            document.getElementById('mouse-position').textContent = `${{Math.round(pointer.x)}}, ${{Math.round(pointer.y)}}`;
            
            if (!isDrawing) return;
            
            switch(currentTool) {{
                case 'brush':
                    continueBrush(pointer);
                    break;
                case 'eraser':
                    continueEraser(pointer);
                    break;
            }}
            
            lastPoint = pointer;
        }}
        
        function onMouseUp(event) {{
            isDrawing = false;
            
            switch(currentTool) {{
                case 'brush':
                case 'eraser':
                    finishDrawing();
                    break;
            }}
        }}
        
        // Drawing tools implementation
        function startBrush(point) {{
            // Implementation for brush tool
            console.log('Starting brush at', point);
        }}
        
        function continueBrush(point) {{
            // Implementation for brush continuation
        }}
        
        function startEraser(point) {{
            // Implementation for eraser tool
            console.log('Starting eraser at', point);
        }}
        
        function continueEraser(point) {{
            // Implementation for eraser continuation
        }}
        
        function useMagicEraser(point) {{
            // Implementation for magic eraser
            console.log('Using magic eraser at', point);
            // This would integrate with AI-powered background removal
        }}
        
        function finishDrawing() {{
            // Save state to history
            saveToHistory();
        }}
        
        // Text tool
        function addText(point) {{
            const text = new fabric.IText('Click to edit text', {{
                left: point.x,
                top: point.y,
                fontSize: 24,
                fill: document.getElementById('fg-color').style.backgroundColor || '#000000',
                fontFamily: 'Arial'
            }});
            
            canvas.add(text);
            canvas.setActiveObject(text);
            text.enterEditing();
        }}
        
        // Shape tools
        function startShape(point) {{
            // Add rectangle shape (can be extended for other shapes)
            const rect = new fabric.Rect({{
                left: point.x,
                top: point.y,
                width: 100,
                height: 100,
                fill: document.getElementById('fg-color').style.backgroundColor || '#000000',
                stroke: document.getElementById('bg-color').style.backgroundColor || '#ffffff',
                strokeWidth: 2
            }});
            
            canvas.add(rect);
            canvas.setActiveObject(rect);
        }}
        
        // Color picker
        function pickColorFromCanvas(point) {{
            // Get pixel color at point
            const ctx = canvas.getContext('2d');
            const imageData = ctx.getImageData(point.x, point.y, 1, 1);
            const pixel = imageData.data;
            
            const color = `rgb(${{pixel[0]}}, ${{pixel[1]}}, ${{pixel[2]}})`;
            document.getElementById('fg-color').style.backgroundColor = color;
        }}
        
        // Panel management
        function showPanel(panelName) {{
            // Hide all panels
            document.querySelectorAll('.panel-content > div').forEach(panel => {{
                panel.classList.add('hidden');
            }});
            
            // Show selected panel
            document.getElementById(panelName + '-panel').classList.remove('hidden');
            
            // Update tab states
            document.querySelectorAll('.panel-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            event.target.classList.add('active');
        }}
        
        // Layer management
        function addLayer() {{
            const layerName = `Layer ${{layers.length + 1}}`;
            const layer = {{
                name: layerName,
                visible: true,
                locked: false,
                objects: []
            }};
            
            layers.push(layer);
            updateLayerPanel();
            saveToHistory();
        }}
        
        function deleteLayer() {{
            if (layers.length <= 1) return; // Keep at least one layer
            
            const activeLayerIndex = layers.findIndex(layer => layer.active);
            if (activeLayerIndex !== -1) {{
                layers.splice(activeLayerIndex, 1);
                updateLayerPanel();
                saveToHistory();
            }}
        }}
        
        function duplicateLayer() {{
            const activeLayer = layers.find(layer => layer.active);
            if (activeLayer) {{
                const duplicatedLayer = JSON.parse(JSON.stringify(activeLayer));
                duplicatedLayer.name += ' copy';
                layers.push(duplicatedLayer);
                updateLayerPanel();
                saveToHistory();
            }}
        }}
        
        function updateLayerPanel() {{
            const layerList = document.getElementById('layer-list');
            layerList.innerHTML = '';
            
            layers.forEach((layer, index) => {{
                const layerElement = document.createElement('div');
                layerElement.className = `layer-item ${{layer.active ? 'active' : ''}}`;
                layerElement.innerHTML = `
                    <div class="layer-thumbnail"></div>
                    <div class="layer-name">${{layer.name}}</div>
                    <div class="layer-controls">
                        <button class="layer-control" onclick="toggleLayerVisibility(${{index}})" title="Toggle Visibility">
                            ${{layer.visible ? '👁' : '👁‍🗨'}}
                        </button>
                        <button class="layer-control" onclick="lockLayer(${{index}})" title="Lock Layer">
                            ${{layer.locked ? '🔒' : '🔓'}}
                        </button>
                    </div>
                `;
                
                layerElement.onclick = () => selectLayer(index);
                layerList.appendChild(layerElement);
            }});
        }}
        
        function selectLayer(index) {{
            layers.forEach(layer => layer.active = false);
            layers[index].active = true;
            updateLayerPanel();
        }}
        
        function toggleLayerVisibility(index) {{
            layers[index].visible = !layers[index].visible;
            updateLayerPanel();
            // Update canvas visibility
        }}
        
        function lockLayer(index) {{
            layers[index].locked = !layers[index].locked;
            updateLayerPanel();
        }}
        
        // History management
        function saveToHistory() {{
            const state = canvas.toJSON();
            history = history.slice(0, historyIndex + 1);
            history.push(state);
            historyIndex = history.length - 1;
            
            updateHistoryPanel();
        }}
        
        function updateHistoryPanel() {{
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = '';
            
            history.forEach((state, index) => {{
                const historyItem = document.createElement('div');
                historyItem.className = `history-item ${{index === historyIndex ? 'active' : ''}}`;
                historyItem.textContent = `Step ${{index + 1}}`;
                historyItem.onclick = () => restoreFromHistory(index);
                historyList.appendChild(historyItem);
            }});
        }}
        
        function restoreFromHistory(index) {{
            if (index >= 0 && index < history.length) {{
                historyIndex = index;
                canvas.loadFromJSON(history[index], () => {{
                    canvas.renderAll();
                    updateHistoryPanel();
                }});
            }}
        }}
        
        // Library management
        function handleLibraryUpload(event) {{
            const files = Array.from(event.target.files);
            files.forEach(file => {{
                if (file.type.startsWith('image/')) {{
                    const reader = new FileReader();
                    reader.onload = (e) => {{
                        addToLibrary(e.target.result, file.name);
                    }};
                    reader.readAsDataURL(file);
                }}
            }});
        }}
        
        function addToLibrary(imageData, name) {{
            const libraryGrid = document.getElementById('library-grid');
            const item = document.createElement('div');
            item.className = 'library-item';
            item.innerHTML = `<img src="${{imageData}}" alt="${{name}}" title="${{name}}">`;
            item.onclick = () => addImageToCanvas(imageData);
            libraryGrid.appendChild(item);
        }}
        
        function addImageToCanvas(imageData) {{
            fabric.Image.fromURL(imageData, (img) => {{
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
        
        function searchLibrary() {{
            const searchTerm = document.getElementById('library-search').value.toLowerCase();
            const items = document.querySelectorAll('.library-item');
            
            items.forEach(item => {{
                const title = item.querySelector('img').title.toLowerCase();
                item.style.display = title.includes(searchTerm) ? 'block' : 'none';
            }});
        }}
        
        function filterLibrary(category) {{
            // Update active category
            document.querySelectorAll('.library-category').forEach(cat => {{
                cat.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Filter items (implementation depends on categorization system)
            console.log('Filtering library by category:', category);
        }}
        
        // Utility functions
        function updateStatusBar() {{
            document.getElementById('canvas-info').textContent = 
                `Canvas: ${{canvas.width}} × ${{canvas.height}} px`;
        }}
        
        function updateToolOptions() {{
            // Update tool options panel based on current tool
            const toolOptions = document.getElementById('tool-options');
            // Implementation depends on selected tool
        }}
        
        function updateBrushSize() {{
            const size = document.getElementById('brush-size').value;
            document.getElementById('brush-size-value').textContent = size + 'px';
        }}
        
        function updateBrushOpacity() {{
            const opacity = document.getElementById('brush-opacity').value;
            document.getElementById('brush-opacity-value').textContent = opacity + '%';
        }}
        
        function updateBrushHardness() {{
            const hardness = document.getElementById('brush-hardness').value;
            document.getElementById('brush-hardness-value').textContent = hardness + '%';
        }}
        
        function updateObjectPosition() {{
            const obj = canvas.getActiveObject();
            if (obj) {{
                obj.set({{
                    left: parseInt(document.getElementById('object-x').value),
                    top: parseInt(document.getElementById('object-y').value)
                }});
                canvas.renderAll();
            }}
        }}
        
        function updateObjectSize() {{
            const obj = canvas.getActiveObject();
            if (obj) {{
                const width = parseInt(document.getElementById('object-width').value);
                const height = parseInt(document.getElementById('object-height').value);
                obj.set({{
                    scaleX: width / obj.width,
                    scaleY: height / obj.height
                }});
                canvas.renderAll();
            }}
        }}
        
        function updateObjectRotation() {{
            const obj = canvas.getActiveObject();
            if (obj) {{
                obj.set('angle', parseInt(document.getElementById('object-rotation').value));
                canvas.renderAll();
            }}
        }}
        
        // Object event handlers
        function onObjectAdded(event) {{
            updateLayerPanel();
            saveToHistory();
        }}
        
        function onObjectRemoved(event) {{
            updateLayerPanel();
            saveToHistory();
        }}
        
        function onSelectionCreated(event) {{
            updatePropertiesForSelection();
        }}
        
        function onSelectionUpdated(event) {{
            updatePropertiesForSelection();
        }}
        
        function onSelectionCleared(event) {{
            clearProperties();
        }}
        
        function updatePropertiesForSelection() {{
            const obj = canvas.getActiveObject();
            if (obj) {{
                document.getElementById('object-x').value = Math.round(obj.left);
                document.getElementById('object-y').value = Math.round(obj.top);
                document.getElementById('object-width').value = Math.round(obj.width * obj.scaleX);
                document.getElementById('object-height').value = Math.round(obj.height * obj.scaleY);
                document.getElementById('object-rotation').value = Math.round(obj.angle);
            }}
        }}
        
        function clearProperties() {{
            document.getElementById('object-x').value = 0;
            document.getElementById('object-y').value = 0;
            document.getElementById('object-width').value = 100;
            document.getElementById('object-height').value = 100;
            document.getElementById('object-rotation').value = 0;
        }}
        
        // Keyboard shortcuts
        function handleKeyboardShortcuts(event) {{
            if (event.ctrlKey || event.metaKey) {{
                switch(event.key) {{
                    case 'z':
                        event.preventDefault();
                        undo();
                        break;
                    case 'y':
                        event.preventDefault();
                        redo();
                        break;
                    case 's':
                        event.preventDefault();
                        saveDocument();
                        break;
                    case 'o':
                        event.preventDefault();
                        openDocument();
                        break;
                    case 'n':
                        event.preventDefault();
                        newDocument();
                        break;
                    case 'c':
                        event.preventDefault();
                        copy();
                        break;
                    case 'v':
                        event.preventDefault();
                        paste();
                        break;
                }}
            }} else {{
                switch(event.key) {{
                    case 'Delete':
                        deleteSelectedObjects();
                        break;
                    case 'Escape':
                        canvas.discardActiveObject();
                        canvas.renderAll();
                        break;
                }}
            }}
        }}
        
        // Menu and toolbar functions (stubs - to be implemented)
        function newDocument() {{ console.log('New document'); }}
        function openDocument() {{ console.log('Open document'); }}
        function saveDocument() {{ console.log('Save document'); }}
        function undo() {{ if (historyIndex > 0) restoreFromHistory(historyIndex - 1); }}
        function redo() {{ if (historyIndex < history.length - 1) restoreFromHistory(historyIndex + 1); }}
        function copy() {{ console.log('Copy'); }}
        function paste() {{ console.log('Paste'); }}
        function flipHorizontal() {{ console.log('Flip horizontal'); }}
        function flipVertical() {{ console.log('Flip vertical'); }}
        function rotateLeft() {{ console.log('Rotate left'); }}
        function rotateRight() {{ console.log('Rotate right'); }}
        function zoomIn() {{ canvas.setZoom(canvas.getZoom() * 1.1); }}
        function zoomOut() {{ canvas.setZoom(canvas.getZoom() * 0.9); }}
        function zoomFit() {{ canvas.setZoom(1); }}
        function exportImage() {{ console.log('Export image'); }}
        function printDocument() {{ console.log('Print document'); }}
        
        function deleteSelectedObjects() {{
            const activeObjects = canvas.getActiveObjects();
            activeObjects.forEach(obj => canvas.remove(obj));
            canvas.discardActiveObject();
        }}
        
        // Color functions
        function pickColor(type) {{
            // Open color picker (implementation needed)
            console.log('Pick color for', type);
        }}
        
        function swapColors() {{
            const fg = document.getElementById('fg-color').style.backgroundColor;
            const bg = document.getElementById('bg-color').style.backgroundColor;
            document.getElementById('fg-color').style.backgroundColor = bg;
            document.getElementById('bg-color').style.backgroundColor = fg;
        }}
        
        function resetColors() {{
            document.getElementById('fg-color').style.backgroundColor = '#000000';
            document.getElementById('bg-color').style.backgroundColor = '#ffffff';
        }}
        
        // Property group toggle
        function togglePropertyGroup(header) {{
            const content = header.nextElementSibling;
            const arrow = header.querySelector('span:last-child');
            
            if (content.style.display === 'none') {{
                content.style.display = 'block';
                arrow.textContent = '▼';
            }} else {{
                content.style.display = 'none';
                arrow.textContent = '▶';
            }}
        }}
        
        // Initialize panels
        function initializePanels() {{
            // Create initial layer
            createInitialLayer();
            
            // Initialize history
            saveToHistory();
        }}
        
        function createInitialLayer() {{
            const initialLayer = {{
                name: 'Background',
                visible: true,
                locked: false,
                active: true,
                objects: []
            }};
            
            layers.push(initialLayer);
            updateLayerPanel();
        }}
        
        // Initialize the application when DOM is loaded
        document.addEventListener('DOMContentLoaded', initializeApp);
        """

class CanvasSizeManager:
    """Manages different canvas sizes and formats"""
    
    CANVAS_SIZES = {
        # Business Cards
        "US Standard": {"width": 1050, "height": 600, "dpi": 300, "unit": "inches", "real_size": "3.5 × 2"},
        "EU Standard": {"width": 1004, "height": 649, "dpi": 300, "unit": "inches", "real_size": "3.346 × 2.165"},
        "UK Standard": {"width": 1004, "height": 649, "dpi": 300, "unit": "inches", "real_size": "3.346 × 2.165"},
        "Japanese Standard": {"width": 1075, "height": 649, "dpi": 300, "unit": "inches", "real_size": "3.582 × 2.165"},
        "Mini Card": {"width": 825, "height": 525, "dpi": 300, "unit": "inches", "real_size": "2.75 × 1.75"},
        "Jumbo Card": {"width": 1275, "height": 825, "dpi": 300, "unit": "inches", "real_size": "4.25 × 2.75"},
        "Square Card": {"width": 750, "height": 750, "dpi": 300, "unit": "inches", "real_size": "2.5 × 2.5"},
        "Slim Card": {"width": 1050, "height": 450, "dpi": 300, "unit": "inches", "real_size": "3.5 × 1.5"},
        "Folded Card": {"width": 2100, "height": 600, "dpi": 300, "unit": "inches", "real_size": "7 × 2"},
        
        # Social Media
        "Instagram Post": {"width": 1080, "height": 1080, "dpi": 72, "unit": "pixels", "real_size": "1080 × 1080"},
        "Instagram Story": {"width": 1080, "height": 1920, "dpi": 72, "unit": "pixels", "real_size": "1080 × 1920"},
        "Facebook Cover": {"width": 1200, "height": 630, "dpi": 72, "unit": "pixels", "real_size": "1200 × 630"},
        "Twitter Header": {"width": 1500, "height": 500, "dpi": 72, "unit": "pixels", "real_size": "1500 × 500"},
        "LinkedIn Banner": {"width": 1584, "height": 396, "dpi": 72, "unit": "pixels", "real_size": "1584 × 396"},
        "YouTube Thumbnail": {"width": 1280, "height": 720, "dpi": 72, "unit": "pixels", "real_size": "1280 × 720"},
        "Pinterest Pin": {"width": 735, "height": 1102, "dpi": 72, "unit": "pixels", "real_size": "735 × 1102"},
        
        # Print Materials
        "Postcard": {"width": 1800, "height": 1200, "dpi": 300, "unit": "inches", "real_size": "6 × 4"},
        "Flyer A4": {"width": 2480, "height": 3508, "dpi": 300, "unit": "inches", "real_size": "8.27 × 11.69"},
        "Flyer Letter": {"width": 2550, "height": 3300, "dpi": 300, "unit": "inches", "real_size": "8.5 × 11"},
        "Brochure Tri-fold": {"width": 3300, "height": 2550, "dpi": 300, "unit": "inches", "real_size": "11 × 8.5"},
        "Poster A3": {"width": 3508, "height": 4961, "dpi": 300, "unit": "inches", "real_size": "11.69 × 16.54"},
        "Banner": {"width": 10800, "height": 3600, "dpi": 300, "unit": "inches", "real_size": "36 × 12"},
        
        # Digital Formats
        "Web Banner": {"width": 728, "height": 90, "dpi": 72, "unit": "pixels", "real_size": "728 × 90"},
        "Mobile Banner": {"width": 320, "height": 50, "dpi": 72, "unit": "pixels", "real_size": "320 × 50"},
        "Square Ad": {"width": 300, "height": 300, "dpi": 72, "unit": "pixels", "real_size": "300 × 300"},
        "Leaderboard": {"width": 728, "height": 90, "dpi": 72, "unit": "pixels", "real_size": "728 × 90"},
        "Skyscraper": {"width": 160, "height": 600, "dpi": 72, "unit": "pixels", "real_size": "160 × 600"},
    }
    
    @classmethod
    def get_canvas_config(cls, size_name: str, orientation: str = "landscape") -> Dict[str, Any]:
        """Get canvas configuration for a specific size"""
        if size_name not in cls.CANVAS_SIZES:
            raise ValueError(f"Unknown canvas size: {size_name}")
        
        config = cls.CANVAS_SIZES[size_name].copy()
        
        # Apply orientation
        if orientation == "portrait" and config["width"] > config["height"]:
            config["width"], config["height"] = config["height"], config["width"]
            # Update real_size for portrait
            real_parts = config["real_size"].split(" × ")
            config["real_size"] = f"{real_parts[1]} × {real_parts[0]}"
        
        return config
    
    @classmethod
    def get_all_sizes(cls) -> List[str]:
        """Get list of all available canvas sizes"""
        return list(cls.CANVAS_SIZES.keys())
    
    @classmethod
    def get_sizes_by_category(cls) -> Dict[str, List[str]]:
        """Get canvas sizes grouped by category"""
        categories = {
            "Business Cards": [
                "US Standard", "EU Standard", "UK Standard", "Japanese Standard",
                "Mini Card", "Jumbo Card", "Square Card", "Slim Card", "Folded Card"
            ],
            "Social Media": [
                "Instagram Post", "Instagram Story", "Facebook Cover", "Twitter Header",
                "LinkedIn Banner", "YouTube Thumbnail", "Pinterest Pin"
            ],
            "Print Materials": [
                "Postcard", "Flyer A4", "Flyer Letter", "Brochure Tri-fold", "Poster A3", "Banner"
            ],
            "Digital Formats": [
                "Web Banner", "Mobile Banner", "Square Ad", "Leaderboard", "Skyscraper"
            ]
        }
        return categories


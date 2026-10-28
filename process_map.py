import re
import os
import json
from bs4 import BeautifulSoup

def process_map():
    # 1. Read the raw HTML provided by the user
    with open("raw_map_input.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # 2. Extract the text tags
    dark_tags_div = soup.find("div", class_="dark-tags")
    tags = []
    if dark_tags_div:
        for tag in dark_tags_div.find_all("div", class_="tag"):
            _id = tag.get("id", "")
            style = tag.get("style", "")
            text = tag.text.strip()
            tags.append({
                "id": _id,
                "style": style,
                "text": text
            })

    # 3. Extract the icon legends
    icon_divs = soup.find_all("img", class_="legend")
    
    # Map icon filenames to emojis
    icon_to_emoji = {
        "library": "ðŸ“š",
        "gym": "ðŸ‹ï¸",
        "medical": "ðŸ¥",
        "meat": "ðŸ—",
        "food": "ðŸ”",
        "snacks": "ðŸ¿",
        "atm": "ðŸ§",
        "wifi": "ðŸ“¶",
        "laundry": "ðŸ§º",
        "xerox": "ðŸ–¨ï¸",
        "parking": "ðŸ…¿ï¸",
        "office": "ðŸ¢",
        "football": "âš½",
        "cricket": "ðŸ",
        "chess": "â™Ÿï¸",
        "juice": "ðŸ§ƒ",
        "hostel": "ðŸ›ï¸",
        "parlour": "ðŸ’‡"
    }

    icons = []
    for img in icon_divs:
        src = img.get("src", "")
        style = img.get("style", "")
        _id = img.get("id", "")
        
        # Determine emoji based on src
        emoji = "ðŸ“" # default
        for key, val in icon_to_emoji.items():
            if key in src:
                emoji = val
                break
                
        icons.append({
            "id": _id,
            "style": style,
            "emoji": emoji
        })

    def get_tag_category(_id, text):
        _id_l = _id.lower()
        t_l = text.lower()
        # Passive Outdoor Spaces & Open Landscapes (Zero active grid power consumption)
        if any(k in _id_l or k in t_l for k in [
            'playground', 'lake', 'garden', 'empty', 'smart-agri', 'cricket', 'football',
            'tennis', 'basket', 'volley', 'throwball', 'outdoor-gym', 'ground'
        ]):
            return 'Passive Outdoor Space'
        if 'chiller' in _id_l or 'chiller' in t_l:
            return 'Chiller plant'
        if 'stp' in _id_l or 'sewage' in t_l:
            return 'STP'
        if any(k in _id_l or k in t_l for k in [
            'staff-quarter', 'power-house', 'guest-house', 'main-gate', 'west-gate', 
            'west-parking', 'main-parking', 'bus', 'atm', 'west-gate-staffs'
        ]):
            return 'Staff Quarters'
        if any(k in _id_l or k in t_l for k in [
            'hostel', 'mess', 'canteen', 'cafeteria', 'gym', 'laundry', 'parlour', 
            'hall', 'hut', 'visitor', 'recreation', 'dance', 'pet-room',
            'sapphire', 'ruby', 'pearl', 'diamond', 'emerald', 'coral', 'ganga', 'narmadha', 'kaveri', 'yamuna', 'bhavani'
        ]):
            return 'Hostels'
        return 'Academic blocks'

    # 5. Read the background SVG (campus_map.svg)
    with open("campus_map.svg", "r", encoding="utf-8") as f:
        bg_svg = f.read()

    # 6. Generate the new index.html
    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Streamlit Interactive Campus Map</title>
    
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: transparent;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}
        #map-container {{
            width: 100vw;
            height: 100vh;
            position: relative;
            background: #0b0f19;
            user-select: none;
        }}
        
        /* Modern Sleek Interactive Tag Badges */
        .interactive-tag {{
            position: absolute;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            padding: 5px 12px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.02em;
            white-space: nowrap;
            width: auto;
            min-width: max-content;
            color: #f8fafc;
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(8px);
            border: 1.5px solid rgba(148, 163, 184, 0.35);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
            transform: translate(-50%, -50%);
            z-index: 20;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .tag-academic {{
            border-color: rgba(56, 189, 248, 0.6);
            color: #e0f2fe;
        }}
        .tag-academic::before {{
            content: '';
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #38bdf8;
            box-shadow: 0 0 8px #38bdf8;
            flex-shrink: 0;
        }}
        
        .tag-hostels {{
            border-color: rgba(129, 140, 248, 0.6);
            color: #ede9fe;
        }}
        .tag-hostels::before {{
            content: '';
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #818cf8;
            box-shadow: 0 0 8px #818cf8;
            flex-shrink: 0;
        }}
        
        .tag-staff {{
            border-color: rgba(250, 204, 21, 0.6);
            color: #fef08a;
        }}
        .tag-staff::before {{
            content: '';
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #facc15;
            box-shadow: 0 0 8px #facc15;
            flex-shrink: 0;
        }}
        
        .tag-chiller {{
            border-color: rgba(14, 165, 233, 0.8);
            color: #bae6fd;
        }}
        .tag-chiller::before {{
            content: '';
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #0ea5e9;
            box-shadow: 0 0 8px #0ea5e9;
            flex-shrink: 0;
        }}
        
        .tag-stp {{
            border-color: rgba(34, 197, 94, 0.6);
            color: #dcfce7;
        }}
        .tag-stp::before {{
            content: '';
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow: 0 0 8px #22c55e;
            flex-shrink: 0;
        }}

        .tag-passive {{
            border-color: rgba(52, 211, 153, 0.5);
            color: #a7f3d0;
            background: rgba(15, 23, 42, 0.85);
        }}
        .tag-passive::before {{
            content: '';
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
            flex-shrink: 0;
        }}

        .interactive-tag:hover {{
            transform: translate(-50%, -50%) scale(1.18);
            background: rgba(30, 41, 59, 0.98);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.8), 0 0 16px rgba(56, 189, 248, 0.6);
            z-index: 1000;
        }}
        
        .interactive-tag.active {{
            transform: translate(-50%, -50%) scale(1.22);
            background: #0284c7 !important;
            color: #ffffff !important;
            border-color: #38bdf8 !important;
            box-shadow: 0 0 25px #38bdf8, 0 8px 25px rgba(0, 0, 0, 0.9) !important;
            z-index: 1001;
        }}

        .icon-legend {{
            position: absolute;
            font-size: 1.5rem;
            z-index: 15;
            text-shadow: 0 0 8px rgba(0,0,0,0.9);
            transform: translate(-50%, -50%);
            pointer-events: none;
        }}
        
        #map-wrapper {{
            position: absolute;
            top: 0;
            left: 0;
            width: 3420px;
            height: 3876px;
            transform-origin: 0 0;
        }}
        
        .svg-bg {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}

        /* Floating Zoom Controls */
        #map-controls {{
            position: fixed;
            top: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            z-index: 2000;
        }}
        #map-controls button {{
            width: 38px;
            height: 38px;
            border-radius: 8px;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(8px);
            border: 1px solid #2b2d49;
            color: #f8fafc;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        }}
        #map-controls button:hover {{
            background: #1e293b;
            border-color: #38bdf8;
            color: #38bdf8;
            transform: scale(1.1);
        }}
    </style>
</head>
<body>
    <div id="map-container">
        <!-- Floating Zoom Controls -->
        <div id="map-controls">
            <button id="zoom-in" title="Zoom In">+</button>
            <button id="zoom-out" title="Zoom Out">−</button>
            <button id="zoom-reset" title="Reset Map View">⟲</button>
        </div>

        <div id="map-wrapper">
            <!-- The Map SVG Background -->
            <div class="svg-bg">
                {bg_svg}
            </div>
            
            <!-- Map Markers / Icons -->
"""

    for icon in icons:
        style = icon['style']
        html_out += f'            <div class="icon-legend" style="{style}">{icon["emoji"]}</div>\n'

    html_out += "\n            <!-- Interactive Labels -->\n"
    
    category_to_class = {
        'Academic blocks': 'tag-academic',
        'Hostels': 'tag-hostels',
        'Staff Quarters': 'tag-staff',
        'Chiller plant': 'tag-chiller',
        'STP': 'tag-stp',
        'Passive Outdoor Space': 'tag-passive'
    }

    for tag in tags:
        category = get_tag_category(tag['id'], tag['text'])
        cat_class = category_to_class.get(category, 'tag-academic')
        data_attr = f'data-category="{category}" data-name="{tag["text"]}"'
        class_name = f"interactive-tag {cat_class}"
        inline_style = tag['style']
            
        html_out += f'            <div id="{tag["id"]}" class="{class_name}" {data_attr} style="{inline_style}">\n'
        html_out += f'                {tag["text"]}\n'
        html_out += f'            </div>\n'

    html_out += """
        </div>
    </div>

    <script>
        // Simple panning and zooming logic since svg-pan-zoom only works directly on SVGs
        // We have a div wrapper containing both SVG and HTML absolute tags
        
        const container = document.getElementById('map-container');
        const wrapper = document.getElementById('map-wrapper');
        
        let isDragging = false;
        let startX, startY;
        let translateX = 0, translateY = 0;
        let scale = 0.2; // Initial zoom to fit
        
        // Center the map initially
        const updateTransform = () => {
            wrapper.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
        };
        
        // Initial center
        window.onload = () => {
            const containerRect = container.getBoundingClientRect();
            // Try to fit the map
            scale = Math.min(containerRect.width / 3420, containerRect.height / 3876) * 0.9;
            translateX = (containerRect.width - (3420 * scale)) / 2;
            translateY = (containerRect.height - (3876 * scale)) / 2;
            updateTransform();
        };

        // Panning
        container.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
            container.style.cursor = 'grabbing';
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
            container.style.cursor = 'default';
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            translateX = e.clientX - startX;
            translateY = e.clientY - startY;
            updateTransform();
        });

        // Zooming
        container.addEventListener('wheel', (e) => {
            e.preventDefault();
            const zoomSensitivity = 0.001;
            const delta = -e.deltaY * zoomSensitivity;
            const newScale = Math.max(0.05, Math.min(scale * Math.exp(delta), 3));
            
            // Zoom towards mouse pointer
            const rect = container.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            
            translateX = mouseX - (mouseX - translateX) * (newScale / scale);
            translateY = mouseY - (mouseY - translateY) * (newScale / scale);
            scale = newScale;
            
            updateTransform();
        }, { passive: false });

        // --- Streamlit Communication ---
        function sendToStreamlit(data) {
            window.parent.postMessage({
                isStreamlitMessage: true,
                type: 'streamlit:setComponentValue',
                value: data
            }, '*');
        }

        // Floating zoom button listeners
        document.getElementById('zoom-in').addEventListener('click', () => {
            scale = Math.min(scale * 1.3, 3.5);
            updateTransform();
        });
        document.getElementById('zoom-out').addEventListener('click', () => {
            scale = Math.max(scale / 1.3, 0.05);
            updateTransform();
        });
        document.getElementById('zoom-reset').addEventListener('click', () => {
            const containerRect = container.getBoundingClientRect();
            scale = Math.min(containerRect.width / 3420, containerRect.height / 3876) * 0.9;
            translateX = (containerRect.width - (3420 * scale)) / 2;
            translateY = (containerRect.height - (3876 * scale)) / 2;
            updateTransform();
        });

        // Add click listeners to tags
        const tags = document.querySelectorAll('.interactive-tag');
        tags.forEach(tag => {
            tag.addEventListener('click', function(e) {
                e.stopPropagation(); // Prevent panning interference
                
                // Highlight active tag
                document.querySelectorAll('.interactive-tag').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // Send category and building details to Streamlit
                const category = this.getAttribute('data-category');
                const buildingId = this.getAttribute('id');
                const buildingName = this.getAttribute('data-name') || this.innerText;
                
                sendToStreamlit({
                    category: category,
                    building_id: buildingId,
                    building_name: buildingName
                });
            });
        });
        
        // Notify Streamlit we are ready
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: 'streamlit:componentReady',
            apiVersion: 1
        }, '*');
        
        // Set frame height
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: 'streamlit:setFrameHeight',
            height: 600
        }, '*');
        
        window.addEventListener('resize', () => {
            window.parent.postMessage({
                isStreamlitMessage: true,
                type: 'streamlit:setFrameHeight',
                height: 600
            }, '*');
        });
    </script>
</body>
</html>
"""

    with open(r"map_component\index.html", "w", encoding="utf-8") as f:
        f.write(html_out)
        
    import json
    locations_dict = {}
    for tag in tags:
        cat = get_tag_category(tag['id'], tag['text'])
        locations_dict[tag['text']] = {
            'id': tag['id'],
            'name': tag['text'],
            'category': cat
        }
    os.makedirs('outputs', exist_ok=True)
    with open('outputs/campus_locations.json', 'w', encoding='utf-8') as f:
        json.dump(locations_dict, f, indent=2)

if __name__ == "__main__":
    process_map()

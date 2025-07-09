# src/app/themes.py

# List of the standard themes you want to offer
BASE_THEMES = ["Streamlit Light", "Streamlit Dark"]

# Dictionary for all your custom theme presets
CUSTOM_THEMES = {
    "Demon Slayer": {
        "base": "dark",
        "primaryColor": "#2E8B57",           # Tanjiro's Green Haori
        "backgroundColor": "#1A2E2A",         # Very Dark Green (instead of black)
        "secondaryBackgroundColor": "#243E3A", # A slightly lighter dark green
        "textColor": "#F0FFF0",           # A soft, almost white Honeydew color
        "font": "serif"
    }, 
    "Dragon Ball Z": {
        "base": "light",
        "primaryColor": "#FF4500",           # Goku's vibrant Orange Gi for accents
        "backgroundColor": "#FFEBCD",         # A light, pale Orange for the main background
        "secondaryBackgroundColor": "#FFDAB9", # A slightly darker orange for sidebars
        "textColor": "#00008B",           # Dark Blue for text, like Goku's belt
        "font": "sans serif"
    },
    "Chainsaw Man": {
        "base": "light",
        "primaryColor": "#F9A826",           # Pochita's vibrant orange body
        "backgroundColor": "#FFF8E1",         # A very light, creamy orange background
        "secondaryBackgroundColor": "#FFE0B2", # A soft orange for sidebars
        "textColor": "#424242",           # Dark gray for text, like his handle
        "font": "monospace"
    },
    "Jujutsu Kaisen": {
        "base": "dark",
        "primaryColor": "#8B0000",
        "backgroundColor": "#0B0C10",
        "secondaryBackgroundColor": "#1F2833",
        "textColor": "#C5C6C7",
        "font": "sans serif",
    },
    "Bleach": {
        "base": "dark",
        "primaryColor": "#E53935",           # Vibrant Red for the mask's stripes
        "backgroundColor": "#121212",         # Very dark charcoal, almost black
        "secondaryBackgroundColor": "#212121", # A slightly lighter dark grey for contrast
        "textColor": "#FAFAFA",           # Crisp, clean white like the mask itself
        "font": "sans serif"
    },
     "One Piece": {
        "base": "light",
        "primaryColor": "#D32F2F",           # Luffy's Red Vest
        "backgroundColor": "#FFF8F0",         # A soft, warm off-white background
        "secondaryBackgroundColor": "#1976D2", # Luffy's Blue Shorts
        "textColor": "#2C3E50",           # A very dark, desaturated blue for text
        "font": "sans serif"
    },
    "Naruto": {
        "base": "light",
        "primaryColor": "#FF7F50",
        "backgroundColor": "#FFF8DC",
        "secondaryBackgroundColor": "#9ACD32",
        "textColor": "#2F4F4F",
        "font": "sans serif",
    },
    "Attack on Titan": {
        "base": "light",
        "primaryColor": "#8B4513",           # Leather Straps Brown
        "backgroundColor": "#F5F5DC",         # Survey Corps Jacket Beige
        "secondaryBackgroundColor": "#556B2F", # Cape Green
        "textColor": "#4A2C2A",           # A deep, dark brown for text
        "font": "serif"
    },
    "Dandadan": {
        "base": "light",
        "primaryColor": "#FFD700",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0FFF0",
        "textColor": "#FF69B4",
        "font": "monospace",
    },
    "Fullmetal Alchemist: Brotherhood": {
        "base": "light",
        "primaryColor": "#B22222",
        "backgroundColor": "#F5F5DC",
        "secondaryBackgroundColor": "#D2B48C",
        "textColor": "#5A2D0C",
        "font": "serif",
    },
    "Frieren: Beyond Journey's End": {
        "base": "light",
        "primaryColor": "#ADD8E6",
        "backgroundColor": "#F5FFFA",
        "secondaryBackgroundColor": "#E6E6FA",
        "textColor": "#483D8B",
        "font": "serif",
    },
    "Code Geass": {
        "base": "dark",
        "primaryColor": "#4B0082",
        "backgroundColor": "#120A12",
        "secondaryBackgroundColor": "#241824",
        "textColor": "#FFD700",
        "font": "sans serif",
    },
    "Neon Genesis Evangelion": {
        "base": "dark",
        "primaryColor": "#9400D3",
        "backgroundColor": "#1B1725",
        "secondaryBackgroundColor": "#3C3744",
        "textColor": "#7FFF00",
        "font": "monospace",
    },
}

# Combine the lists for the UI dropdown
ALL_THEMES = BASE_THEMES + list(CUSTOM_THEMES.keys())

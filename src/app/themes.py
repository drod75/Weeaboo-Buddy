# src/app/themes.py

# List of the standard themes you want to offer
BASE_THEMES = ["Streamlit Light", "Streamlit Dark"]

# Dictionary for all your custom theme presets
CUSTOM_THEMES = {
    "Demon Slayer": {
        "base": "dark",
        "primaryColor": "#2E8B57",
        "backgroundColor": "#1A1A1D",
        "secondaryBackgroundColor": "#2C3E50",
        "textColor": "#EAEAEA",
        "font": "serif",
    },
    "Dragon Ball Z": {
        "base": "light",
        "primaryColor": "#FF8C00",
        "backgroundColor": "#F0F8FF",
        "secondaryBackgroundColor": "#ADD8E6",
        "textColor": "#00008B",
        "font": "sans serif",
    },
    "Solo Leveling": {
        "base": "dark",
        "primaryColor": "#7B68EE",
        "backgroundColor": "#101010",
        "secondaryBackgroundColor": "#1A1A2E",
        "textColor": "#E0E0E0",
        "font": "sans serif",
    },
    "Chainsaw Man": {
        "base": "dark",
        "primaryColor": "#FF4500",
        "backgroundColor": "#1C1C1C",
        "secondaryBackgroundColor": "#4B0000",
        "textColor": "#FFFFFF",
        "font": "monospace",
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
        "primaryColor": "#FFA500",
        "backgroundColor": "#000000",
        "secondaryBackgroundColor": "#212121",
        "textColor": "#FFFFFF",
        "font": "serif",
    },
    "One Piece": {
        "base": "light",
        "primaryColor": "#000080",
        "backgroundColor": "#E0F7FA",
        "secondaryBackgroundColor": "#B2EBF2",
        "textColor": "#005662",
        "font": "sans serif",
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
        "base": "dark",
        "primaryColor": "#8B4513",
        "backgroundColor": "#242120",
        "secondaryBackgroundColor": "#3D3531",
        "textColor": "#D2B48C",
        "font": "serif",
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

# FIDE Chess Ratings - Interactive Visualizations

An interactive exploration of the FIDE chess ratings dataset, answering questions across three categories: global insights, subset analysis, and cross-subset comparisons.

## 📋 Project Overview

This project presents three interactive visualizations:

1. **Birth Year vs Peak Rating** - Explores the relationship between player birth year and peak rating achievement
2. **Gender Rating Gap by Country** - Compares how the gender rating gap varies across countries and over time
3. **Gender Representation Timeline** - Tracks gender representation evolution across different rating thresholds

## 📁 Project Structure

```
Implementation/
├── viz/                        # Visualization HTML files
│   ├── index.html              # Main landing page
│   ├── 1-age-rating-final.html # Visualization 1
│   ├── 2-gender-gap-map-final.html  # Visualization 2
│   └── 3-gender-timeline-final.html # Visualization 3
├── data/                       # Data files
│   ├── players.tsv             # Player information (~465k players)
│   ├── ratings.tsv             # Monthly ratings (~5M entries)
│   └── ...                     # Other data files
├── vendor/                     # Third-party libraries
│   └── d3-7.8.5/               # D3.js v7.8.5 (local copy)
└── README.md                   # This file
```

## 🔧 Dependencies

### Required Software
- **Web Browser**: Modern browser with JavaScript enabled (Chrome, Firefox, Edge, Safari)
- **Local HTTP Server**: Required to serve the files (due to browser security restrictions on local file access)

### Libraries (Included)
- **D3.js v7.8.5** - Data visualization library (included in `vendor/` folder)
- **TopoJSON** - Geographic data library (loaded from CDN in Visualization 2)
- **World Atlas** - World map data (loaded from CDN in Visualization 2)

## Running the Visualization

### Step 1: Start a Local HTTP Server

Navigate to the folder and start a simple HTTP server:

**Using Python 3:**
```bash
cd Implementation
python -m http.server
```

### Step 2: Open in Browser

Open your web browser and navigate to:

```
http://localhost:8000/viz/
```

This will open the main landing page (`index.html`) with links to all three visualizations.

### Direct Links to Visualizations

Once the server is running:
- **Landing Page**: http://localhost:8000/viz/
- **Visualization 1**: http://localhost:8000/viz/1-age-rating-final.html
- **Visualization 2**: http://localhost:8000/viz/2-gender-gap-map-final.html
- **Visualization 3**: http://localhost:8000/viz/3-gender-timeline-final.html

## Data Files

The visualizations require the data files in the `data/` folder

## Interaction Guide

### Common Interactions
- **Timeline Slider**: Drag to scrub through time
- **Play/Pause Button**: Animate through time
- **Hover**: Show tooltips with detailed information
- **Click**: Select items for comparison or filtering
- **Legend Toggle**: Show/hide categories

## Author

**S. M. Rakib Hasan**  
Information Visualization Project  

Grenoble INP - Fall 2025

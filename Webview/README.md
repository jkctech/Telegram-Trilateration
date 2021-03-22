# Webview

This would not be a project of mine without an unnecessary webtool. This part of the project converts the raw data from the scraper into an interactive map.

---

## Table of Contents
* [Preprocessing](#preprocessing)
* [Controls](#controls)

---

### Preprocessing
To show your collected data in the webview, follow these steps:
1. Collect enough data using the Scraper so trilateration can commence. (<a href="/Scraping/">Read More</a>)
1. Drag all your `.xlsx` files onto `combine.py` located in `/Scraping/src/tools`
1. A new `.xlsx` file will generate in the `tools` folder. Drag this file on top of `resolver.py`
1. A new `.json` file will generate. This is the file we will load into the webviewer
1. Open the `webview.html` with your browser.
1. Load in the `.json` file using the method described in the `File Loader` section in [Controls](#controls)

---

### Controls

<img src="_assets/controls.jpg" width="100%">

![](https://via.placeholder.com/15/FF0000/000000?text=+) **Map Controls**
* **Zoom** `in` / `out`
* **Switch** between a `Grayscale` and `Streets` map
* **Toggle** a `user` / `group`

The map is also controlled by mouse scrolling (Zooming) and dragging (Panning). Clicking a marker will show it's trilateration circles.


![](https://via.placeholder.com/15/B200FF/000000?text=+) **Extended Controls**
* **Center** - Will center your view back to the center of all markers
* **Show All** - Enables all markers
* **Hide All** - Disables all markers


![](https://via.placeholder.com/15/FF6A00/000000?text=+) **File Loader**
* **Select File** - Select a JSON file on your device to load in
* **Load** - Load in selected file


![](https://via.placeholder.com/15/0026FF/000000?text=+) **Settings**
* **Draw Circles** - Draw the colored trilateration circles for each entity
* **Draw Markers** - Draw the blue / orange markers for each entity
* **Show Unresolvable Users** - Show data of users with less than 3 datapoints


![](https://via.placeholder.com/15/00FF21/000000?text=+) **Information**

Contains general information about the webpanel and a legend for reference.

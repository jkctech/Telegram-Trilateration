# Scraping

By abusing NOX's GPS spoofing and doing some keyboard, mouse and OCR magic, we can automate tracing users.
Because who has time for doing this by hand?

---

## Table of Contents
* [Usage](#usage)
* [Theory](#theory)
* [Known Issues](#known-issues)

---

### Usage

---

### Theory

Almost anything can be automated with software these days. By using [NOX Player](https://www.bignox.com/) as an Android emulator with GPS Spoofing capabilities we can make Telegram think we are at specific locations. By moving ourselves to a location and doing a scan of users + their distances we can collect a dataset which we will use for trilateration. For this theory to work on a user, we need (At least) 3 points of reference.

**This concept is displayed very well in the [Trilateration](/Trilateration) part of this project.**

Okay so we want to scrape the data from the Telegram app. Since I am not very good in Android development, I decided to go the [OCR](https://en.wikipedia.org/wiki/Optical_character_recognition) route. Going this way has it's downsides but we will discuss those later. In this case, we will make use of [PyTesseract](https://pypi.org/project/pytesseract/).

Let's have a look at what we're dealing with inside of Telegram by making a new fresh account and opening **"People Nearby"**.

<img src="_assets/main.png" width="45%">
<img src="_assets/nearby.png" width="45%">

![](https://via.placeholder.com/15/FF00DC/000000?text=+) **Users**
![](https://via.placeholder.com/15/FF0000/000000?text=+) **Groups**
![](https://via.placeholder.com/15/00FF21/000000?text=+) **User Unfolder**
![](https://via.placeholder.com/15/0026FF/000000?text=+) **User / Group names**
![](https://via.placeholder.com/15/FF6A00/000000?text=+) **Distances (+ Members when applicable)**

Looking at this screen we need to accomplish a few things:
1. Unfold the complete list of users
1. Scroll through the list in a controlled manner for scraping
1. Take screenshots of the screen and scrape the characters
1. Determine if entries are Users or Groups

Optionally, I wanted to add support to download the profile pictures for the groups and users but that seemed like a lot of extra work for just a proof of concept so that is a postponed feature.

**Unfold the complete list of users**
As a first obstacle, we need to unfold the complete list of users so we can start scraping without any hiccups. If the "Show More" button is being shown on the screen at all, it will be on the same position every single time. By taking a screenshot of that specific area and looking for "Show More" in the resulted OCR string, we can detect if the list should be unfolded. If so, we simply just click with the mouse there once and we have the complete list on our screen.

**Scroll through the list in a controlled manner for scraping**
Scrolling through the list of chats nearby should not be THAT much of a hassle... Right? By simply dragging our mouse on the screen we can simulate scrolling.

First I created a way for my program to align itself to a specific point on the screen. Every chat has the same height on screen. This is easily spotted by looking at the light grey lines between chats. When I exported this as a screenshot (Using NOX itself), I measured the amount of pixels between those lines. This turned out to be **129 (NATIVE)** pixels. The "Native" in this is important. 

<img src="_assets/align.png" width="75%">

I have configured the emulator to run a higher resolution than my screen itself (About 2x). This is to make more items fit on the screen at once. The downside of this is that when you divide **129** by 2, you get a decimal number. Pixels cannot be divided into decimals, so this presents a problem. At first I didn't expect this issue to be of significance, but in the end this resulted in the alignment of my scraper to drift and miss some critical data. To counter this, the program will re-align itself after every "page" scan. This takes some extra time and can be optimized but for now, this will do.

Scrolling in itself turned out to be an issue as well. You have to move your mouse a certain amount of pixels before the emulator even registers it as a dragging finger. We will call this the **"Scrollbleed"** from now on. After determining the scrollbleed with some tests, I had to sum this to every distance I was about to drag, so this is now fixed.

**Take screenshots of the screen and scrape the characters**
Let's have a look at what a single "page" of users looks like.

<img src="_assets/page.png" width="75%">

Lucky as I am, exactly 14 users fit on my screen at once. This will make it easier to scrape since I can just take my entire screen at once and run it. I also underlined 2 entries in this screenshot. These are examples of names that tend to be an issue with the OCR engine. The first name is in Cyrillic which the OCR engine does not recognise. The second example has a tilde above it. It depends on the mood of the OCR engine if it recognises this or not. There is no easy way to fix both of these issues, so I decided to just... ignore the issues :D

After taking the screenshot, we convert it to grayscrale and crop-off the user pictures because they can contain characters as well and mess-up the scraping. After this, we are left with an alternating list of strings:

```
name
distance
name
distance
name
distance
...
```

By simply looping over those lines we can combine them into objects containing a name and distance. By writing a simple RegEx pattern I checked to see if the distances are really distances and that the OCR didn't mess up. In the same step. I also converted these distance strings into integers and made the distances in meters. So `1.75 km away` becomes `1750` as an integer. I also noticed that users are displayed ordered by distance in ascending order. I used this to loop over all distances and check if they are indeed ordered. If not, I assumed something broke in the meantime and I will error out to prevent corrupted or wrong data.

Now we end up with this outpur from the scraper:

<img src="_assets/scraped.png" width="75%">

![](https://via.placeholder.com/15/FF6A00/000000?text=+) Represents the scraper taking a screenshot, running the OCR engine and parsing the output.

![](https://via.placeholder.com/15/0026FF/000000?text=+) Represents the scraper scrolling back a little, after which it will re-align itself to the light-grey line on top of the next-to-scan user.

![](https://via.placeholder.com/15/00FF21/000000?text=+) Represents the stats and finishing-up.

Here we also see the scraper found out which entries are **groups** and which are **users**.

<img src="_assets/groups.png" width="50%">

Whenever the scraper finds the text **"Create a Local Group"** we start marking chats as groups instead of users. The theoretical edgecase in this, is that if someone has the actual name **"Create a Local Group"**, the scraper starts to mess up... The chances of this are slim so again, we will be ingoring this issue.


---

### Known Issues
* Telegram has a cooldown on changing your GPS position **[UNSOLVABLE]**
* Scraper sometimes misaligns on initial align
* Issues when users / groups have the same name **[UNSOLVABLE]**
* Coordinate scraper does not handle negatives very well
* OCR engine does not handle non-standard characters very well (Emoji's, Arabic, Cyrillic, etc.)

### Todo's
(Which I probably will never do)
* Properly parse flags
* Better OCR engine (Difficult without investing money)
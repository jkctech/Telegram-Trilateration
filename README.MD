# Telegram Trilateration

A while back, Telegram rolled out a new (Opt-in) feature which allows users to find people and groupchats close to their location. Because of poor implementation, this "feature" allows a user to see the distance between them and another user with about 10 meters of accuracy. By using trilateration we are able to pinpoint someone's (near) exact location...

When enabled, you will see this popup on your screen which is giving you a general warning which probably won't alert much people.

<img src="_assets/notification.jpg" width="50%">

The goal of this repository is to build a proof of concept for mass exploiting this "feature".

---

## Table of Contents
* [Trilateration](#trilateration) (Finding someone's EXACT location)
* [Scraping](#scraping) (Automating the trilateration)
* [Webview](#webview) (Using the scraped data)
* [Public Groups](#public-groups)
* [User Information](#user-information)

---

### Trilateration
A great example of why this new feature is a problem is trilateration.
([Not to be confused with triangulation](https://gis.stackexchange.com/questions/17344/differences-between-triangulation-and-trilateration))

Using this technique, we can determine a user's whereabouts by taking multiple samples of locations and distances relative to our own location.
(We will use GPS spoofing for this)

**This problem could be easily avoided by simply rounding the "Distance to X" to whole kilometers instead of just 10 meters...**

<img src="_assets/trilateration.jpg" width="75%">
<h5><a href="Trilateration/">Read More ></a></h5>

---

### Scraping

Locating someone by hand takes time (A few minutes) and effort (Clicking and typing). It will probably take you 20-ish minutes to track someone.
So naturally, I spent weeks of effort into automating this system to save myself minutes of time...

<img src="_assets/scrape.jpg" width="50%">
<h5><a href="Scraping/">Read More ></a></h5></a>

---

### Webview

Gathering the data through scraping is fun and all, but actually being able to interpret it is better.
**(I took this way too far, please don't ever be like me)**

<img src="_assets/webview.jpg" width="75%">

<h5><a href="Webview/">Read More ></a></h5></a>

---

### Public Groups
Other than users, groupchats can also be indexed by location. You have to create a group specifically for this purpose. The creator of the group probably realizes everyone can read along with the chats, but some of the people who join by invite for example won't.

The chats are shown to people who click on the group, even if they don't actually join. The groups are free to join by anyone so even blocking this won't suffice, but at least you KNOW that someone has read the chat.

Using this, it's not hard to find groups where people sell illegal goods / services or find private information.

<img src="_assets/groups.jpg" width="75%">

---

### User Information
In general, finding user information on Telegram is not difficult and it's expected that people see your profile, regardless of using the "Nearby" function or just username searching. The problem here is by using location search you gain much more information in the sense of knowing that persons general whereabouts and thus are able to find a specific person more easily.

By finding someone, you can see their profile picture(s), bio and username. (Depending on their privacy settings)

Being able to see someone's profile on a "search engine" is to be expected and key to it's functionality but being able to find people this way could open up a doorway for stalkers to find someone or just lurk for random people without them knowing their phonenumber or Telegram username.

<img src="_assets/user.jpg" width="75%">

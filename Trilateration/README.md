# Trilateration

* [Test 1](#test-1) (Random user)
* [Test 2](#test-2) (Friend with known location)

---

## Test 1

For the first proof of concept test, I picked a random user in the "Near me" list of my actual location.\
The person I picked is called "Clara".

<img src="_assets/tt1_overview.jpg" width="50%"><img src="_assets/tt1_user.jpg" width="50%">

For trilateration to be useful, I need a tool that can visualize it for me. I could write a tool like this myself but why should I when [https://www.gpsvisualizer.com/](https://www.gpsvisualizer.com/) exists? This website allows to import an `.xlsx` file and make it into a circle map using this formatting:

<img src="_assets/example_excel.jpg" width="75%">

To determine a location, you need at least 3 sets of data. I could either move there myself in the real world, or let my computer do the work for me. By using an emulated Android device, I can spoof my GPS location and make Telegram think I am at another location. I will be using Nox for this. ([https://www.bignox.com/](https://www.bignox.com/))

<img src="_assets/example_gps.jpg" width="50%">

Nox Allows me to move my GPS location by simply using an embedded Google Maps.\
It will also show us the exact coordinates we moved to which we will use for our trilateration.

**The steps for locating a specific person are rather easy:**

1. Guess their general location, let&#39;s say a city for example.
1. Place your GPS marker to a random location around that area.
	- **Please Note:** Telegram has ratelimiting on how quickly you can change your coordinates. The cooldown seemed to be +-10 minutes when I tried this.
1. Repeat above untill you see the user in the list.
1. Note your exact coordinates and the distance to that user.
1. Repeat the above at least 2 more times by moving around the expected area.
	- Keep about 5-6 km between your testing coordinates.
1. Note them in an Excel sheet as in the example.
1. Upload your Excel sheet to [https://www.gpsvisualizer.com/](https://www.gpsvisualizer.com/)
1. Find where all the circles intersect each other, this is the location of the user.

**These are the results Test 1:**

<img src="_assets/tt1_location.jpg" width="75%">
<img src="_assets/tt1_location2.jpg" width="75%">

**Judge the results for yourself...**

---

## Test 2

Since asking a stranger *"Hey, is this where you currently stay?"* to confirm our findings seems… You know… Odd? I re-did this experiment with a friend of mine. He was currently staying at a random (For me) unknown location in Nijmegen.

<img src="_assets/tt2_ask.jpg" width="75%">

**Me:**
_Also, I want to do an experiment, can you enable your Telegram location for me, tell me which city you are in, and let me see if I can pinpoint you?_

**Him:**
_I enabled it, I am in Nijmegen
 I have a Dr. Pepper can as profile picture
 And as name `Wesley X / @\<username\>`_

Finding him was not very difficult:

<img src="_assets/tt2_overview.jpg" width="50%"><img src="_assets/tt2_user.jpg" width="50%">

After I found him, I conducted the same test as on the previous example using the exact same steps. This resulted in the following dataset:

<img src="_assets/tt2_excel.jpg" width="75%">

After creating this dataset, I rendered a map using GPS Visualizer and collected the results. I replaced the background tiles with a texture instead of the actual map to give my friend some privacy.

_(By hosting a local webserver and redirecting all tile requests of Mapbox to localhost and hosting 1 single image there, for the curious people)_

<img src="_assets/tt2_location.jpg" width="75%">
<img src="_assets/tt2_location2.jpg" width="75%">

The purple dot marks the real location of my friend which I got later. I think this confirms this proof of concept is viable and should be taken seriously as an exploitable way of stalking people.

Of course, I had to confirm my calculations were correct by asking him if I was right.

<img src="_assets/tt2_confirm.jpg" width="75%">

**Me:**
_Am I right?_

**Him:**
_Red and blue intersect literally on top of my head_

**Me:**
_HAHAHHA_

**Him:**
**\*Gives his actual current location as confirmation\***

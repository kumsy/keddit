<p align="center">
  <a href="https://www.github.com/Kumsy/Keddit">
  <img src="static/images/keddit_logo_image_dark.png" width="550" title="Keddit">
  </a>
</p>

<p align="center">
  <a href="#author"> <b>About</b></a> <b>|</b> 
  <a href="#features"> <b>Features</b></a> <b>|</b> 
  <a href="#getting-started"> <b>Docs</b></a> <b>|</b>
  <a href="#tech-stack"> <b>Stack</b></a> <b>|</b> 
  <a href="#apis"> <b>API</b></a> 
</p>


<p align="center">
  <sub>The Force is strong with this one:</sub>
</p>

<p align="center">
  <sub><a href="https://www.linkedin.com/in/kristencampbell"><b>Kristen Campbell</b></a></sub>
</p>

----

```html
Detailed README.md currently in-progress
```
```html
Please reference my demo video currently at: 
```

* <a href="https://drive.google.com/open?id=1aR5mOqMz8OF7ECEa648PfNAlZBOfBZjt">Keddit Demo</a>


___________________________________

## What's Keddit?

Keddit is a full-stack community-driven social media site built from the ground-up, inspired by &nbsp; <a href="https://www.reddit.com"><img src="static/images/reddit-logo.png" width="90" title="Reddit"></a>

Users are able to create an account, upload their custom profile picture, create communities, post topics, comment, share posts, and vote on posts and comments. Posts may be up-voted or down-voted by other registered members on Keddit. If a post from any community has enough up-votes, it may be featured on Keddit's front page often referred to as 'k/ popular'.

---

## Features

###### Account Security
  * Password hashing via Bcrypt
  * Adds a layer of security from database breaches.

###### Account Customization
  * Upload custom profile pictures
  * Edit username and email addresses
  
###### Create Communities
  * Also known as 'subkeddits'
  * Holds collection of posts relating to it's subject title.
  
###### Create Posts and Comments
  * Upload local files through Python's Imaging Libray
  * Giphy's API provides registered users with the option to use GIFs with their messages.
  
###### Upvotes and Downvotes
  * Registered users may vote on posts and comments
  * Javascript communicates with Python's backend to allow for asynchronous voting.

###### Cloud Hosting
  * Autonomous multimedia hosting and servicing provided through Cloudinary's API.
  
###### Post Sharing via SMS/MMS
  * A share button feature using Twilio's API allows for users to share posts via SMS/MMS.
  
<sub>and more coming soon!</sub>

---

## Getting started

### Requirements
###### In order to get started, you will need to setup personal API Keys. Please setup developer accounts at:

* [Twilio](https://www.twilio.com)
* [Cloudinary](https://cloudinary.com)
* [Giphy](https://developers.giphy.com/)

###### Download and install PostgreSQL
* [PostgreSQL](https://www.postgresql.org/)

### Installation

###### Clone Keddit's repository in a project directory:
```
git clone https://github.com/Kumsy/Keddit.git
```

###### Set up a virtual environment:

* ###### Mac
```
virtualenv env
source env/bin/activate
```

* ###### Windows
```
virtualenv env --always-copy
source env/bin/activate
```
###### Install dependencies:
```
pip3 install -r requirements.txt
```
<sub>:bulb:&nbsp; <b>Note</b> - Depending on system setup, you may need to install bcrypt separately:</sub>
```
pip3 install flask-bcrypt
```

### Configuration
<sub>:key:&nbsp; We will now use your API keys to configure our server.</sub>

<sub>
Coming soon
</sub>

#####

---


## Tech Stack
<p>
  <a href="https://www.python.org/">
    <img class="tech-stack-python" src="static/images/Python.png" width="120"></a>&nbsp;
   <a href="https://www.postgresql.org/">
     <img class="tech-stack-psql" src="static/images/psql.png" width="60"></a>&nbsp;&nbsp;&nbsp;
  <a href="http://flask.pocoo.org/">
    <img class="tech-stack-flask" src="static/images/flask.png" width="45"></a>&nbsp;&nbsp;&nbsp;
  <a href="http://jinja.pocoo.org/docs/2.10/">
    <img class="tech-stack-jinja" src="static/images/jinja2.png" width="55"></a>&nbsp;
  <a href="https://www.javascript.com/">
    <img class="tech-stack-js" src="static/images/jslogo.png" width="60"></a>&nbsp;
</p>

--------------

## APIs

<p>
  <a href="https://cloudinary.com">
  <img src="https://res.cloudinary.com/cloudinary/image/upload/c_scale,w_200/v1/logo/for_white_bg/cloudinary_icon_for_white_bg.png"       width="35" title="Cloudinary"></a>
  <b>Cloudinary</b> - Images and GIFs from posts are automatically uploaded to a cloud server.
</p>


<p>&nbsp;
   <a href="https://developers.giphy.com/">
     <img src="static/images/giphybadge.gif" width="20" title="Giphy"></a>&nbsp;&nbsp;
  <b>Giphy</b> - Users can search for their favorites GIFs powered by GIPHY.
</p>


<p>&nbsp;
  <a href="https://www.twilio.com/">
    <img src="static/images/twilio-vector-logo.png" width="25" title="Twilio"></a>&nbsp;
  <b>Twilio</b> - Users can share posts and send the contents via SMS and MMS.
</p>

  
  ----
## Author

<p align="center">
  <a href="https://www.github.com/Kumsy/Keddit">
    <img src="static/images/kristen_snoo.PNG">
  </a>
</p>
<p align="center"><b>Kristen Campbell</b> is a Software Engineer in San Francisco, CA.</p>


<sub>
<p align="center">Keep in touch with Kristen! She's so friendly!</p>

<p align="center">
  <a href="https://www.linkedin.com/in/kristencampbell"> LinkedIn</a>&nbsp;
  <a href="https://twitter.com/kumykums"> Twitter</a>&nbsp;
  <a href="https://www.twitch.tv/kumy"> Twitch</a>&nbsp;
</p></sub>

<p align="center"><sub>Special Thanks:</sub></p>

<p align="center">
  <a href="https://drive.google.com/open?id=1ArXoKknxXs7fZFJ693JjsQadhB-jKc0j">
    <img class="press-logo" src="static/images/reddit-logo.png" width="100" title="Thank you Uzi"></a>&nbsp;&nbsp;
  <a href="https://drive.google.com/open?id=1B2Dx0yoaT1LWANajDM2ZVd26aavKsCgE">
  <img class="press-logo" src="static/images/twilio-logo-1.png" width="100" title="Thank you Mara"></a>
</p>


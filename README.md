<p align="center">
  <img src="static/images/keddit_logo_image_dark.png" width="550" title="Keddit">
</p>

<p align="center">
  <a href="#author"> <b>About</b></a> <b>|</b> 
  <a href="#features"> <b>Features</b></a> <b>|</b> 
  <a href="#getting-started"> <b>Docs</b></a> <b>|</b>
  <a href="#tech-stack"> <b>Stack</b></a> <b>|</b> 
  <a href="#apis"> <b>API</b></a> 
</p>


<p align="center">
  <sub>The Force is strong with this one..</sub>
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

Keddit is a full-stack community-driven social media site built from the ground-up, inspired by &nbsp; <img src="static/images/reddit-logo.png" width="90" title="Reddit">

Users are able to create an account, upload their custom profile picture, create communities, post topics, comment, share posts, and vote on posts and comments. Posts may be up-voted or down-voted by other registered members on Keddit. If a post from any community has enough up-votes, it may be featured on Keddit's main front page often referred to as 'k/ popular'.

---

## Features

<i>Coming soon</i>

Giphy's API provides registered users with the option to use GIFs in their messages, while Cloudinary's API automatically uploads, stores, and services all posts containing multimedia content to and from it's cloud server. With Twilio's API, users may share posts via SMS & MMS.

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
<sub>We will now use your API keys to configure our server.</sub>
###### From within our project directory:
```
mkdir config
cd config
touch config.json
```
###### Config.json:
```
Coming Soon
```



---

## APIs

<p>
  <img src="https://res.cloudinary.com/cloudinary/image/upload/c_scale,w_200/v1/logo/for_white_bg/cloudinary_icon_for_white_bg.png"       width="60" title="Cloudinary">
  <b>Cloudinary</b> - Images and GIFs from posts are automatically uploaded to a cloud server.
</p>


<p>&nbsp;
  <img src="static/images/giphybadge.gif" width="40" title="GIPHY">&nbsp;&nbsp;
  <b>Giphy</b> - Users can search for their favorites GIFs powered by GIPHY.
</p>


<p>&nbsp;
  <img src="static/images/twilio-vector-logo.png" width="40" title="Twilio">&nbsp;
  <b>Twilio</b> - Users can share posts and send the contents via SMS and MMS.
</p>






## Tech Stack
<p>
  <img class="tech-stack-python" src="static/images/Python.png" width="120">&nbsp;
  <img class="tech-stack-psql" src="static/images/psql.png" width="60">&nbsp;&nbsp;&nbsp;
  <img class="tech-stack-flask" src="static/images/flask.png" width="45">&nbsp;&nbsp;&nbsp;
  <img class="tech-stack-jinja" src="static/images/jinja2.png" width="55">&nbsp;
  <img class="tech-stack-js" src="static/images/jslogo.png" width="60">&nbsp;
</p>
  
  ----
## Author

<p align="center">
  <img src="static/images/kristen_snoo.PNG">
</p>
<p align="center"><b>Kristen Campbell</b> is a Software Engineer in San Francisco, CA.</p>

<sub>
<p align="center">Keep in touch with her! She's so friendly!</p>

<p align="center">
  <a href="https://www.linkedin.com/in/kristencampbell"> LinkedIn</a>&nbsp;
  <a href="https://twitter.com/kumykums"> Twitter</a>&nbsp;
  <a href="https://www.twitch.tv/kumy"> Twitch</a>&nbsp;
</p></sub>

# Instagram-Confessions
Users submit 'confession' to a web form which gets sent to server that converts confession into a picture and then posts it on Instagram.


Whole thing runs in one script. Requires:
- InstagramAPI
- Pillow
- textwrap3

Web form should be hosted on a website that allows php scripts to be run. I used 000webhostapp and it worked fine. 

Instagram has some limitations on how much you can post but I found that at least 60 seconds between each post didn't arrise any issues. You also must have a verified email/phone number on account or else it won't let you post anymore and won't tell you why... that was fun to debug. 

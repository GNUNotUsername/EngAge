# deco3801-frontend
 
The frontend requires node.js and Expo, along with an Expo GO installation on either iOS or Android.

First download and install node.js (we used the LTS 16.18.0).

Then "npm start" from the directory where DECO3801-FRONTEND is contained. 
You'll be prompted to "npm install" the various packages required from there.

After that if you "npm start", Expo will display a QR code that you can scan which will open up Expo GO and run Engage.

Since you probably don't own matthewhoffman.xyz as your backend server,
if you wish to run your OWN backend, you'll want to change the BASE address
in endspoints.js, but you're free to use ours for testing :D

# deco38001-backend

This is the code for the backend side of the EngAge app for DECO3801.
Authored by Mallika Mukherji, Christian Bingelli, Matthew Hoffman, Jack Blashki, Cooper Willis, Thomas Barton.

DESCRIPTION
Codebase for the backend for EngAge.
EngAge is an app which connects the aged community. It offers ways to add friends, attend events, send messages and keep up to date with how friends are feeling. It makes use of this information by communicating it to health authorities for better upkeep of community wellbeing.

REQUIREMENTS
The codebase was written on a unix server and so a unix system is advised.
This project utilises the django framework package for server-client communication.
Requires host with open port and valid SSL certificate.
Needs gunicorn, nginx and certbot packages installed.

The project was created was running OpenBSD and using the exact packages:
	nginx-1.22.0_6,2
	py39-certbot-1.27.0,1
	py39-certbot-nginx-1.27.0
	py39-django40-4.0.7

INSTRUCTIONS
Use certbot to create valid SSL certificate.
Start NGINX as a service to allow it to redirect http traffic to gunicorn which can't handle it natively.
	On a BSD host: for hosts using systemd or "service nginx start"
	On a host using systemd: "systemctl start nginx"
	On a host using OpenRC: "rc-service nginx start"
From the master directory, run "gunicorn -c config/gunicorn/dev.py" to host the necessary endpoints.
Program can now handle server requests.

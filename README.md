# Photo-Booth

This is a simple photo booth application that allows users to take pictures through a web interface on a gphoto2 compatible camera (I'm using a6400), and then send the pictures to an email address.

**Note**: This is some what of a work in progress, I was planning to use it at a Hackathon but I kept getting segfaults from the gphoto2 bindings.

Another note is that there is some "security" built into this application like the option to use https and a password to access the backend, but I wouldn't trust this too much.

## Getting Started

There's two main components to this project, the website and the backend which controls the camera.

### Website

First you'll need to create `frontend/.env` based on the `frontend/.env-template` file. Here's a little more about each of the variables.

* **PUBLIC_APP_PASSWORD** - This is a password specified on the backend server to make sure only approved clients can access the backend.
* **PUBLIC_API_URL** - This is the url of the backend server.
* **PUBLIC_EVENT_NAME** - This is the name of the event that will be displayed on the website.

The frontend is a svelte application, so you'll need to install the dependencies and then can either build the application or run it in development mode.

```bash
npm install
```

```bash
npm run dev
```

The website will be available at `http://localhost:3000`.

### Backend

Like the website, you'll need to create `backend/.env` based on the `backend/.env-template` file. Here's a little more about each of the variables.

* **APP_PASSWORD** - This is the password that is required to access the backend, needs to match the password specified in the website.
* **TWILIO_ACCOUNT_SID** - This is the account sid for your twilio account (note: twilio not supported yet).
* **TWILIO_AUTH_TOKEN** - This is the auth token for your twilio account (note: twilio not supported yet).
* **TWILIO_PHONE_NUMBER** - This is the phone number for your twilio account (note: twilio not supported yet).
* **SMTP_USERNAME** - This is the username for your smtp server you want to use to send emails.
* **SMTP_PASSWORD** - This is the password for your smtp server you want to use to send emails.
* **SMTP_HOST** - This is the host for your smtp server you want to use to send emails.
* **SMTP_STARTTLS_PORT** - This is the port for your smtp server you want to use to send emails.
* **SMTP_SSL_PORT** - This is the port for your smtp server you want to use to send emails.
* **SMTP_SOURCE_EMAIL** - This is the email address you want to send emails from.
* **USE_SIMULATED_CAMERA** - This is a boolean ("true", or default "false") that determines whether or not to use a simulated camera. This is useful for testing the application without a camera. The mp4 to use for the simulated camera needs to be specified in `backend/simulated.mp4`. 

The backend is a python application that uses the [gphoto2](https://github.com/gphoto/gphoto2) bindings to control the camera. You'll need to install the dependencies and then can run the application.

You might need to install some dependencies for [gphoto2](https://github.com/gphoto/gphoto2) or the binary itself. I remember that I had to install some dependencies on my RaspberryPI to get it to work, although sorry I don't remember what they were.

```bash
pip install -r requirements.txt
```

```bash
python3 server.py
```

The backend will be available at `http://localhost:8000`.

#### Using SSL

If you want to use SSL, you'll need to generate a certificate and key and put them in `backend/ssl/cert.pem` and `backend/ssl/key.pem` respectively. You can use the following commands to generate a self signed certificate and key.

```bash
openssl req -x509 -newkey rsa:4096 -keyout backend/ssl/key.pem -out backend/ssl/cert.pem -days 365 -nodes
```

**Note**: If you're using a self signed certificate, you'll need to open your backend url in a browser and accept the certificate before you can use it. I personally do this by going through the network tab, opening the failed request in a new tab by double clicking then hitting accept. When you refresh the website it should work.
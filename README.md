# Finding the top Queries for websites

## Google Search Console API configuration

### Step 1: Activating The API

Activate the API via the [API library here](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com).

Notice the project selected, you might want to create an project just for this. 😉

TK video 01

### Step 2: Configure OAuth

After activating it you'll need to configure the OAuth for that project.

To do this follow along with video bellow:

TK video 02

### Step 3: Create Your credentials

Then you have to create a client ID and client secret. To keep track of those info you'll need create a secrets file named `client_secrets.json` with the contents in [the file available here](https://github.com/googleapis/google-api-python-client/blob/master/samples/searchconsole/client_secrets.json).

Here's how you can get the ID and secret:

TK video 03

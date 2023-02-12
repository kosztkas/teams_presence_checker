# Teams Presence checker & busylight controller
Simple python app to poll own presence information from MS Graph and control a busylight.

When my status (activity) is `InACall` or `Presenting`, it turns on a light by sending a request to an ESP01+Relay module.

## Setup
First you need an Azure App registration, with delegated Presence.Read permissions.

Populate the `config.json` file with your apps client ID and the relays IP.

## Usage

Either you can run it directly:

```console
foo@bar:~/presence $ python3 main.py config.json
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ACBDEFGHI to authenticate.

```

or you can create a docker image with the provided Dockerfile:

```console
foo@bar:~/presence $ docker build -t presence .
```

and run it:

```console
foo@bar:~/presence $ docker run --name=presence -d presence
0a1b2c3d4e5f
foo@bar:~/presence $
```

The app uses the devicelogin flow, once started get the logs of your container which will give you your devicecode:

```console
foo@bar:~/presence $ docker logs presence
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ACBDEFGHI to authenticate.
foo@bar:~/presence $
```

head over to https://microsoft.com/devicelogin, enter the the code and follow the big blue buttons.

If you check your logs again in a couple of seconds, you can now see your Teams status (activity to be precise):

```console
foo@bar:~/presence $ docker logs presence
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ACBDEFGHI to authenticate.
Status changed to Available
Status changed to Busy
Status changed to InACall
foo@bar:~/presence $
```
## Some technical information

Polling is every 10 seconds, hardcoded (the rate limit by MS is `1500 requests in a 30 second period, per application per tenant`) <br>
Only logging when change occurs in status, relay is toggled accordingly. 

## TODO
- [ ] Use Environment variables instead of a config file
- [ ] Generate usage snippet gifs with VHS
- [x] Dockerfile needs some improvements
- [x] MS Device login session is like 5 minutes -> Use MSAL to renew tokens
- [x] Reduce docker image size


## Dependencies
- msal==1.17.0
- requests==2.22.0
- schedule==1.1.0


Based on the Microsoft Authentication Library (MSAL) sample

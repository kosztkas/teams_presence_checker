# Teams Presence checker & busylight controller
Simple python app to poll own presence information from MS Graph and control a busylight.

When my activity is `InACall` or `Presenting`, it turns on a light controlled by an ESP01+Relay module

## Making it work
First you need an Azure App registration, and populate the config.json file with your apps client ID and IP.

## Running it

Either you can run it from a shell

```console
foo@bar:~/presence $ python3 main.py config.json
```

or you can create a docker container with the provided Dockerfile.

## TODO
- [ ] Dockerfile needs some improvements
- [x] MS Device login session is like 5 minutes -> Use MSAL to renew tokens
- [x] Reduce docker image size


## Dependencies
- msal==1.17.0
- requests==2.22.0
- schedule==1.1.0


Based on the Microsoft Authentication Library (MSAL) sample

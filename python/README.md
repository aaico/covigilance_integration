# Covigilance API Python Starter

The python implementation provides you with 5 modules to call the different endpoints and test the covigilance.ai API. 

## Usage

We provide the executable `covigilance-api` to call the different methods of the API directly

* `./covigilance-api abstracts [FILENAME]`
* `./covigilance-api file [FILE OR PATH]`
* `./covigilance-api feedback [FILENAME]`
* `./covigilance-api webhook --port [LOCAL PORT] --url [PUBLIC URL]`

## Modules

### Classify Abstracts

The classify abstracts module has preparation functions to push a json, a csv, and an excel sheet to our API.
CSV and Excel will both be parsed into the correction json before sending.

IDs can either be already included in the data, or they will be generated based on input file and position in the list.

### Classify File(s)

The implementation has the base version included to upload a single file to the API. For convenience we also included a method to upload a folder of files to the API.

IDs will be based on the folder and the filename, if nothing else is provided.

### Feedback

The implementation allows to update a single or multiple predictions made by the AI.

### Webhook

A small echo server to see the results, that are being pushed back by the API. The echo server contains a reference to the update webhook methods for an easier time to test.

## Setup

### Access Token

Refer to [Main Introduction](../README.md).

### Webhook

To use the webhook on your local machine, you need to generate a public URL to enter into the system. We recommend to use [ngrok](https://ngrok.com/) to link your local service to Covigilance.ai.

For security please use the `https` version of the provided URL.

Example:
```
> ngrok http 5001

Session Status                online                                 
Account                       test@test.org         
Version                       2.3.40                                                  
Web Interface                 http://127.0.0.1:4040                  
Forwarding                    http://b497-84-172-93-198.ngrok.io -> http://localhost:5001
Forwarding                    https://b497-84-172-93-198.ngrok.io -> http://localhost:5001
                                                                   
```


# Covigilance.ai API Integration Starter Code

This repository provides a reference implementation for calling and integrating the API of Covigilance.ai, a platform that allows the screening of medical articles if they contain relevant safety information on pharmaceutical products.

The code includes different calls that allow you to retrieve and process data from the [Covigilance.ai API](https://covigilance.ai), as well as a simple server to receive the results over a webhook.

This starter code can help you quickly get started with integrating Covigilance.ai's powerful monitoring capabilities into your own application. Currently we provide an implementation in Python and looking to include more languages in the future.


If you want to write your own integration, check out the API documentation at [https://api.covigilance.ai/documentation].

We hope you find this repository helpful and welcome any feedback or contributions from the community.

## Authentication

The API is secured over an access token to identify your machine to your account. To generate a new token

1. Login to your account at [Covigilance.ai](app.covigilance.ai)
2. Go to Settings > Organization
3. Click on Authorization Token
4. Click on "Generate New Token"
5. Save the Token securely
6. (Optional) Export the token on your system as "COVIGILANCE_TOKEN"

Make sure not to leak the token (like including in repositories). To be save we will never show the token after the generation. In case you lost the token you can deactivate it and generate a new one.

The last step is optional, but the reference implementations can all ingest the token from the environment.
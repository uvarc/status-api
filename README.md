# status-api

This Chalice application creates API Gateway handlers in AWS Lambda for the "status" display on the UVA Research Computing website.

## Data

Data for this application is stored in DynamoDB tables:

- `status`
- `status-messages`

Data is updated via Slack Bot commands to `gopherbot`. From the #general channel, invoke the bot using the `!status` command:

```
!status (rivanna/ivy/skyline/dcos/value/project/globus) (green/yellow/red/blue) - update the website system status (channels: general)
!status message <text of message> - update the website system status text (channels: general)
!status (ok/clear) - remove the status message from the website (channels: general)
```
Color key:
- ![Green](https://www.rc.virginia.edu/images/status/green.png) - System running nominally
- ![Yellow](https://www.rc.virginia.edu/images/status/yellow.png) - System moderately impaired
- ![Red](https://www.rc.virginia.edu/images/status/red.png) - System severely impaired or unavailable
- ![Blue](https://www.rc.virginia.edu/images/status/blue.png) - System under maintenance

## Lambda Function

Chalice deploys a single Lambda function using Python 3.8 to support all endpoints and methods of this API. The ARN for this Lambda function is:

    arn:aws:lambda:us-east-1:474683445819:function:status-badges-dev

Permissions for the Lambda function are derived from `.chalice/policy-dev.json`. This policy creates an IAM role for the Lambda function named `status-badges-dev-api_handler`.

## API Gateway

The published API exists at the following endpoints:

1. `https://tja4lfp3da.execute-api.us-east-1.amazonaws.com/api/badge/{system}`
A **GET** method endpoint that returns a badge-ready JSON payload for any given system (`rivanna`, `ivy`, `skyline`, `dcos`, `globus`, `value`, or `project`)

```
{
  "schemaVersion": 1,
  "label": "DCOS",
  "message": "No issues",
  "color": "5cb85c"
}
```

An example badge, using the `shields.io` open endpoint coupled with the API data above:
![Rivanna Badge](https://img.shields.io/endpoint?url=https://tja4lfp3da.execute-api.us-east-1.amazonaws.com/api/badge/rivanna&style=for-the-badge)

2. `https://tja4lfp3da.execute-api.us-east-1.amazonaws.com/api/grid`
A **GET** method endpoint that returns a full array of status across all seven systems. All fields are included and are used in UI display for sorting, filtering, etc.

```
[
  {
    "system": "rivanna",
    "image": "/images/status/green.png",
    "message": "No issues",
    "sort": 0.0,
    "url": "/userinfo/rivanna/overview/",
    "color": "5cb85c",
    "statez": 0.0,
    "title": "Rivanna"
  },
  {
    "system": "ivy",
    "image": "/images/status/green.png",
    "message": "No issues",
    "sort": 1.0,
    "url": "/userinfo/ivy/overview/",
    "color": "5cb85c",
    "statez": 0.0,
    "title": "Ivy"
  },
  {
    "system": "skyline",
    "image": "/images/status/green.png",
    "message": "No issues",

    . . .
```

3. `https://tja4lfp3da.execute-api.us-east-1.amazonaws.com/api/messages`
A **GET** endpoint for retrieving any service update messages for display on the home page of the UVARC website.

Note that this payload always contains a minimal datetime placeholder, but must be populated further in order to be rendered in the UI:

```
[
  {
    "message": "message",
    "body": "2021-06-17 08:47:47  "
  }
]
```
# Backstage AI Recommendations Demo

## About this Project

[Start here](docs/index.md)

## Quickstart

### Prerequisites

- An OpenShift cluster
- OpenShift GitOps operator
- GitLab Operator

_These items can be substituted with upstream projects, however the code contained in this repo was only tested on this setup_

### Setup

`oc apply -f argo.yaml`

...

out of scope:

- argo operator setup

in scope:

- demo namespace
- argo apps
- set up backstage
- install generic analytics and set up event forwarding on backstage
- create burgershop resources in backstage
- set up zombie interactions with backstage
- set up log ingestion, tranformation and forwarding to redis
- set up redis

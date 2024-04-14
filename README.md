# Backstage AI Recommendations Demo

## Quickstart

### Prerequisites

-   An OpenShift cluster
-   OpenShift GitOps operator

_These items can be substituted with upstream projects, however the code contained in this repo was only tested on this setup_

### Setup

```
helm package helm
Successfully packaged chart and saved it to: backstage-ai-demo-0.1.0.tgz
helm repo index helm
```

`oc apply -f argo.yaml`

...

out of scope:

-   argo operator setup

in scope:

-   demo namespace
-   argo apps
-   set up backstage
-   install generic analytics and set up event forwarding on backstage
-   set up zombie interactions with backstage
-   set up log ingestion, tranformation and forwarding to redis
-   set up redis

## Prerequisites

These instructions assume you're using Linux (MacOS should also work) with [`docker`](https://docs.docker.com/get-docker) installed.  

_NOTE: if you receive a "permissioned denied" error, prefix the commands below with `sudo` (i.e., `sudo docker ...`)._

## Launching Odinson

To follow along, you'll first need to build an Odinson index using the provided data.

### 1. [Index documents](http://gh.lum.ai/odinson/docker.html#indexing-documents-using-the-docker-image)

```bash
docker run \
  --name="odinson-extras" \
  -it \
  --rm \
  -e "HOME=/app" \
  -v "$PWD/odinson:/app/data/odinson" \
  --entrypoint "bin/index-documents" \
  "lumai/odinson-extras:latest"
```

#### 2. [Launch the REST API](http://gh.lum.ai/odinson/restapi.html)

```bash
docker run \
--name="odinson-rest-api" \
-it \
--rm \
-e "HOME=/app" \
-p "0.0.0.0:9001:9000" \
-v "$PWD/data:/app/data/odinson" \
"lumai/odinson-rest-api:latest"
```

If the service launched correctly, you should be able to view the OpenAPI docs for the REST API at the following URL:

[http://localhost:9001/api](http://localhost:9001/api)

Let's test a **basic pattern** which identifies grammatical subjects:
```
(?<subject> [tag=/(NN|JJ).*/]* [incoming=nsubj] [tag=/(NN|JJ).*/]*)
```

We can apply it by executing a `GET` request to the [`/api/execute/pattern`](http://localhost:9001/api#/core/search) endpoint.  

The following URL will display all matches for this pattern in our test corpus:

- http://localhost:9001/api/execute/pattern?odinsonQuery=%28%3F%3Csubject%3E%20%5Btag%3D%2F%28NN%7CJJ%29.%2A%2F%5D%2A%20%5Bincoming%3Dnsubj%5D%20%5Btag%3D%2F%28NN%7CJJ%29.%2A%2F%5D%2A%29&pretty=true

## Querying Odinson

For most nontrivial applications, we'll want to use a _grammar_ (i.e., a set of interacting rules defining an information need).  Odinson grammars are written in [`YAML`]().  In the following example, we'll use a very simple grammar defined in [`grammar.yml`](./grammar.yml) and apply it using a `POST` request using Python.

### 1. Build the docker image

We'll be using Python to make our `POST` request.  First we need to build our Docker image:

```bash
cd python
docker build -f python/Dockerfile -t "parsertongue/odinson-example:python" python/
```

### 2. Querying the Odinson index from Python


#### Using `parentQuery` filters


Filter using a regex on the `title`:

```bash
docker run -it \
--network="host" \
-v $PWD:/data \
"parsertongue/odinson-example:python" \
--grammar /data/grammar.yml \
--host http://0.0.0.0:9001 \
--page-size 1 \
--parent-query "title:Subcell.*"
```

Filter using an exact match on `pubType`:

```bash
docker run -it \
--network="host" \
-v $PWD:/data \
"parsertongue/odinson-example:python" \
--grammar /data/grammar.yml \
--host http://0.0.0.0:9001 \
--page-size 1 \
--parent-query "pubType:\"epreprint\"
```
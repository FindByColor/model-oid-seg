![Find By Color Logo](https://findbycolor-github.s3.amazonaws.com/logo.png 'Find By Color Logo')

**[↤ BACK](../README.md)**

# Using Docker

> Docker ensures everything is preconfigured, set up, and ready to go.

**Requirements**:

- [X] [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## New Container

Run the following terminal command from the root of this project:

```bash
docker build --no-cache -t model-oid-seg .
```

### Run CLI Commands

Once you have the Docker instance built, you can spin it up and run a specific python script:

```bash
docker run --name fbc model-oid-seg python3 get_masks.py train
```

### Run Docker in CUDA Mode

If you are on a high-end computer with an Nvidia Graphics Card that supports CUDA, you can add the `--gpus=all` to `docker run` to enable CUDA support.  Just replace `docker run` with `docker run --gpus=all`

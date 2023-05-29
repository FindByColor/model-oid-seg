![Find By Color Logo](https://findbycolor-github.s3.amazonaws.com/logo.png 'Find By Color Logo')

**[↤ BACK](../README.md)**

# Troubleshooting

This document will contain a list of known issues, and how to solve them.

## SSH Keys

VS Code Remove Developer Containers require that SSH Keys installed on the host computer be added to the `ssh-agent` so VS Code can access them from the Docker Virtual Machine. When this goes wrong, you can see a few errors.

## GitHub

```
git@github.com: Permission denied (publickey)
```

If you are seeing this kind of error, you'll need to make sure you review the steps covered in our WIKI:

[![Up Next](https://img.shields.io/badge/WIKI-Git_Credentials-blue.svg?style=for-the-badge&logo=github&logoColor=ffffff&logoWidth=16)](https://github.com/FindByColor/.github/wiki/Git-Credentials)

## Docker

Having Docker issues? It happens to the best of us. I find going nuclear is the best option sometimes. This command will clean everything and allow you to do a clean install ( without it trying to use some random hidden cache ).

**WARNING:** If you are using docker for anything else, maybe don't use this and contact someone for help.

```bash
docker system prune -a
```

## Live Share

The quickest way to tell if Live Share is broken ( sadly, it happens more than it should ), you can check your status bar in the footer of VS Code. If you do not see `Live Share` in the status bar, then it broke.

### Here is how to fix the issue:

1. Press <kbd>F1</kbd> to open the Command Palette
2. Select `Live Share: Repair Installation` and let it run

## ModuleNotFoundError: No module named '_lzma'

```bash
sudo apt-get install lzma
sudo apt-get install liblzma-dev
sudo apt-get install libbz2-dev
```

After running the following, if you are using a `venv` session, you will need to `deactivate` and start the session over.

## Training Fails with 'killed process'

I found this can happen if you do not have a swap file in place that can be used for temp storage.  My research found that this needs to be around 64GB to prevent issues:

You can configure a swap file using the following:

```bash
sudo swapoff /swapfile
sudo fallocate -l 64G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Then you can verify things are working with:

```
sudo swapon --show
```

This shoudl show something like:

```
NAME      TYPE SIZE  USED PRIO
/swapfile file  64G 39.1G   -2
```

If you are using this computer a lot for training, you might want to make this swap file permanent:

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Another option you can try, if you are on a linux distro and you know your computer has a lot of memory, sometimes processes are killed because of an `overcommit` rule is tripped.

You can disable this by using:

```bash
sudo echo 1 > /proc/sys/vm/overcommit_memory
```

It is not recommended to leave it that way though, so set it back to `0` after training if this resolved your issue:

```bash
sudo echo 0 > /proc/sys/vm/overcommit_memory
```

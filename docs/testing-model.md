![Find By Color Logo](https://findbycolor-github.s3.amazonaws.com/logo.png 'Find By Color Logo')

**[↤ BACK](../README.md)**

# Testing the Model

Once training has started on our model, we can start testing it:

## Model Validation

> Generate Analytics on Model

YOLOv8 has some powerful validation tools which will generate a bunch of handy charts and graphs.

```bash
python validate.py
```

This will create a new folder in `./runs/segment/val` ( each time you run this, a new folder is created, e.g. `val2` etc ).

## Model Predictions

> This is the fun part - Testing that the model works.

We have a default `samples` folder which will be used with a confidence of `0.01`.

```bash
python predict.py nano
```

**Size Options:** `nano | small | medium | large | extralarge`

This will create a new folder in `./predictions/fbc-seg-{size}-e{epoch}` where `{size}` is the first letter of the size, and `{epoch}` is the number of the last epoch that ran

**CLI Options:**

`--confidence`

You can adjust the confidence of the prediction by passing in a `--confidence` of `-c` flag ( 0.0 - 1.0 ):

* Lower confidence has more predictions returned, but less accurate
* Higher confidence has less predictions returned, but more accurate

```bash
python predict.py --confidence 0.25
```

`--image`

You can pass in any image you want to test.  We recommend using an absolute path.

```bash
python predict.py --image /path/to/image.jpg
```

---

[![Previous Step](https://img.shields.io/badge/Previous-121212.svg?logo=github&style=for-the-badge)](./training-model.md)

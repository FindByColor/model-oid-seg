![Find By Color Logo](https://findbycolor-github.s3.amazonaws.com/logo.png 'Find By Color Logo')

**[↤ BACK](../README.md)**

# Training the Model

Once everything is setup, you can start training the model:

```bash
python train.py nano
```

**Size Options:** `nano | small | medium | large | extralarge`

Size         | Model            | mAP<sup>box</sup> | mAP<sup>mask</sup> | Speed CPU ONNX | Speed A100 TensorRT | Params | FLOPs
-------------|------------------|-------------------|--------------------|----------------|---------------------|--------|--------
`nano`       | [yolov8n-seg.pt] | 36.7              | 30.5               | 96.1 ms        | 1.21 ms             | 3.4 M  | 12.6 B
`small`      | [yolov8s-seg.pt] | 44.6              | 36.8               | 155.7 ms       | 1.47 ms             | 11.8 M | 42.6 B
`medium`     | [yolov8m-seg.pt] | 49.9              | 40.8               | 317.0 ms       | 2.18 ms             | 27.3 M | 110.2 B
`large`      | [yolov8l-seg.pt] | 52.3              | 42.6               | 572.4 ms       | 2.79 ms             | 46.0 M | 220.5 B
`extralarge` | [yolov8x-seg.pt] | 53.4              | 43.4               | 712.1 ms       | 4.02 ms             | 71.8 M | 344.1 B

* **mAP<sup>val</sup>** values are for single-model single-scale on [COCO val2017](https://docs.ultralytics.com/tasks/segment/#train:~:text=single%2Dscale%20on-,COCO%20val2017,-dataset.%0AReproduce) dataset.
* **Speed** averaged over COCO val images using an [Amazon EC2 P4d](https://aws.amazon.com/ec2/instance-types/p4/) instance.
* All Models are trained using an image size of 640px

**Customizing:**

Edit the following line in `train.py` with custom [Training Configuration](https://docs.ultralytics.com/usage/cfg/#train) to tweak performance of our model.

```python
model.train(data='config.yaml', epochs=100, imgsz=640)
```

[yolov8n-seg.pt]: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-seg.pt
[yolov8s-seg.pt]: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s-seg.pt
[yolov8m-seg.pt]: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m-seg.pt
[yolov8l-seg.pt]: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l-seg.pt
[yolov8x-seg.pt]: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x-seg.pt

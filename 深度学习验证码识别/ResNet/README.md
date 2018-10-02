# ResNet prototxt
**暂未上传私改版**  
Fork from **https://github.com/antingshen/resnet-protofiles**
Current config for 8 GPUs with 32 mini-batch size each.

The layer names are designed to match MSRA released pre-trained models to allow for finetuning. You may need to enable/disable bias on `conv1` to use these prototxts with some pretrained models. 

Running the ResNet-50 as-is gets a few percent lower accuracy than MSRA if done without random reshape & crop. 

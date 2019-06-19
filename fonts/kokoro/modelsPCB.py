from baseline.models.models import *


class PCB_classfifier(nn.Module):
    def __init__(self, part, ftOut=2048, basicFtSize=2048, largeFtSize=12288, class_num=None):
        super(PCB_classfifier, self).__init__()

        self.basicClass = ClassBlock(basicFtSize, class_num)
        self.largeClass = ClassBlock(largeFtSize, class_num)

        self.shareConv = ClassBlock_Conv(ftOut, class_num)

        for i in range(part):
            setattr(self, 'conv' + str(i), ClassBlock_Conv(ftOut, class_num))
            setattr(self, 'linear' + str(i), ClassBlock_Linear(ftOut, class_num))


# Part Model proposed in Yifan Sun etal. (2018)
class PCB_resnet(nn.Module):
    def __init__(self, class_num, part=6):
        super(PCB_resnet, self).__init__()
        self.part = part  # We cut the pool5 to 6 parts

        model_ft = models.resnet50(pretrained=True)
        model_ft.layer4[0].downsample[0].stride = (1, 1)
        model_ft.layer4[0].conv2.stride = (1, 1)
        # for mo in model_ft.layer4[0].modules(): if isinstance(mo, nn.Conv2d): mo.stride = (1, 1)

        model_ft.avgpool_global = nn.AdaptiveAvgPool2d((1, 1))
        model_ft.avgpool_local = nn.AdaptiveAvgPool2d((self.part, 1))

        classifier = PCB_classfifier(part=part, class_num=class_num)

        self.model = model_ft
        self.classifier = classifier

    def forward(self, x, pcbSettings):
        basicClass, largeClass, partClass, shareConv, basicFt, largeFt = pcbSettings
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)
        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)

        if basicClass or basicFt:
            x1 = torch.squeeze(self.model.avgpool_global(x))

        if largeClass or partClass or largeFt:
            x0 = self.model.avgpool_local(x)

            if largeClass or largeFt:
                x2 = x0.view(x0.size(0), -1)

            if partClass:
                x3 = nn.Dropout(p=0.5)(x0)
                if shareConv:
                    x3 = self.classifier.shareConv(x3)
                    x3 = x3.chunk(6, 2)
                else:
                    x3 = x3.chunk(6, 2)
                    x3 = [getattr(self.classifier, 'conv' + str(i)).conv_block(x3[i]) for i in range(self.part)]

            # if largeClass or largeFt: x2 = torch.squeeze(torch.cat(x3, dim=1))
            # x2.shape = torch.Size([64, 1536])

        y1 = [self.classifier.basicClass(x1)] if basicClass else []

        y2 = [self.classifier.largeClass(x2)] if largeClass else []

        y3 = [getattr(self.classifier, 'linear' + str(i)).classifier(x3[i].squeeze()) for i in
              range(self.part)] if partClass else []

        feature = x1 if basicFt else (x2 if largeFt else None)
        outputs = y1 + y2 + y3

        return feature, (outputs[0] if len(outputs) == 1 else outputs)

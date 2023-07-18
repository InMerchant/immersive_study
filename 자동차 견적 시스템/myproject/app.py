from flask import Flask, render_template, request
import torch
import cv2
import matplotlib.pyplot as plt
import os
from src.Models import Unet

app = Flask(__name__)

def process_image(image_path, models, device):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))

    img_input = img / 255.
    img_input = img_input.transpose([2, 0, 1])
    img_input = torch.tensor(img_input).float().to(device)
    img_input = img_input.unsqueeze(0)

    outputs = []
    for model in models:
        output = model(img_input)
        img_output = torch.argmax(output, dim=1).detach().cpu().numpy()
        img_output = img_output.transpose([1, 2, 0])
        outputs.append(img_output)

    return outputs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        image_path = 'static/' + image_file.filename
        image_file.save(image_path)

        weight_path = 'models/[DAMAGE][Scratch]Unet.pt'
        labels = ['Breakage', 'Crushed', 'Scratch', 'Seperated']
        models = []
        n_classes = 2
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        for label in labels:
            model_path = f'models/[DAMAGE][{label}]Unet.pt'
            model = Unet(encoder='resnet34', pre_weight='imagenet', num_classes=n_classes).to(device)
            model.model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
            model.eval()
            models.append(model)

        outputs = process_image(image_path, models, device)

        # 출력 이미지를 저장
        for i, output in enumerate(outputs):
            output_path = f'static/output_{i}.jpg'
            output = (output * 255).astype('uint8')
            cv2.imwrite(output_path, output)

        # 견적 계산
        price_table = [
            100, # Breakage
            200, # Crushed
            50,  # Scratch
            120, # Seperated
        ]
        total = 0
        for i, price in enumerate(price_table):
            area = outputs[i].sum()
            total += area * price

        return render_template('index.html', image_path=image_path, labels=labels, outputs=outputs, total=total)

    return render_template('index.html')

if __name__ == '__main__':
    # static 폴더에 저장할 output 이미지를 생성하기 위해 미리 폴더 생성
    os.makedirs('static', exist_ok=True)
    app.run()

import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from io import BytesIO
import requests
import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_wordcloud(text, mask_image=None, background_color='white', output_path='wordcloud.png'):
    wc = WordCloud(background_color=background_color, repeat=True, mask=mask_image)
    wc.generate(text)

    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig(output_path, format='png')
    plt.close()

def main():
    input_path = '../files/view_experience.json'
    mask_url = "https://raw.githubusercontent.com/R-CoderDotCom/samples/main/wordcloud-mask.jpg"
    output_path = "../files/wordcloud.png"

    data = load_json(input_path)
    skills = [item["Skill"] for item in data]
    text = "Python " + " ".join(skills)

    response = requests.get(mask_url)
    mask = np.array(Image.open(BytesIO(response.content)))

    generate_wordcloud(text, mask_image=mask, output_path=output_path)

if __name__ == "__main__":
    main()

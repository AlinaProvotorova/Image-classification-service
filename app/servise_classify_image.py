import settings


def classify_image(image):
    if image.mode == 'P':
        frame_number = 0
        image.seek(frame_number)
        image = image.resize((224, 224)).convert('RGB')
    settings.MODEL.eval()
    preprocess = settings.WEIGHTS.transforms()
    batch = preprocess(image).unsqueeze(0)
    prediction = settings.MODEL(batch).squeeze(0).softmax(0)
    class_id = prediction.argmax().item()
    category_name = settings.WEIGHTS.meta["categories"][class_id]
    return category_name

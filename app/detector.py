import uuid
import numpy as np
import face_recognition
import cv2
from PIL import Image, ImageOps, ImageDraw, ImageFont
from torch.autograd import Variable
from torchvision import transforms
from app import model


rect_color = (244, 113, 66)
imgsize = 48, 48
emotion_classes = ['Anger', 'Contempt', 'Disgust', 'Fear',
                   'Happiness', 'Neutral', 'Sadness', 'Surprise']


def save_emotion_image(image):
    """ Takes a PIL Image as input and saves an emotion
    annotated copy, returning the filename of the copy """

    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    pil_image = draw_rects(image, detect_faces(image))
    image_file = 'temp/' + uuid.uuid4().hex + '.jpg'
    pil_image.save('app/static/' + image_file)

    return image_file


def detect_faces(image):
    """ Detects faces in the supplied image file """

    face_locations = face_recognition.face_locations(image)
    return face_locations


def process_face(gray_image, coords):
    """ Crops and preprocesses detected faces """
    face = gray_image[coords[0]:coords[2], coords[3]:coords[1]]
    face = np.repeat(face[:, :, None], 3, axis=2)

    # Convert to PIL Image and resize.
    face = Image.fromarray(face)
    resized = ImageOps.fit(face, imgsize, Image.ANTIALIAS)

    # Transform it into a torch tensor
    loader = transforms.Compose([transforms.ToTensor()])

    return loader(resized).unsqueeze(0)


def predict_emotion(image, model):
    """ Predicts the emotion from an image tensor """

    img_variable = Variable(image)
    logprob = model.forward(img_variable).data.numpy()[0]
    prob = np.exp(logprob)

    return emotion_classes[prob.argmax()]


def draw_rects(image, face_locations):
    """ Draws rectangles around the faces and writes detected
    emotion below it """

    # Placeholder
    emotions = ['Poker'] * len(face_locations)

    # Convert to grayscale and extract faces
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = [process_face(gray_image, coords)
             for coords in face_locations]
    emotions = [predict_emotion(face, model)
                for face in faces]

    # Convert to PIL image
    pil_image = Image.fromarray(image[:, :, ::-1])

    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), emotion in zip(face_locations, emotions):

        # Draw bounding box around face
        draw.rectangle(((left, top), (right, bottom)), outline=rect_color)

        # Write emotion in caption box
        caption_box_height = 0.1 * (bottom - top)
        fnt = ImageFont.truetype('app/static/gillsans.ttf',
                                 size=int(caption_box_height))
        textwidth, textheight = draw.textsize(emotion, font=fnt)
        textwidth += 0.25 * textwidth

        # Draw Caption box
        draw.rectangle(((left, bottom + caption_box_height),
                        (left + textwidth, bottom)),
                       fill=rect_color, outline=rect_color)

        # Draw text
        draw.text((left + 0.10 * textwidth,
                   bottom + (0.05 * caption_box_height)),
                  emotion, font=fnt, fill=(255, 255, 255, 255))

    del draw

    return pil_image

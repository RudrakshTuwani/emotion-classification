import face_recognition
from PIL import Image, ImageDraw, ImageFont


rect_color = (244, 113, 66)
fnt_sizes = {sz: ImageFont.truetype('app/static/gillsans.ttf', size=sz)
             for sz in range(1, 72)}

def detect_faces(image):
    """ Detects faces in the supplied image file """

    face_locations = face_recognition.face_locations(image)
    return face_locations


def draw_rects(image, face_locations, emotions="Poker"):
    """ Draws rectangles around the faces and writes detected
    emotion below it """

    emotions = [emotions] * len(face_locations)

    # Convert the image to a PIL-format image so that we can
    # draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(image[:, :, ::-1])

    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), emotion in zip(face_locations, emotions):

        draw.rectangle(((left, top), (right, bottom)), outline=rect_color)

        # Draw a label with a name below the face
        box_height = 0.1 * (bottom - top)
        fnt = fnt_sizes[int(box_height)]
        text_width, text_height = draw.textsize(emotion, font=fnt)

        draw.rectangle(((left, bottom - box_height),
                        (right, bottom)), fill=rect_color, outline=rect_color)
        draw.text((left + 6, bottom - (0.9 * box_height)), "POKER",
                  font=fnt, fill=(255, 255, 255, 255))

    del draw

    return pil_image

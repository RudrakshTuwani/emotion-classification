import face_recognition
from PIL import Image, ImageDraw, ImageFont


rect_color = (244, 113, 66)


def detect_faces(image):
    """ Detects faces in the supplied image file """

    face_locations = face_recognition.face_locations(image)
    return face_locations


def draw_rects(image, face_locations, emotions=None):
    """ Draws rectangles around the faces and writes detected
    emotion below it """

    # Placeholder
    emotions = ['Poker'] * len(face_locations)

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

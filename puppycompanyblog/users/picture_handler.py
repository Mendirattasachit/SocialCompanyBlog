import os
from PIL import Image
from flask import url_for, current_app
from werkzeug.utils import secure_filename


def add_profile_pic(pic_upload, username):

    filename = pic_upload.filename
    # 'image'  .  'jpg'
    ext_type = filename.split('.')[-1]
    # We gonna store pic as username.jpg OR username.png, and username is UNIQUE!
    storage_filename = str(username) + '.' + ext_type

    filepath = os.path.join(current_app.root_path,
                            'static/profile_pics', storage_filename)  # puppycompanyblog/static/profile_pics/username.jpg

    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)  # To resize it to 200x200 pixel
    pic.save(filename)

    return storage_filename

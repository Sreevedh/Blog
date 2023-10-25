# pictures_handler.py file under users
import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):
    # we will use it when we create views for user.
    filename = pic_upload.filename
    # mypicture      .         jpeg ----> Splitting on the dot.
    ext_type = filename.split('.')[-1]
    # will be saving the file as "username.jpeg"
    storage_filename = str(username) + '.' + ext_type

    file_path = os.path.join(current_app.root_path, 'static/profile_pics', storage_filename)

    output_size = (200, 200)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(file_path)

    return storage_filename
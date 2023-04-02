ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif',"zip"]
ALLOWED_EXTENSIONS_LABEL = ["txt",'xml',"zip"]

UPLOADS_FOLDER = 'uploads/images/'

def file_valid(file):
  return '.' in file and \
    file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def label_valid(file):
  return '.' in file and \
    file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_LABEL
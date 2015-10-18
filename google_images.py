import json
import os
import time
import requests
from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError

import numpy as np
import cv2
import face_detect as fd

def find_character(query):
  """Download full size images from Google image search.
  Don't print or republish images without permission.
  I used this to train a learning algorithm.
  """
  path = 'tmp/characters'
  BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
             'v=1.0&q=' + query + '&start=%d'

  BASE_PATH = path

  if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

  start = 0 # Google's start query string parameter for pagination.
  while True:
    r = requests.get(BASE_URL % start)
    for image_info in json.loads(r.text)['responseData']['results']:
      url = image_info['unescapedUrl']
      try:
        image_r = requests.get(url)
      except ConnectionError, e:
        print 'could not download %s' % url
        continue

      # Remove file-system path characters from name.
      title = image_info['titleNoFormatting'].replace('/', '').replace('\\', '')

      file = open(os.path.join(BASE_PATH, '%s.jpg') % query, 'w')
      try:
        arr = np.asarray(bytearray(image_r.content), dtype=np.uint8)
        img = cv2.imdecode(arr,-1) # 'load it as it is'
        # save a copy of the image
        results = fd.detect_face(img)
        print(results)
        if not results:
          continue
        Image.open(StringIO(image_r.content)).save(file)
        return (results, img)
      except IOError, e:
        # Throw away some gifs...blegh.
        print 'could not save %s' % url
        continue
      finally:
        file.close()
    start += 4

# Example use
find_character('data character')

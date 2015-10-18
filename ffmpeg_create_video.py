import subprocess

ASPECT_RATIO = 16.0 / 9.0
VERTICAL_RESOLUTION = 720
HORIZONTAL_RESOLUTION = int(VERTICAL_RESOLUTION * ASPECT_RATIO)

FRAME_RATE = 24

VIDEO_FILENAME = 'out'

ffmpeg_create_video_command = ['ffmpeg',
	'-y', # overwrite file if it exists
	'-f', 'rawvideo',
	'-vcodec', 'rawvideo',
	'-s', '%dx%d' % (HORIZONTAL_RESOLUTION, VERTICAL_RESOLUTION),
	'-pix_fmt', 'rgb24',
	'-r', '%d' % FRAME_RATE,
	'-i', '-',
	'-an',
	'-vcodec', 'mpeg4',
	'%s.mp4' % VIDEO_FILENAME
	]

import scipy.ndimage

cat_image = scipy.ndimage.imread('tmp/cat.jpg')
cat2_image = scipy.ndimage.imread('tmp/cat2.jpg')

pipe = subprocess.Popen(ffmpeg_create_video_command, stdin=subprocess.PIPE)

for i in range(240):
	pipe.stdin.write(cat_image.tostring())
	pipe.stdin.write(cat2_image.tostring())

pipe.stdin.close()

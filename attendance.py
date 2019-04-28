import os
import face_recognition
from tqdm import tqdm
dir='./Database CCE_C/'
image_list = os.listdir(dir)
load_images = []
known_encoding = []
print('Encoding known Image this may take long...')

for image in tqdm(image_list) :
    load_images.append(face_recognition.load_image_file(dir+image))
    known_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file(dir+image)))

print('Enter the group photo')
file_stream=input()
unknown_image = face_recognition.load_image_file(file_stream)
unknown_image_face_location = face_recognition.face_locations(unknown_image)
unknown_faces = []
unknown_faces_encoding = []
for i in unknown_image_face_location:
    try:
        unknown_faces.append(unknown_image[i[0]:i[2],i[3]:i[1]])
        unknown_faces_encoding.append(face_recognition.face_encodings(unknown_image[i[0]:i[2],i[3]:i[1]])[0])
    except:
        print("Exception occured")
    
results = []
results.append('Person,Attendance')
for i in range(len(known_encoding)):
    result = str()
    flag = False
    result = result + image_list[i]
    for encoding in unknown_faces_encoding:
        found = face_recognition.compare_faces(known_encoding[i], encoding,tolerance=0.5)
        if found[0]:
            flag = True
            break
    if flag:
        result = result + ',Present'
    else:
        result = result + ',Absent'
    results.append(result)
import datetime
time = str(datetime.datetime.now())
filename='./result/Attendance '+time+'.csv'
print(results)
f=open(filename, "a+")
for result in results:
    f.write('%s\n' % (result))
f.close()

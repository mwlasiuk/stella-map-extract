import json
import numpy
import transforms3d
import cv2

with open('unpacker-0.json') as unpacker_file:
    data = json.load(unpacker_file)

landmarks = dict(data['landmarks'].items())
keyframes = dict(data['keyframes'].items())
camera = dict(data['cameras']['GOPROMAX'])

cols = camera['cols']
rows = camera['rows']
channels = 1

with open('poses.csv', 'w') as poses_file:
    poses_file.write('# id, rot_cw_x, rot_cw_y, rot_cw_z, rot_cw_w, trans_cw_x, trans_cw_y, trans_cw_z, trans_wc_x, trans_wc_y, trans_wc_z\n')

    for keyframe_id, keyframe in keyframes.items():

        rot_cw = keyframe['rot_cw']
        trans_cw = keyframe['trans_cw']
        undist_keypts = keyframe['undist_keypts']

        # print(undist_keypts[0])

        q = numpy.array([rot_cw[3], rot_cw[0], rot_cw[1], rot_cw[2]])
        t = numpy.array([trans_cw[0], trans_cw[1], trans_cw[2]])
        z = numpy.array([1.0, 1.0, 1.0])

        R = transforms3d.quaternions.quat2mat(q)
        M = transforms3d.affines.compose(t, R, z)

        M_inv = numpy.linalg.inv(M)

        t_x = M_inv[0, 3]
        t_y = M_inv[1, 3]
        t_z = M_inv[2, 3]

        poses_file.write(f'{keyframe_id}, {rot_cw[0]}, {rot_cw[1]}, {rot_cw[2]}, {rot_cw[3]}, {trans_cw[0]}, {trans_cw[1]}, {trans_cw[2]}, {t_x}, {t_y}, {t_z}\n');

        with open(f'landmarks-for-keyframe-{keyframe_id}.csv', 'w') as keyframe_landmarks_file:
            for landmark_id in keyframe['lm_ids']:
                if landmark_id  == -1:
                    continue
                landmark = landmarks[str(landmark_id)]
                pos_w = landmark['pos_w']
                keyframe_landmarks_file.write(f'{pos_w[0]}, {pos_w[1]}, {pos_w[2]}\n')

        with open(f'keypoints-for-keyframe-{keyframe_id}.csv', 'w') as keyframe_keypoints_file:

            img = numpy.zeros((rows, cols, channels), dtype = "uint8")

            for undist_keypt in undist_keypts:
                pt = undist_keypt['pt']

                img[int(pt[1]) - 1, int(pt[0]) - 1] = numpy.array([0xFF])
                img[int(pt[1]) - 0, int(pt[0]) - 1] = numpy.array([0xFF])
                img[int(pt[1]) + 1, int(pt[0]) - 1] = numpy.array([0xFF])

                img[int(pt[1]) - 1, int(pt[0]) + 0] = numpy.array([0xFF])
                img[int(pt[1]) + 0, int(pt[0]) + 0] = numpy.array([0xFF])
                img[int(pt[1]) + 1, int(pt[0]) + 0] = numpy.array([0xFF])

                img[int(pt[1]) - 1, int(pt[0]) + 1] = numpy.array([0xFF])
                img[int(pt[1]) + 0, int(pt[0]) + 1] = numpy.array([0xFF])
                img[int(pt[1]) + 1, int(pt[0]) + 1] = numpy.array([0xFF])

                keyframe_keypoints_file.write(f'{pt[0]}, {pt[1]}\n')

            cv2.imwrite(f'img-keypoints-for-keyframe-{keyframe_id}.png', img)
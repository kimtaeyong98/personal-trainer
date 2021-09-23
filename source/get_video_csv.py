from scipy.spatial import distance as dist
import numpy as np
import pandas as pd
import progressbar
import cv2

# 운동 종류 , 유저(사용자인지,트레이너인지)를 입력받아 스켈레톤 동영상을 생성하고 좌표를 csv로 저장


def get_video(exercise_Type, User_classification):

    protoFile = "./model/pose_deploy_linevec.prototxt"
    weightsFile = "./model/pose_iter_160000.caffemodel"

    if User_classification == "trainer":
        if exercise_Type ==  "스쿼트":
            video_path = './video/스쿼트_트레이너.mp4'
            out_path = './trainer/스쿼트/트레이너_스쿼트.mp4'  # 결과 파일
            csv_path = './trainer/스쿼트/트레이너_스쿼트.csv'  # 결과 파일 csv
        elif exercise_Type == "벤치프레스":
            video_path = './video/벤치프레스_트레이너.mp4'
            out_path = './trainer/벤치프레스/트레이너_벤치프레스.mp4'  # 결과 파일
            csv_path = './trainer/벤치프레스/트레이너_벤치프레스.csv'  # 결과 파일 csv
        elif exercise_Type== "풀업": 
            video_path = './video/풀업_트레이너.mp4'
            out_path = './trainer/풀업/트레이너_풀업.mp4'  # 결과 파일
            csv_path = './trainer/풀업/트레이너_풀업.csv'  # 결과 파일 csv
        else:
            print("파일이 없습니다.")
            return
        
    else:
        if exercise_Type ==  "스쿼트":
            video_path = './video/스쿼트_유저.mp4'
            out_path = './user/스쿼트/유저_스쿼트.mp4'  # 결과 파일
            csv_path = './user/스쿼트/유저_스쿼트.csv'  # 결과 파일 csv
        elif exercise_Type == "벤치프레스":
            video_path = './video/벤치프레스_유저.mp4'
            out_path = './user/벤치프레스/유저_벤치프레스.mp4'  # 결과 파일
            csv_path = './user/벤치프레스/유저_벤치프레스.csv'  # 결과 파일 csv
        elif exercise_Type =="풀업":
            video_path = './video/풀업_유저.mp4'
            out_path = './user/풀업/유저_풀업.mp4'  # 결과 파일
            csv_path = './user/풀업/유저_풀업.csv'  # 결과 파일 csv
        else: 
            print("파일이 없습니다.")
            return
    

    # 모델과 가중치 불러오기
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    # 비디오 정보 저장
    cap = cv2.VideoCapture(video_path)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    ok, frame = cap.read()
    frame = cv2.resize(frame, (640,360), cv2.INTER_AREA)#해상도 조절
    (frameHeight, frameWidth) = frame.shape[:2]
    print(frameHeight, frameWidth)
    h = frameHeight
    w = frameWidth

    # 모델에 입력을 크기
    inHeight = h
    inWidth = w

    # 아웃풋(스켈레톤 동영상 설정)
    output = cv2.VideoWriter(out_path, 0, fps, (w, h))

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    writer = None
    (f_h, f_w) = (h, w)
    zeros = None

    data = []
    previous_x, previous_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 15개의 부위
    pairs = [[0, 1],  # 머리
             [1, 2], [1, 5],  # 어깨
             [2, 3], [3, 4], [5, 6], [6, 7],  # 팔
             [1, 14], [14, 11], [14, 8],  # 엉덩이
             [8, 9], [9, 10], [11, 12], [12, 13]]  # 다리
    

    bnp_pairs = [[2, 3], [3, 4],  # 벤치프레스 or 풀업 선택 시 부위
                 [5, 6], [6, 7]]

    bnp_points = [2, 3, 4, 5, 6, 7]


    sqt_pairs = [[0, 1],         # 스쿼트 선택 시 부위
                 [1, 14], [8, 14],
                 [8, 9], [9, 10]]

    sqt_points = [0, 1, 8, 9, 10, 14]



    # 임계값
    thresh = 0.1

    # 점,선 색
    circle_color, line_color = (0, 255, 255), (0, 255, 0)

    # 진행률 표시
    widgets = ["비디오 변환 진행률: ", progressbar.Percentage(), " ",
               progressbar.Bar(), " ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval=n_frames,
                                   widgets=widgets).start()
    p = 0

    # 관절 움직임 저장 리스트
    frame_xy = [[0], [1], [2], [3], [4], [5],
                [6], [7], [8], [9], [10], [11],
                [12], [13], [14]]

    # 시작
    while True:
        ok, frame = cap.read()
        if ok != True:
            break

        frame = cv2.resize(frame, (w, h), cv2.INTER_AREA)
        frame_copy = np.copy(frame)

        # 네트워크 전처리
        inpBlob = cv2.dnn.blobFromImage(
            frame_copy, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
        net.setInput(inpBlob)
        output = net.forward()
        H = output.shape[2]
        W = output.shape[3]

        points = []
        x_data, y_data = [], []

        # 프레임별 데이터 저장 및 반복
        for i in range(15):
            probMap = output[0, i, :, :]
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
            x = (w * point[0]) / W
            y = (h * point[1]) / H

            if prob > thresh:
                points.append((int(x), int(y)))
                x_data.append(x)
                y_data.append(y)
            else:
                points.append((0, 0))
                x_data.append(previous_x[i])
                y_data.append(previous_y[i])

            #print(i," ",points[i][0], points[i][1],'',end='')


        if (exercise_Type == "벤치프레스" or exercise_Type == "풀업") :
            for pair in bnp_pairs:
                partA = pair[0]
                partB = pair[1]
                cv2.line(frame_copy, points[partA], points[partB],
                         line_color, 1, lineType=cv2.LINE_AA)

            for i in bnp_points:  # len(points)
                cv2.circle(frame_copy, (points[i][0],
                                        points[i][1]), 5, circle_color, -1)
                cv2.putText(frame_copy, str(
                    i), (points[i][0], points[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, lineType=cv2.LINE_AA)

                frame_xy[i].append((points[i][0], points[i][1]))

        elif exercise_Type == "스쿼트":
            for pair in sqt_pairs:
                partA = pair[0]
                partB = pair[1]
                cv2.line(frame_copy, points[partA], points[partB],
                         line_color, 1, lineType=cv2.LINE_AA)

            for i in sqt_points:  # len(points)
                cv2.circle(frame_copy, (points[i][0],
                                        points[i][1]), 5, circle_color, -1)
                cv2.putText(frame_copy, str(
                    i), (points[i][0], points[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, lineType=cv2.LINE_AA)

                frame_xy[i].append((points[i][0], points[i][1]))

        else:#아무 운동이 아닐시 모든 부위 딕텍션
            for pair in pairs:
                partA = pair[0]
                partB = pair[1]
                cv2.line(frame_copy, points[partA], points[partB],
                    line_color, 1, lineType=cv2.LINE_AA)
                

                
    
        if writer is None:
            writer = cv2.VideoWriter(out_path, fourcc, fps,
                                     (f_w, f_h), True)
            zeros = np.zeros((f_h, f_w), dtype="uint8")
        writer.write(cv2.resize(frame_copy, (f_w, f_h)))

        cv2.imshow('frame', frame_copy)

        data.append(x_data + y_data)
        previous_x, previous_y = x_data, y_data

        p += 1
        pbar.update(p)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # csv로 변환
    df = pd.DataFrame(frame_xy)
    df = df.transpose()
    df = df.drop(0)
    df.to_csv(csv_path, index=False)
    # print('저장완료')

    pbar.finish()
    cap.release()
    cv2.destroyAllWindows()

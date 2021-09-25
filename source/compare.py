import pandas as pd
import math
import numpy as np
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


#4구간 평균 각도 비교
def angle_parts(data,data2):#트레이너데이터, 유저 데이터
    T_data_length=len(data)
    
    T_first=np.mean(data[0:int(T_data_length*0.25)])
    T_second= np.mean(data[int(T_data_length*0.25):int(T_data_length*0.5)])
    T_third=np.mean(data[int(T_data_length*0.5):int(T_data_length*0.75)])
    T_last=np.mean(data[int(T_data_length*0.75):T_data_length-1])
    
    # print("트레이너")
    # print("0%~25% 평균 각도", T_first)
    # print("25%~50% 평균 각도", T_second)
    # print("50%~75% 평균 각도", T_third)
    # print("75%~100% 평균 각도", T_last)
    
    U_data_length=len(data2)
    U_first=np.mean(data2[0:int(U_data_length*0.25)])
    U_second= np.mean(data2[int(U_data_length*0.25):int(U_data_length*0.5)])
    U_third=np.mean(data2[int(U_data_length*0.5):int(U_data_length*0.75)])
    U_last=np.mean(data2[int(U_data_length*0.75):U_data_length-1])
    
    # print("유저")
    # print("0%~25% 평균 각도", U_first)
    # print("25%~50% 평균 각도", U_second)
    # print("50%~75% 평균 각도", U_third)
    # print("75%~100% 평균 각도", U_last)
    
    first_result=round(U_first/T_first*100,1)
    second_result=round(U_second/T_second*100,1)
    third_result=round(U_third/T_third*100,1)
    last_result=round(U_last/T_last*100,1)
    print("트레이너 대비 0%~25% 구간 평균각도 비율:",first_result)
    print("트레이너 대비 25%~50% 구간 평균각도 비율:",second_result)
    print("트레이너 대비 50%~75% 구간 평균각도 비율:",third_result)
    print("트레이너 대비 75%~100% 구간 평균각도 비율:",last_result)
    
    

#각도변화량 계산
def angle_change(U,T,E):#유저,트레이너,운동종류
    user_path=check_path(U,E)
    trainer_path=check_path(T,E)
    
    if E=="스쿼트":
        print("<스쿼트>-각도변화량")
        T_back_neck = angle(trainer_path, 14,1,0)#뒷목
        U_back_neck = angle(user_path,14,1,0)
        print("뒷목 각도 변화:")
        angle_parts(T_back_neck,U_back_neck)
        print()
        
        T_back_right_knee = angle(trainer_path, 10,9,8) # 오른쪽 뒷무릎
        U_back_right_knee = angle(user_path, 10,9,8)
        print("무릎 각도 변화:")
        angle_parts(T_back_right_knee,U_back_right_knee)
        print()
        
        T_spine = angle(trainer_path, 8,14,1)#척추
        U_spine= angle(user_path, 8,14,1)#척추
        print("척추 각도 변화:")
        angle_parts(T_spine,U_spine)
        print()
        
    elif E=="벤치프레스":
        print("<벤치프레스>-각도변화량")
        T_left_arm = angle(trainer_path, 2,3,4) # 왼팔
        T_right_arm = angle(trainer_path, 7,6,5) # 오른팔
        U_left_arm = angle(user_path, 2,3,4) # 왼팔
        U_right_arm = angle(user_path, 7,6,5) # 오른팔
        print("왼팔 각도 변화:")
        angle_parts(T_left_arm,U_left_arm)
        print()
        print("오른팔 각도 변화:")
        angle_parts(T_right_arm,U_right_arm)
        print()
        
#가동범위 출력 함수
def range_motion(U,T,E):#유저,트레이너,운동종류
    user_path=check_path(U,E)
    trainer_path=check_path(T,E)
    
    if E=="스쿼트":
        trainer_range=squat_angle(trainer_path)
        user_range=squat_angle(user_path)
        T_knee=max(trainer_range[1])-min(trainer_range[1])
        U_Knee=max(user_range[1])-min(user_range[1])
        print("<스쿼트>- 가동범위 비교 결과:")
        # print("트레이너 무릎 가동범위",T_knee)
        result=round((U_Knee/T_knee)*100,1)
        print("트레이너 대비 무릎 가동범위 비율:", result)
        print()
        # if 85<=result<=100 :
        #     print("참 잘했어요.")
        # elif result>100:
        #     print("너무 많이 움직였어요ㅠㅠ")
        # else:
        #     print("좀 더 움직이세요!")
        # print()
        
    elif E=="벤치프레스":
        trainer_range=benchpress_angle(trainer_path)
        user_range=benchpress_angle(user_path)
        T_right_angle=max(trainer_range[1])-min(trainer_range[1])
        T_left_angle=max(trainer_range[0])-min(trainer_range[0])
        U_right_angle=max(user_range[1])-min(user_range[1])
        U_left_angle=max(user_range[0])-min(user_range[0])
        
        print("<벤치프레스>- 가동범위 비교 결과:")
        # print("트레이너 왼팔 가동범위",T_left_angle)
        # print("트레이너 오른팔 가동범위",T_right_angle)
        # print("유저 왼팔 가동범위",U_left_angle)
        # print("유저 오른팔 가동범위",U_right_angle)
        
        left_result=round((U_left_angle/T_left_angle)*100,1)
        right_result=round((U_right_angle/T_right_angle)*100,1)
        print("트레이너 대비 왼팔 가동범위 비율:", left_result)
        print("트레이너 대비 오른팔 가동범위 비율:", right_result)
        print()
        
        # if 85<=left_result<=100 :
        #     print("왼팔: 참 잘했어요.")
        # elif right_result>100:
        #     print("왼팔: 너무 많이 움직였어요ㅠㅠ")
        # else:
        #     print("왼팔: 좀 더 움직이세요!")

        
        # if 85<=right_result<=100 :
        #     print("오른팔: 참 잘했어요.")
        # elif right_result>100:
        #     print("오른팔: 너무 많이 움직였어요ㅠㅠ")
        # else:
        #     print("오른팔: 좀 더 움직이세요!")
        # print()
       
#5분위수 반환 함수
def quintile(data):
    quintile=[]
    quintile.append(np.min(data))
    quintile.append(np.percentile(data,25))
    quintile.append(np.percentile(data,50))
    quintile.append(np.percentile(data,75))
    quintile.append(np.max(data))
    
    return quintile

#파일 경로 설정해주는 함수
def check_path(User_classification,exercise_Type):
    if User_classification=="trainer" and exercise_Type=="벤치프레스":
        path="./trainer/벤치프레스/트레이너_벤치프레스.csv"
    elif User_classification=="trainer" and exercise_Type=="스쿼트":
        path="./trainer/스쿼트/트레이너_스쿼트.csv"
    elif User_classification=="trainer" and exercise_Type=="풀업":
        path="./trainer/풀업/트레이너_풀업.csv"
    elif User_classification=="user" and exercise_Type=="벤치프레스":
        path="./user/벤치프레스/유저_벤치프레스.csv"
    elif User_classification=="user" and exercise_Type=="스쿼트":
        path="./user/스쿼트/유저_스쿼트.csv"
    elif User_classification=="user" and exercise_Type=="풀업":
        path="./user/풀업/유저_풀업.csv"
    else:
        print("파일이 없습니다.")
        return
    return path

#포인트 이동 중 (0,0)으로 튄 포인트 찾아서 보정 후 다시 저장, 필요없는 문자제거
def check(User_classification,exercise_Type):
    
    path=check_path(User_classification,exercise_Type)
    data = pd.read_csv(path)
    row,column =data.shape
    row=int(row)
    column=int(column)

    for i in range(column):
        for j in range(row):
            try:
                data[str(i)][j]=data[str(i)][j].replace("(","")#(제거
                data[str(i)][j]=data[str(i)][j].replace(")","")#)제거
                
                if data[str(i)][j] =='0, 0':#0,0이 있으면 이전 값 저장
                    data[str(i)][j]=data[str(i)][j-1]
            except:
                continue

                
                
    data.to_csv(path,header=True,index=False)#csv로 다시 저장
     
#csv 파일 경로와 3부위를 입력받아 angle을 구하는 함수-맞는 알고리즘인지 코드검수 필요
def angle(path,first,second,third):
    data = pd.read_csv(path)
    row,column=data.shape
    angle_list=[]
    
    #원하는 3지점 데이터 받아오기
    first_list=data[str(first)]
    second_list=data[str(second)]
    third_list=data[str(third)]
    
    for i in range(int(row)):
        #프레임별 위치 데이터 불러오기
        f_x,f_y=map(int,(first_list[i].split(",")))
        s_x,s_y=map(int,(second_list[i].split(",")))
        t_x,t_y=map(int,(third_list[i].split(",")))
    
        s_to_f=(f_x-s_x,f_y-s_y)#second-first
        s_to_t=(t_x-s_x,t_y-s_y)#second-third
        
        dot=s_to_f[0]*s_to_t[0]+s_to_f[1]*s_to_t[1]
        det=s_to_f[0]*s_to_t[1]-s_to_f[1]*s_to_t[0]
        
        theta=np.rad2deg(np.arctan2(det, dot))
        
        if theta < 0:
            theta=theta+360.0
            
        angle_list.append(theta)


    
    return angle_list

#전프레임에서 다음프레임 부위 이동방향 구하는 함수
def direct(User_classification,exercise_Type):
    data = pd.read_csv(check_path(User_classification,exercise_Type)) #check path
    row_count=len(data) #프레임수
    df_new=pd.DataFrame()
    
    for i in range(0,15):
        df=pd.DataFrame(columns=["id",i])
        for j in range(0, row_count-1):
            
            #처음 좌표
            data_1=data.iat[j,i]
            if pd.isnull(data_1):
                continue
            
            x1,y1=data_1.split(", ")
            x1,y1=int(x1),int(y1)
        
            data_2=data.iat[j+1,i]
            x2,y2=data_2.split(", ")
            x2,y2=int(x2),int(y2)
            
        

            a=math.atan2(-(y2-y1),x2-x1)*(180/math.pi) # 방위각 계산, cv좌표계 -> y축변환
            
            if x1==x2 and y1==y2:
                direct="" #움직임 변화가 없을때
            elif -22.5<=a<=22.5: 
                direct=1 # →
            elif 22.5<a<=67.5: 
                direct=2 # ↗
            elif 67.5<a<=112.5:
                direct=3 # ↑
            elif 112.5<a<=157.5:
                direct=4 # ↖
            elif -180<a<=-157.5 or 157.5<a<=180:
                direct=5 # ←
            elif -157.5<a<=-112.5: 
                direct=6 # ↙
            elif -112.5<a<=-67.5: 
                direct=7 # ↓
            elif -67.5<a<-22.5:
                direct=8 #↘
        
            df= df.append(pd.DataFrame([[j,direct]], columns=["id",i]), ignore_index=True)
        df_new=df_new.append(df[i])
    
    df_new=df_new.transpose()
    
    #경로에 방향 csv 저장
    if User_classification=="trainer" and exercise_Type=="벤치프레스":
        df_new.to_csv("./trainer/벤치프레스/트레이너_벤치프레스_방향.csv", index = False)
    elif User_classification=="trainer" and exercise_Type=="스쿼트":
        df_new.to_csv("./trainer/스쿼트/트레이너_스쿼트_방향.csv", index = False)
    elif User_classification=="trainer" and exercise_Type=="풀업":
        df_new.to_csv("./trainer/풀업/트레이너_풀업_방향.csv", index = False)
    elif User_classification=="user" and exercise_Type=="벤치프레스":
        df_new.to_csv("./user/벤치프레스/유저_벤치프레스_방향.csv", index = False)
    elif User_classification=="user" and exercise_Type=="스쿼트":
        df_new.to_csv("./user/스쿼트/유저_스쿼트_방향.csv", index = False)
    elif User_classification=="user" and exercise_Type=="풀업":
        df_new.to_csv("./user/풀업/유저_풀업_방향.csv", index = False)
    else:
        print("파일이 없습니다.")
        return
    
    return df_new

#움직인 방향, 변하는 점 개수 알려주는 함수
#direction함수 선 실행 필수☆
def move_direct(User_classification,exercise_Type):
    
    if User_classification=="trainer" and exercise_Type=="벤치프레스":
        path="./trainer/벤치프레스/트레이너_벤치프레스_방향.csv"
        print("트레이너 - 벤치프레스")
    elif User_classification=="trainer" and exercise_Type=="스쿼트":
        path="./trainer/스쿼트/트레이너_스쿼트_방향.csv"
        print("트레이너 - 스쿼트")
    elif User_classification=="trainer" and exercise_Type=="풀업":
        path="./trainer/풀업/트레이너_풀업_방향.csv"
        print("트레이너 - 풀업")
    elif User_classification=="user" and exercise_Type=="벤치프레스":
        path="./user/벤치프레스/유저_벤치프레스_방향.csv"
        print("유저 - 벤치프레스")
    elif User_classification=="user" and exercise_Type=="스쿼트":
        path="./user/스쿼트/유저_스쿼트_방향.csv"
        print("유저 - 스쿼트")
    elif User_classification=="user" and exercise_Type=="풀업":
        path="./user/풀업/유저_풀업_방향.csv"
        print("유저 - 풀업")
    else:
        print("방향 파일이 없습니다.")
        return
    
    data = pd.read_csv(path)
    
    if exercise_Type=="벤치프레스":
        measure_body = [2, 3, 4, 5, 6, 7] #4,7:손목 3,6:팔꿈치 2,5:어깨
    elif exercise_Type=="스쿼트":
        measure_body = [8, 9, 14] #8:엉덩이 9:무릎 14:명치
       
    for i in measure_body:
        list=[]
        for j in range(0,len(data)-1):
            direct=data.iat[j,i]
            
            if direct==1: direct="→"
            elif direct==2: direct="↗"
            elif direct==3: direct="↑"
            elif direct==4: direct="↖"
            elif direct==5: direct="←"
            elif direct==6: direct="↙"
            elif direct==7: direct="↓"
            elif direct==8: direct="↘"
            
            if pd.notnull(direct):
                list.append(direct)
            for k in range(0,len(list)-1):
                if list[k]==list[k+1]:
                    del list[k+1]
        print("[{}] direct:{} \nchanged point count:{}".format(i,list,len(list)-1))
        
# 운동 부위별 각도 계산
# 1. 벤치프레스
def benchpress_angle(path):
    
    left_arm = angle(path, 2,3,4) # 왼팔
    right_arm = angle(path, 7,6,5) # 오른팔
    
    #5분위수 저장-왼쪽 팔,오른쪽팔
    benchpress_left_angle=quintile(left_arm)
    benchpress_right_angle=quintile(right_arm)
    
    #5분위수 리턴
    return [benchpress_left_angle , benchpress_right_angle]

# 2. 스쿼트
def squat_angle(path):
    
    back_neck = angle(path, 14,1,0)#뒷목
    back_right_knee = angle(path, 10,9,8) # 오른쪽 뒷무릎
    spine = angle(path, 8,14,1)#척추
    
    #5분위수 계산
    squat_neck=quintile(back_neck)
    squat_right_knee=quintile(back_right_knee)
    squat_spine=quintile(spine)
    
    return [squat_neck,squat_right_knee,squat_spine]
   
    
    
    

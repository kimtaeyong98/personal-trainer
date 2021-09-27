import get_video_csv
import compare
import numpy as np
def result(exercise_Type):#1 2 3 단계 종
    if exercise_Type=="스쿼트":
        print("<스쿼트>-가동범위")
        squat_result_1=compare.range_motion("user","trainer",exercise_Type)#스쿼트 1단계
        if 85<=squat_result_1<=115:
            print("스쿼트 무릎 가동범위 비율:",squat_result_1,"\n")

            #2단계 실행 공간
            score,detail=compare.angle_change("user","trainer",exercise_Type)
            print(exercise_Type,"총점수:",score,"\n")
            print("자세히보기")
            for i in detail:
                print(i)
            
            print("<스쿼트>-방향변화율")
            compare.direct("trainer",exercise_Type)
            compare.direct("user",exercise_Type)
            compare.move_direct("trainer",exercise_Type)
            compare.move_direct("user",exercise_Type)
            
        else:
            print("스쿼트 무릎 가동범위 비율:",squat_result_1)
            print("가동범위를 신경써서 다시 촬영하세요.")
        
    elif exercise_Type=="벤치프레스":
        print("<벤치프레스>-가동범위")
        benchpress_result_l, benchpress_result_r=compare.range_motion("user","trainer",exercise_Type)
        if 85<=benchpress_result_l<=115 and 85<=benchpress_result_r<=115:
            print("벤치 왼팔 가동범위 비율:",benchpress_result_l)
            print("벤치 오른쪽 가동범위 비율:",benchpress_result_r,"\n")
            #2단계 실행 공간
            score,detail=compare.angle_change("user","trainer",exercise_Type)
            print(exercise_Type,"총점수:",score,"\n")
            print("자세히보기")
            for i in detail:
                print(i)
            compare.direct("trainer",exercise_Type)
            compare.direct("user",exercise_Type)
            compare.move_direct("trainer",exercise_Type)
            compare.move_direct("user",exercise_Type)
            
        else:
            print("벤치 왼팔 가동범위 비율:",benchpress_result_l)
            print("벤치 오른쪽 가동범위 비율:",benchpress_result_r)
            print("가동범위를 신경써서 다시 촬영하세요.")


#main
#get_video_csv.get_video("스쿼트","user")#user 스켈레톤 동영상과 csv 얻기
#get_video_csv.get_video("스쿼트","trainer")#trainer 스켈레톤 동영상과 csv 얻기

#get_video_csv.get_video("벤치프레스","user")#user 스켈레톤 동영상과 csv 얻기
#get_video_csv.get_video("벤치프레스","trainer")#trainer 스켈레톤 동영상과 csv 얻기


#0,0 체크(전처리)
#compare.check("trainer","스쿼트")
#compare.check("trainer","벤치프레스")
#compare.check("user","스쿼트")
#compare.check("user","벤치프레스")

result("스쿼트")
print()
result("벤치프레스")


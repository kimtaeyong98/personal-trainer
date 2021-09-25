import get_video_csv
import compare
import numpy as np

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



#가동범위
compare.range_motion("user","trainer","스쿼트")
compare.range_motion("user","trainer","벤치프레스")

#각도 변화율
compare.angle_change("user","trainer","스쿼트")
compare.angle_change("user","trainer","벤치프레스")

#방향 변화
compare.direct("trainer","스쿼트")
compare.move_direct("trainer","스쿼트")
compare.direct("trainer","벤치프레스")
compare.move_direct("trainer","벤치프레스")



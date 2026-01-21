# 베이스 이미지 설정
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /deploy

# Python 스크립트 및 텍스트 파일 복사
COPY ./deploy /deploy/

# Flask 설치
RUN pip install flask pyjwt

RUN FLAG=$(cat /dev/urandom | tr -dc 'a-z' | fold -w 4 | head -n 1); mv /deploy/flag.txt /deploy/flag_$FLAG.txt

EXPOSE 13000
# main.py 실행
CMD ["python", "/deploy/main.py"]
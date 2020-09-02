#!/bin/bash
# setup.sh
# 확장자 sh 파일을 shell script 파일이라고 부릅니다.
user=$1
password=$2
port=$3
if [[-z "${user}" ] || [ -z "${password}" ] || [ -z "${port}" ]]; then
    echo "MongoDB ID/PW, 포트 번호를 입력해주세요."
    echo "실행법"
    # sudo bash ./setup.sh {몽고DB 관리자 ID} {몽고DB 관리자 암호} {flask 포트 설정}
    # e.g. sudo bash ./setup.sh admin admin1234 5000
    exit 1
fi
# 프로젝트에 적용할 MongoDB 설정파일(/etc/mongod.conf)
mongod_conf="
# mongod.conf
# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/
# Where and how to store data.
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
#  engine:
#  mmapv1:
#  wiredTiger:
# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
# network interfaces
net:
  port: 27017
  bindIp: 0.0.0.0
# how the process runs
processManagement:
  timeZoneInfo: /usr/share/zoneinfo
security:
  authorization: enabled
#operationProfiling:
#replication:
#sharding:
## Enterprise-Only Options:
#auditLog:
#snmp:"
# 1. python3 대신 python 명령어 사용
# 우분투 리눅스의 python 명령어는 python 2.7 버전을 실행시킵니다.
# 스파르타 코딩 클럽의 프로젝트는 python 3 이상 버전을 사용하기 때문에
# 사용의 편의성을 위해 python 명령어로 python 3 이상 버전을 실행시키도록 설정합니다.
echo "python 명령어 실행 준비"
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
echo "python 명령어 실행 준비 완료"
# 2. MongoDB 설치
echo "MongoDB 설치"
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add - &&
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list &&
    sudo apt-get update &&
    sudo apt-get install -y mongodb-org
sudo service mongod start
echo "MongoDB 설치 완료"
# 3. pip 설치
# pip 명령어는 파이참에서 외부 패키지를 설치하던 것을 명령어로 할 수 있게끔 도와줍니다.
echo "pip 명령어 실행 준비"
sudo apt-get update
sudo apt-get install -y python3-pip
# python3 -> python 작업처럼 pip도 pip3 -> pip 명령어로 실행할 수 있도록 설정합니다. (2.7 버전이 아닌 3 버전으로 실행)
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
echo "pip 명령어 실행 준비 완료"
# 4. MongoDB 어드민 유저 생성
# 이미 어드민 유저가 있을 경우에는아래 코드 사용
# mongo admin -u my_admin_user -p my_admin_password --eval "db.createUser({user: 'test1', pwd: 'test1', roles:['root']});"
mongo admin --eval "db.createUser({user: '${user}', pwd: '${password}', roles:['root']});"
echo -e "${mongod_conf}" >/etc/mongod.conf
sudo service mongod restart
echo "MongoDB 설정 완료(관리자 아이디 ${user} 비밀번호 ${password})"
# 5. 포트 포워딩
# 외부 포트 접속 요청의 포트를 변환합니다.
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port ${port}
echo "80 포트 -> ${port} 포트로 포트 포워딩 완료"
# 파이썬 사용 안내
echo "#서버 실행 예시"
echo "nohup python app.py &"
echo "# 아래 명령어로 미리 pid 값(프로세스 번호)을 본다"
echo "ps -ef | grep 'python'"
echo "# pid 값 사용해 서버 종료"
echo "kill -9 [pid값]"
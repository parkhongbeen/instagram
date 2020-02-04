#!/usr/bin/env python
import subprocess

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    # background로 실행하는 옵션 추가
    ('-d', ''),
    ('-p', '8001:80'),
    ('--name', 'instagram'),
]
DOCKER_IMAGE_TAG = 'pack122/wps-instagram'

subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)
subprocess.run(f'docker stop instagram', shell=True)

# secrets.json이 없는 상태로 docker run으로 bash를 실행 -> background로 들어감
subprocess.run('docker run {options} {tag} /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)

# secrets.json을 전송
subprocess.run('docker cp secrets.json instagram:/srv/instagram', shell=True)

# bash실행
subprocess.run('docker exec -it instagram /bin/bash', shell=True)

# runserver명령을 전송
# subprocess.run('docker exec -it instagram python manage.py runserver 0:8000', shell=True)

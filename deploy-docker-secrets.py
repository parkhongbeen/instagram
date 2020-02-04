#!/usr/bin/env python
# 1. Host에서 이미지 build, push
# 2. EC2에서 이미지 pull, run(bash)
# 3. Host -> EC2 ->Container를 secrets.json전송
# 4. Container에서 runserver
import os
import subprocess
from pathlib import Path

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    # background로 실행 종료
    ('-d', ''),
    ('-p', '80:8000'),
    ('--name', 'instagram'),
]

DOCKER_IMAGE_TAG = 'pack122/wps-instagram'

subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)
subprocess.run(f'docker stop instagram', shell=True)

subprocess.run('docker run {options} {tag} /bin/bash'. format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)

subprocess.run('docker cp secrets.json instagram:/srv/ins')

subprocess.run()
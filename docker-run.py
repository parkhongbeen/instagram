#!/usr/bin/env python
# 도커 이미지에 secrets.json이 포함
import subprocess

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-p', '8001:8000'),
    ('--name', 'instagram'),
]
DOCKER_IMAGE_TAG = 'azelf/wps-instagram'

subprocess.run(f'poetry export -f requirements.txt > requirements.txt', shell=True)
subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)
subprocess.run(f'docker stop instagram', shell=True)
subprocess.run('docker run -d {options} {tag} /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)
subprocess.run(f'docker cp secrets.json instagram:/srv/instagram', shell=True)
subprocess.run('docker exec -it instagram /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)
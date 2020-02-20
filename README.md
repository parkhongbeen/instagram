- # Instagram

  ## Requirements

  - Python (>3.6)
  - Secrets JSON File

  ## Installation

  ```
  pip install -r requirements.txt
  ```

  ## Secrets JSON File

  ```
  /secrets.json
  {
    "AWS_ACCESS_KEY_ID": "<AWS AccessKeyID (S3 permission)>",
    "AWS_SECRET_ACCESS_KEY": "<AWS SecretAccessKey (S3 permission)>"
  }
  ```

  ## Run development server

  ```
  python manage.py runserver
  ```

  ## EC2에 Docker배포

  1. 로컬에서 이미지 생성, 실행 확인
  2. DockerHub에 저장소 생성
  3. 로컬 이미지에 태그 추가
     `docker tag <로컬이미지명> <저장소명>`
  4. DockerHub에 이미지 Push
     `docker push <저장소명>`
  5. EC2에 Docker설치
  6. EC2에서 docker run명령어 실행
     `docker run --rm -it -p 80:8000 <저장소명>`

  docker설치 및 run명령어 실행하는 부분을 `deploy-docker.sh` 안에 적절히 작성하기

  ## API문서

  Base URL: `https://lhy.kr/api`

  ### 인증

  #### Basic Auth

  HTTP의 Basic Authentication을 사용

  HTTP Header의 `Authorization` 키에 `Basic ` 값을 넣어 전송

  ``에 들어가는 값은 **"username:password"** 문자열을 Base64로 인코딩 한 값

  ex)

  ```
  Authorization: Basic SEFSDFK@#JSDOFOPASODPFI!@@#OP{SDFSDF}
  ```

  #### Token Auth

  [DRF라이브러리](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)에서 제공하는 토큰 인증 방식

  HTTP Header의 `Authorization` 키에 `Token ` 값을 넣어 전송

  ``에 들어가는 값은 Token을 발급받는 API (AuthTokenAPI)에 자격증명(일반적으로 username과 password)를 전달 후 받은 **token**값을 사용

  클라이언트에서는 해당 **token**을 로그인을 유지하는 동안 로컬 저장소에 저장 후, 매 HTTP Request마다 Header에 인증값을 전송하는 형태로 세션 유지

  ex) 전송하는 HTTP Header의 형태

  ```
  Authorization: Token SFEKLKFJDKFJSKDFSKDF
  ```

  ex) curl을 사용해서 테스트 하는 법

  ```
  curl -X GET https://<실제HOST>/api/example/ -H 'Authorization: Token <Token vaue>
  ```

  ### posts

  ### posts

  #### Post List

  - URL: `/posts/`

  - Method: `GET`

  - Query Params

    - ordering (String)
      - asc: 오름차순 정렬
      - desc: 내림차순 정렬
    - page (Integer)
      - 해당 페이지

  - Request Sample

    URL: https://lhy.kr/api/posts/?ordering=asc&page=3

  - Response Sample

    ```
    [
        {
            "pk": 14,
            "author": {
                "pk": 3,
                "username": "moonpeter"
            },
            "content": "TestContent",
            "postimage_set": [
                3974,
                3973,
                3972
            ]
        },
        {
            "pk": 13,
            "author": {
                "pk": 3,
                "username": "moonpeter"
            },
            "content": "TestContent",
            "postimage_set": [
                3974,
                3973,
                3972
            ]
        }
    ]
    ```
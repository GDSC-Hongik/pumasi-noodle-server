# Pumasi Backend
## 개발 환경
- Python (3.11.3)
- Django (4.0)
- Django Rest Framework (3.13.1)
- Firebase Admin (6.3.0)
- Django Dotenv (1.4.2)

코드잇에서 수강했던 [DRF강의 개발환경](https://www.codeit.kr/topics/django-rest-framework/lessons/5826) 을 참고하였습니다.

## 장고 환경 구성
- Project Name : Pumasi

- Apps    

  |   앱 이름    |             설명              |   
  |:---------:|:---------------------------:|   
  |   Care    | '맡기', '맡기기' 데이터 CRUD API 담당 |   
  |   User    |        미구현 (앱 이름 가칭)        |   
  | Community |        미구현 (앱 이름 가칭)        |
  |   Chat    |        미구현 (앱 이름 가칭)        |

## 실행 방법
1. 아래 코드를 실행하여 필요한 라이브러리를 설치합니다.   
    ```
    pip install django==4.0 djangorestframework==3.13.1
    pip install firebase-admin django-dotenv
    pip install pyrebase4
    ```

    ```pyrebase4```를 설치할 때 jws 라이브러리를 설치하면서 decode 에러가 발생할 수 있습니다.   
    [이 게시글](https://wesely.github.io/pip,%20python,%20pip/Fix-'cp950'-Error-when-using-'pip-install'/)을 참고하여 아래와 같은 순서로 해결할 수 있습니다.   
   1.  jws 라이브러리를 '다운'받습니다. (설치x)
       ```
       pip download jws
       ```
       만약 다운받은 라이브러리가 캐시에 이미 저장되어 있어 동일한 오류가 계속 발생하는 경우, [이 사이트](https://pypi.org/project/jws/) 에서 파일을 직접 다운로드 받을 수 있습니다.
   2.  다운로드 받은 파일을 압축해제 합니다.
   3.  ```setup.py``` 의 다음 코드를 아래와 같이 수정합니다. 
       ```(python)
       (수정 전)
        return open(os.path.join(os.path.dirname(file), fname).read()
       (수정 후)
       return open(os.path.join(os.path.dirname(file), fname), encoding=”UTF-8”).read()
       ```
   4. 전체 라이브러리 소스코드를 ```.tar``` 형식으로 압축합니다. (이름은 원하는대로)
   5. 다음 코드를 실행합니다.
      ```
      pip install filename.tar # filename 은 자신이 지었던 이름
      ```
   6. 이제 ```jws``` 라이브러리가 설치되었으므로 다시 한번 ```pyrebase4``` 를 설치합니다.
      ```
      pip install pyrebase4
      ```

2. 이 레포지토리의 최신 코드를 다운받습니다.   
   - 최초 실행   
   ```
   git clone https://github.com/GDSC-Hongik/pumasi-noodle-server.git
   ```
   - 최초 실행 이후에 실행 시   
   ```
   git pull https://github.com/GDSC-Hongik/pumasi-noodle-server.git
   ```
3. 레포지토리를 그대로 받은 뒤
    ``` cd "pumasi"``` 를 실행하여 프로젝트 폴더로 이동합니다.
4. 공유받은 .env 파일을 이동한 폴더에 추가합니다. (manage.py 와 같은 디렉토리에 있는지 확인합니다.)  
5. ```python manage.py runserver``` 을 실행합니다.
6. http://127.0.0.1:8000/test/ 에서 아래 화면이 나오는지 확인합니다.   
    ![img.png](img.png)   
    24년 1월 9일 01:00 기준 데이터베이스에는 아래 이미지와 같은 형태로 데이터가 들어있습니다.      
    ![img_1.png](img_1.png)   
    데이터베이스의 test 문서에 저장된 값과 동일한 리턴이 나오도록 테스트 코드를 작성하였습니다.   
7. 위 화면과 같이 잘 나온다면, 프론트에서 __runserver 명령어가 실행된 상태에서__ 위 주소에 GET 요청을 보냈을 때 위 이미지와 같은 형태의 JSON 데이터를 반환받습니다. 

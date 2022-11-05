# talk-kiosk-flask_server

<img src="https://img.shields.io/badge/%E2%80%BB-%EC%A3%BC%EC%9D%98%EC%82%AC%ED%95%AD-yellow" />\
본 서버은 AWS 프리티어 서비스로 운영되는 학습용 서버입니다.\
관계자가 아닌 분의 무분별한 API호출은 자제 부탁드립니다...!

<a href="https://github.com/Fantastic5-Team/talk-kiosk-flask_server/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/Fantastic5-Team/talk-kiosk-flask_server"></a>\
<a href="https://github.com/Fantastic5-Team/talk-kiosk-flask_server/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/Fantastic5-Team/talk-kiosk-flask_server"></a>\
<a href="https://github.com/Fantastic5-Team/talk-kiosk-flask_server/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Fantastic5-Team/talk-kiosk-flask_server?color=yellow"></a>\
<a href="https://github.com/Fantastic5-Team/talk-kiosk-flask_server"><img alt="GitHub license" src="https://img.shields.io/github/license/Fantastic5-Team/talk-kiosk-flask_server"></a>

## 개요
말하는 사이에 주문 완료! 프로젝트의 플라스크 서버 리파지토리 입니다!

클라이언트 리파지토리\
<a href="https://github.com/Fantastic5-Team/talk-kiosk-client" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-talk--kiosk--client-brightgreen?style=for-the-badge&logo=github" />
</a>\
서버 리파지토리\
<a href="https://github.com/Fantastic5-Team/talk-kiosk-server" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-talk--kiosk--server-brightgreen?style=for-the-badge&logo=github" />
</a>

## API
### BASE_URL: (미정)

### 1. 메뉴 주문
  `[POST]` /order
  ```json
  // body
  {
    "text": "빅맥 라지세트 하나랑 치즈버거 "
  }
  ```
  ```json
  // return
  {
    "order_list": 
    [
      {
        "menu": [111],
        "option": [],
        "set": [202, 302],
        "qty": 1
      },
      {
        "menu": [101, 102, 103, 104],
        "option": [],
        "set": [],
        "qty": 2
      }
    ],
    "code": 1001
  }
  ```
  
### 2. 메뉴 이름 충돌시 하나만 선택
  `[POST]` /order/conflict
  ```json
  // body
  {
    "text": "2번 (또는 더블 쿼터파운더 치즈버거)",
    "menu_id": [101, 102, 103, 104]
  }
  ```
  ```json
  // return
  {
    "resolve": 102,
    "code": 2002
  }
  ```
  
### 3. 옵션 변경
  `[POST]` /option
  ```json
  // body
  {
    "text": "피클빼고 패티 추가해줘"
  }
  ```
  ```json
  // return
  {
    "option": [2001, 2004],
    "code": 2003
  }
  ```
  
### 4. 세트 변경
  `[POST]` /set
  ```json
  // body
  {
    "text": "해쉬브라운이랑 환타",
    "set": [201, 301]
  }
  ```
  ```json
  // return
  {
    "set": [205, 307],
    "code": 2005
  }
  ```

### 5. 주문 확인
  `[POST]` /confirm
  ```json
  //body
  {
    "text" "네"
  }
  ```
  ```json
  //return
  {
  "code":2008
  }
  ```

### 6. 매장내 식사 유무
  `[POST]` /takeout
  ```json
  //body
  {
    "text" "네"
  }
  ```
  ```json
  //return
  {
  "code":1001,
  "anwer": True
  }
  ```



## 코드표
> | 코드 | 설명 |
> |---|---|
> | 1001 | 성공 |
> | 1002 | 분석 실패 |
> | 2001 | 주문완료 |
> | 2002 | 충돌해결 |
> | 2003 | 옵션변경 |
> | 2004 | 옵션완료 |
> | 2005 | 세트변경 |
> | 2006 | 세트완료 |
> | 2007 | 세트충돌 |
> | 2008 | 확인완료 |
> | 2009 | 메뉴 선택 리스트에 없음|
>
> 단, 1003 부터는 클라이언트 내부적으로 사용하고 있는 코드입니다.\
> 따라서, 1003 부터의 코드 사용은 하지 말아주세요.

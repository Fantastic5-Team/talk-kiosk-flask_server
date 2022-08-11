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
(개발 중)

## 데이터 양식
> ### 데이터 양식 설명
> `ordered`: 주문 정보 객체 (서버 데이터 양식 참조)\
> `situation`: 상황에 대한 정보 (완료됬는지, 여러개 음식 중 하나를 선택하도록 해야하는지, 처리할 수 없는 요청이든지...)
> #### `situation` 코드표
> | 코드 | 설명 |
> |---|---|
> | 1000 | 처리 완료 |
> | 2001 | 사용자의 요청 |
> | 2002 | 메뉴(, 옵션 등) 충돌 (해당 문자가 포함된 메뉴가 2개 이상 존재시) |
> | 2003 | 옵션 선택 요청 |
> | 2004 | 세트 선택 요청 |
> | 4000 | 통신 에러 |
> | 4001 | 사용자의 의도를 파악하지 못한 경우 |
>
> `data`: 여러개의 음식 중 하나를 고르게 하기 위한 상황에서 여러 음식(, 옵션)에 대한 id값\
> `voiceText`: 사용자의 음성 텍스트

```json
{
  "jsonInfo": {
    "ordered": {서버 데이터 양식 참조},
    "situation": 1000,
    "data": [1, 2, 3],
    "voiceText": "불고기 버거 하나 주십시오.",
  }
}
```

---
tags:
- 작업일지
- obsidian
- gatsby
date: 2022-06-04, 17:55:14
update: 2022-06-18, 18:43:28
title: Obsidian과 Gatsby로 홈페이지 만들기
---
## TL;DR
기록하기 위해 여러가지 플랫폼을 찾던 중 [Obsidian](https://obsidian.md/)이 있다는 것을 알았다. 몇번 테스트로 사용해보고는 이것을 사용하고자 마음을 먹었다. 이유는 다음과 같다.  

1. 문서 작성도구는 마크다운 형식이어야 한다.
2. 깃허브를 통해 홈페이지를 만들 수 있어야 한다.
3. 문서 생성에 관해서 템플릿이 있는 것이 좋다.

이 부분에 대해서 만족했기 때문에 사용해보고자 한다.

## Obsibian Template for Gatsby Theme Primer Wiki 사용하기.

Obsidian을 gatsby로 배포할 수 있게 해주는 오픈소스이다.

시작하는 방법은 다음과 같다. 우선 Obsidian 보관함이 있다고 가정하에 진행한다.

1. [깃허브 저장소](https://github.com/theowenyoung/obsidian-template-gatsby-theme-primer-wiki)을 로컬에 클론한다.
	```shell
	git clone https://github.com/theowenyoung/obsidian-template-gatsby-theme-primer-wiki.git
	```
2. Obsidian 보관함에 `.layouts`, `.github`, `.gitignore`을 복사한다.

## 로컬에서 확인하기.

```shell
cd .layouts
npm i
npm start
```
- `npm i` 명령어를 사용해 `package.json` 의존성 패키지를 설치한다.
- `npm start`로 실행하면 된다.

로컬에서 동작하는 것을 확인할 수 있다.

## 배포하기
### Path Prefix
나는 wiki라는 레파지토리를 만들어서 사용할 것이다. 이럴 경우 url은 `{깃아이디}.github.io/wiki`이다. 하지만 배포해보면 url 처리는 `{깃아이디}.github.io`로 된다. 사이트 url뒤에 `/wiki`를 고정시키기 위해서는 다음과 같이 설정해야한다.
1. `gatsby-config.js` 을 `pathPrefix` 저장소 이름으로 변경한다.
```js
module.exports = {
pathPrefix: `[저장소 이름]`,
}
```
2. `package.json` 을 변경한다.
- `"build": "gatsby build --prefix-paths"`
- 로컬 미리보기 : `"serve": "gatsby serve --prefix-paths"`

## Github 설정
아래와 같이 작업 후 Git에 푸시하면 된다. 그 후 레파지토리 `setting -> pages` 에서 `source`를 `gh-pages`로 설정하면 된다.

깃허브 액션 후 사이트가 배포되면 url로 입력해서 확인하면 된다.
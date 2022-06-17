---
tags:
- GithubAction
- Python
- github
- git
- 작업일지
date: 2022-06-13, 20:38:39
update: 2022-06-13, 22:42:06
title: Github Actions을 이용하여 Twitter에 자동으로 글쓰기
---
## TL;DR
블로그를 포스팅하고 트위터에 글쓰는 것은 너무 귀찮다고 생각한다. 그래서 깃허브에 푸시를 하면 자동으로 트위터에 글을 쓰도록 한다.

## Github Actions 이용하기
Github Actions은 github에서 제공하는 워크플로우를 자동화하도록 도와주는 도구이다. 이것을 이용하면 다양한 작업들을 자동화하여 처리할 수 있다.

그렇다면 푸시를 할 때 트위터에 글을 쓰는 스크립트를 실행하도록 설정하면 된다.
``` yml
# .github/workflows/Tweet.yml
name: Tweet

on:
  push:
    branches:
      - main
```
나는 main 브런치에 커밋을 할 때만 진행하도록 했다.

## 최신 커밋 정보 가져오기
포스팅을 할 때 새로 커밋한 파일에 대한 것만 트위터에 글을 쓰고 싶다. `git diff`명령어와 옵션을 사용하면 최신 커밋 정보를 가져올 수 있다.
``` shell
$ git diff --name-status HEAD~1
A       Attachments/스크린샷 2022-06-12 오후 8.12.22.png
A       Test/트윗 테스트.md
```
- `--name-status` : 변경 유형과 파일 이름을 알 수 있다.
- `HEAD~1` :  최근 커밋의 변경 사항을 확인할 수 있다.

파일명의 접두사로 커밋의 변경 상태를 알 수 있다.
- `A` : 추가 / 새파일
- `M` : 수정 / 편집
- `D` : 삭제 / 제거 

나는 새로 추가된 파일 중 마크다운 문서의 이름만 가져오고 싶다. `grep` 명령어를 사용하면 된다. `grep`은 원하는 문자열이 들어간 행을 찾아 출력해준다. `grep`를 통해 새로 추가된 파일을 알아낸다. 그 후 `cut` 명령어를 이용해 필요없는 부분을 제거한다. 
```shell
$ git diff --name-status HEAD~1 | grep "^A" | grep ".md$" | cut -c 3-
Test/트윗 테스트.md
```
- `grep "^A"` : A로 시작되는 경우 출력.
- `grep ".md$"` : md로 시작하는 확장자를 가진 경우에만 출력.
- `cut -c 3-` : 3번째 위치에서 끝까지 문자열을 잘라낸다.

이제 최신 커밋의 파일명을 가져올 수 있다.

## 트위터 개발자 등록 및 라이센스 발급
트위터 API를 사용하기 위해서는 트위터 개발자 등록과 라이센스를 발급해야한다.
[Twitter Developer Platform](https://developer.twitter.com/en) 가입 후 프로젝트를 생성하여 앱을 추가해준다. 그사용자 인증은 **OAuth1.0a**로 활성화 해주면 된다. 	`access token`, `access secret token`을 발급 받는다. 해당 부분은 https://jamong-yami.postype.com/post/11433954 페이지에서 자세히 알 수 있다.
필요한 키는 `API Key`, `API Key Secret`, `Access Token`, `Access Secret Token` 이다.

## 트위터 쓰기 코드 작성
나는 `Python`을 사용하여 트위터에 글쓰는 코드를 작성했다. 파이썬을 사용한 이유는 조금 익숙한 언어이며 트위터 API를 제공하는 `tweepy` 라이브러리를 사용할 수 있기 때문이다.
매우 간단하게 코드를 작성했다. 
``` python
# AutoTweet.py
import sys
import os
import frontmatter
import tweepy

import urllib.parse

def OAuth():
	API_KEY = os.environ.get('TWITTER_API_KEY')
	API_KEY_SECRET = os.environ.get('TWITTER_API_SECRET')
	ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')
	ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

	client = tweepy.Client(consumer_key= API_KEY,consumer_secret= API_KEY_SECRET,access_token= ACCESS_TOKEN,access_token_secret= ACCESS_SECRET)
	return client

def GetTweetText(file):
	site_url = os.environ.get('SITE_DOMAIN')
	file_name = file.replace('.md','')
	post_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"+file)
	post = frontmatter.load(post_path)
	post_text = "New Post : " + post['title'] +"\n" + site_url + urllib.parse.quote(file_name)
	return post_text

def main():
	file = " ".join(sys.argv[1:len(sys.argv)])
	if not file:
		return
	client = OAuth()
	client.create_tweet(text = GetTweetText(file))

if __name__ == "__main__":
	main()
```
간단하게 소개하며, 파일명을 인자값으로 받아, 글의 제목과 url을 만들고 트위터에 글을 쓰는 함수를 호출한 것이다. 만들면서 신경쓴 것만 정리하고자 한다.
- `OAuth()` : 트위터 인증을 하는 함수이다.
	- 민감한 정보이기 때문에 [GitHub Secrets](https://fatihkalifa.com/twitter-github-actions#:~:text=%EC%B6%94%EA%B0%80%20%EC%B0%B8%EA%B3%A0%20%EC%82%AC%ED%95%AD-,GitHub%20%EB%B9%84%EB%B0%80,-%EA%B8%B0%EB%8A%A5%EC%9D%84%20%EC%82%AC%EC%9A%A9%20%ED%95%98%EC%97%AC) 기능을 사용하여, 환경변수로 값을 얻게 한다.
- `GetTweetText(file)` : 트위터에 내용을 만들어주는 함수이다.
	- `urllib.parse.quote(file_name)` : 파일명이 한글인 경우가 있기 때문에 url 인코딩을 해준다.
- `file = " ".join(sys.argv[1:len(sys.argv)])` : 파일명을 인자값으로 받는다. 파일명이 띄어쓰기가 있기 때문에 인자값이 배열로 들어온다. 배열로 들어간 인자값을 하나의 문자열로 만들기 위한 코드이다.
- `client.create_tweet(text = GetTweetText(file))` : 트위터에 글을 쓰는 기능을 한다.

## 트위터 쓰기 코드 실행하기
최신 커밋 중 새로 추가한 마크다운 문서의 파일명을 인자값을 가진 트위터를 작성하는 코드를 실행시켜야 한다. `xargs`를 사용하여 파일명을 인자값으로 넘겨서 사용할 수 있다.
``` shell
$ git diff --name-status HEAD~1 | grep ".md$" | grep "^A" | cut -c 3- | xargs -L 1 python3 AutoTweet.py
```
- `xargs -L 1` : 여러줄을 값을 각각 넘겨준다.

### Github Actions로 실행하기
``` yml
name: Tweet
on:
  push:
    branches:
      - main
jobs:
  tweet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0
      - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        working-directory: .automatically
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - run: git config --global core.quotepath false
      - name: Share status
        working-directory: .automatically
        env:
          TWITTER_ACCESS_TOKEN_KEY: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
          TWITTER_BEARER_TOKEN_KEY: ${{ secrets.TWITTER_BEARER_TOKEN_KEY }}
          SITE_DOMAIN: ${{ secrets.SITE_DOMAIN }}
        run: git diff --name-status HEAD~1 | grep ".md$" | grep "^A" | cut -c 3- | xargs -L 1 python3 AutoTweet.py
```
- `- name: Set up Python 3.8` : 파이썬을 설정한다.
- `- name: Install dependencies` : 필요한 라이브러리를 설치한다.
- `- run: git config --global core.quotepath false` : 파일명인 경우 한글이 깨지기 때문에 해당 커맨드를 실행하면 한글이 깨지지 않는다.
- `- name: Share status` : [GitHub Secrets](https://fatihkalifa.com/twitter-github-actions#:~:text=%EC%B6%94%EA%B0%80%20%EC%B0%B8%EA%B3%A0%20%EC%82%AC%ED%95%AD-,GitHub%20%EB%B9%84%EB%B0%80,-%EA%B8%B0%EB%8A%A5%EC%9D%84%20%EC%82%AC%EC%9A%A9%20%ED%95%98%EC%97%AC) 을 사용하여 키를 등록하고 환경변수로 지정한 다음 `AutoTweet.py` 을 실행한다.

이와 같이 하면 새로운 글을 커밋하면 자동으로 트위터를 작성하게 된다.
## 테스트 결과
테스트 결과는 [[트윗 테스트]]에서 확인할 수 있다.

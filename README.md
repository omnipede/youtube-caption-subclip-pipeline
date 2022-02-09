# youtube-caption-subclip-pipeline

유튜브에서 동영상을 다운로드 받고, 자막 (caption) 을 line by line 으로 분리한 뒤, 자막 단위로 동영상을 분리 (subclip) 하여 저장하는 데이터 파이프라인 스크립트.

## Requirements
* ```python``` >= 3.9.0
* ```ffmpeg```

## 설치 방법

* 기본 설치 방법

```
$ pip install git+https://github.com/omnipede/youtube-caption-subclip-pipeline.git
```

* 또는, 직접 repository 를 다운로드 받아 사용해보는 경우 repository 디렉토리 내부에서 다음 커맨드 실행
```
$ pip install -r requirements.txt
```

## 사용 방법

### Arguments
| Argument | Description |
| --- | --- |
| -i (--input) | 처리할 Youtube URL 리스트가 저장된 input file path |
| -o (--output) | Caption 과 subclip 을 저장할 output directory path (Optional) |

### Input file 형식
[example.txt](./example.txt) 처럼 다운로드 받을 유튜브 URL 리스트를 넣으면 된다. 
***단, 영상에 영어 자막이 존재해야 한다.***

### 기본 사용법
```
$ python -m ycsp -i ./example.txt
```

실행 위치의 ```resources``` 디렉토리에 실행 결과가 저장된다. 실행 결과 관련 내용은 [실행 결과](#실행-결과) 항목 참조


### 출력 디렉토리 지정

자막과 subclip 을 저장할 위치를 따로 지정할 수 있다.

```
$ python -m ycsp -i ./example.txt -o /PATH/TO/YOUR/DIR
```

### Help

```
$ python -m ycsp --help
```

## 실행 결과

<img width="757" alt="스크린샷 2022-02-09 오후 2 37 13" src="https://user-images.githubusercontent.com/41066039/153128536-b3d95108-c116-47ae-87ed-6291ebfefdce.png">

스크립트를 실행시키면 지정된 위치에 위와 같이 youtube 동영상 제목으로 디렉토리가 생기고, 각 디렉토리 별로 ```clips``` 디렉토리와 원본 영상이 저장된다.
```clips``` 디렉토리 내부는 다음과 같이 자막 텍스트 파일과 자막 구간에 해당하는 subclip 파일이 존재한다.

<img width="752" alt="스크린샷 2022-02-09 오후 2 40 09" src="https://user-images.githubusercontent.com/41066039/153128856-edaedcdb-ff14-4c7d-92a0-855709097e96.png">

각 subclip 파일명은 (youtube 제목)-(시작지점ms)-(구간길이ms) 로 이루어져있다.

## 주의 사항

유튜브 다운로드 시 [pytube](https://github.com/pytube/pytube) 라이브러리를 사용하고 있는데,  
유튜브 다운로드 정책에 따라 라이브러리가 작동 하지 않는 경우가 종종 발생한다. 이 경우 라이브러리 github repo 에서 이슈를 확인해보고 이슈를 fix 한 브랜치를 사용하는 것으로 해결한다.

## TODO

* Rename module

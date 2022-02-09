from setuptools import setup

setup(
    name="ycsp",
    version="0.1.0",
    description="Youtube 에서 동영상을 받아 자막 (caption) 을 추출하고 자막에 맞는 subclip 단위로 동영상을 나누는 데이터 파이프라인",
    url="https://github.com/omnipede/youtube-caption-subclip-pipeline",
    author="omnipede",
    author_email="omnipede@naver.com",
    packages=['ycsp'],
    zip_safe=False,
    install_requires=[
        'certifi==2021.10.8',
        'charset-normalizer==2.0.11',
        'decorator==4.4.2',
        'idna==3.3',
        'imageio==2.14.1',
        'imageio-ffmpeg==0.4.5',
        'moviepy==1.0.3',
        'numpy==1.22.2',
        'Pillow==9.0.1',
        'proglog==0.1.9',
        'python-dateutil==2.8.2',
        'pytube @ git+https://github.com/DEADF00D/pytube.git@1ef970763363ff96ad344b1d69237f7e4d331da5',
        'requests==2.27.1',
        'six==1.16.0',
        'tqdm==4.62.3',
        'typing_extensions==4.0.1',
        'urllib3==1.26.8'
    ]
)
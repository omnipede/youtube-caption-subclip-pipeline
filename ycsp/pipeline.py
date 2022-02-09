import os
import argparse
import re
import xml.etree.ElementTree as elemTree
from moviepy.config import get_setting
from moviepy.tools import subprocess_call

from pytube import YouTube
from os import path

from ycsp.log import logger


def execute() -> None:
    """
    Python youtube library 를 이용해서 동영상을 자막 단위로 나눔.
    """

    # Parse arguments
    input_file_path, output_dir_path = __parse_args()

    # 파일을 읽어서 다운로드할 url 을 불러온다
    urls = __read_youtube_url_from_input_file(input_file_path)
    logger.info(f'# of target youtube urls: {len(urls)}')

    # Download files
    for url in urls:
        __download_and_split_into_clips(url, output_dir_path)


def __parse_args() -> tuple[str, str]:
    """
    모듈 argument 를 파싱하는 메소드
    -i, --input --> Youtube URL 리스트가 저장된 파일의 위치
    -o, --output --> caption, subclip 으로 나눈 결과를 저장할 위치
    :return: (input_file_path, output_file_path)
    """

    # Default output directory
    resources_dir = path.join('./', 'resources')

    parser = argparse.ArgumentParser(description="Youtube captions & subclips pipeline script.")
    parser.add_argument("-i", "--input", help="처리할 Youtube URL 리스트가 저장된 input file path", required=True)
    parser.add_argument("-o", "--output", help="Caption 과 subclip 을 저장할 output directory path (Optional)", default=resources_dir)

    args = parser.parse_args()

    return args.input, args.output


def __read_youtube_url_from_input_file(input_file_path: str) -> list[str]:
    """
    특정 위치에 존재하는 입력 파일을 읽고 youtube url 리스트를 반환하는 메소드
    :param input_file_path 입력 파일 경로
    :return Youtube URL list
    """

    if not path.exists(input_file_path):
        raise FileNotFoundError(f"File not exists: {input_file_path}")

    if not path.isfile(input_file_path):
        raise FileNotFoundError(f"File {input_file_path} is not file.")

    with open(input_file_path, 'r') as f:
        return f.readlines()


def __download_and_split_into_clips(url: str, resources_dir: str) -> None:
    """
    Youtube url 로 음원을 받고 클립으로 나누는 메소드
    :param url: Youtube URL
    :param resources_dir: 클립을 저장할 경로
    """

    logger.info(f"Processing {url}")

    # 리소스 저장 위치 확인
    if not path.exists(resources_dir):
        logger.info(f"Creating resource dir: {resources_dir}")
        os.mkdir(resources_dir)

    # 저장 위치가 디렉토리가 아닌 경우
    if not path.isdir(resources_dir):
        raise NotADirectoryError(f"{resources_dir} is not directory")

    # Download youtube file
    yt = YouTube(url)
    tube_title = yt.title.replace(' ', '')
    logger.info(f"Target tube title: {tube_title}")

    original_file_name = tube_title + ".mp4"

    # ./resources/{music_title}/{mp4_file_name} 에 원본 음원을 저장한다.
    original_file_dir = path.join(resources_dir, tube_title)
    original_file_loc = yt.streams \
        .first() \
        .download(original_file_dir, original_file_name)

    logger.info(f"Target file is downloaded: {original_file_loc}")

    # ./resources/{music_title}/clips/ 디렉토리에 샘플을 저장한다.
    clips_dir = path.join(resources_dir, tube_title, 'clips')
    if not path.exists(clips_dir):
        logger.info(f"Creating clip dir: {clips_dir}")
        os.mkdir(clips_dir)

    # Get EN captions
    captions = yt.captions.get("en", None)
    if captions is None:
        raise KeyError(f"Caption does not exists on {url}")

    # Parse XML string into tree
    tree = elemTree.fromstring(captions.xml_captions)

    for p in tree.findall("./body/p"):
        start_at_str = p.attrib['t']
        duration_str = p.attrib['d']

        start_at = float(start_at_str) / 1000.0
        duration = float(duration_str) / 1000.0

        # Get end time
        end_at = start_at + duration

        # Get text of caption
        caption = p.text

        # Caption 이 없으면 pass 처리
        if caption is None:
            continue

        # Caption 전처리
        caption = re.sub('[^A-Za-z0-9가-힣 ]', '', caption)

        # Split audio file into clip
        clip_name = f'{tube_title}-{start_at_str}-{duration_str}'
        clip_mp4_path = path.join(clips_dir, clip_name + ".mp4")
        clip_caption_path = path.join(clips_dir, clip_name + ".txt")

        logger.info(f"Creating {clip_mp4_path}")
        __ffmpeg_extract_subclip(original_file_loc, start_at, end_at, clip_mp4_path)

        with open(clip_caption_path, 'w') as f:
            f.write(caption)


def __ffmpeg_extract_subclip(filename, t1, t2, targetname=None):
    """
    Makes a new video file playing video file ``filename`` between
        the times ``t1`` and ``t2``.
    """
    name, ext = os.path.splitext(filename)
    if not targetname:
        T1, T2 = [int(1000 * t) for t in [t1, t2]]
        targetname = "%sSUB%d_%d.%s" % (name, T1, T2, ext)

    cmd = [get_setting("FFMPEG_BINARY"), "-y",
           "-ss", "%0.2f" % t1,
           "-i", filename,
           "-t", "%0.2f" % (t2 - t1),
           "-map", "0", "-vcodec", "copy", "-acodec", "copy", targetname]

    subprocess_call(cmd, logger=None)

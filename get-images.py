from pathlib import Path
import fiftyone as fo
import fiftyone.brain as fob
from fiftyone import ViewField as F
from pytube import YouTube
from pytube.innertube import _default_clients
import shutil
import urllib3

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

OUTPUT_PATH = "downloaded/"
LIMIT = 12
FPS = 1


def main(url: str):
    download_video(url)

    dataset = fo.Dataset.from_videos_dir(OUTPUT_PATH)

    # take FPS frames/sec
    frame_view = dataset.to_frames(sample_frames=True, fps=FPS)

    results = fob.compute_similarity(frame_view, brain_key="frame_sim")

    # Find maximally unique frames
    results.find_unique(LIMIT)
    unique_view = frame_view.select(results.unique_ids)

    # Copy unique frames to another folder
    result_path = OUTPUT_PATH + "result/"
    ensure_dir(result_path)
    for sample in unique_view:
        shutil.copy(sample.filepath, result_path)

    # visualization
    session = fo.launch_app(unique_view)  # type: ignore
    session.wait()


def download_video(url: str):
    shutil.rmtree(OUTPUT_PATH, ignore_errors=True)

    is_youtube = "youtube.com" in url or "youtu.be" in url
    if is_youtube:
        download_youtube_video(url)
    else:
        download_url_video(url)


def download_url_video(url: str):
    try:
        path = OUTPUT_PATH + "video.mp4"
        ensure_dir(OUTPUT_PATH)

        http = urllib3.PoolManager()
        r = http.request("GET", url, preload_content=False)
        chunk_size = 1024 * 1024
        with open(path, "wb+") as out:
            while True:
                data = r.read(chunk_size)
                if not data:
                    break
                out.write(data)

        r.release_conn()
    except Exception as e:
        print("Error downloading video")
        raise e


def download_youtube_video(url: str):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_video=True).get_by_resolution("720p")

        if stream is None:
            stream = yt.streams.get_highest_resolution()

        if stream is None:
            raise ValueError("No stream found")

        stream.download(output_path=OUTPUT_PATH)
    except Exception as e:
        print("Error downloading video")
        raise e


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # url = "https://www.youtube.com/shorts/zsafugt9BeQ"  # few unique frames
    # url = "https://www.youtube.com/shorts/ZbFJ6z4LZJc" # similar frames
    # url = "https://www.youtube.com/shorts/YHXtu7WSc08"
    # url = "https://www.youtube.com/watch?v=22tVWwmTie8"  # houdini
    # url = "https://www.youtube.com/shorts/vuWE3ArKHUg"  # 10 dresses
    url = "https://wishlinkcdn.azureedge.net/creator-media-videos/media_0_zuola_p465472_5c5c8776-5744-495a-976c-0fcca278115f.mp4"  # cdn

    main(url)

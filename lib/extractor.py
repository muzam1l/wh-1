from pathlib import Path
import fiftyone as fo
import fiftyone.brain as fob
from fiftyone.brain.similarity import DuplicatesMixin
from pytube import YouTube
from pytube.innertube import _default_clients
import shutil
import urllib3

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

LIMIT = 12
FPS = 1


def extract_images(url: str, output_path: str, visualize=False):
    download_video(url, output_path)

    dataset = fo.Dataset.from_videos_dir(output_path)

    # take FPS frames/sec
    frame_view = dataset.to_frames(sample_frames=True, fps=FPS)

    results: DuplicatesMixin = fob.compute_similarity(frame_view, brain_key="frame_sim")

    # Find maximally unique frames
    results.find_unique(LIMIT)
    unique_view = frame_view.select(results.unique_ids)

    # Copy unique frames to another folder
    result_path = Path(output_path, "result")
    ensure_dir(result_path)
    for sample in unique_view:
        shutil.copy(sample.filepath, result_path)

    print("Done! results saved at", result_path.absolute())
    # visualization
    if visualize:
        session = fo.launch_app(unique_view)  # type: ignore
        session.wait()


def download_video(url: str, output_path: str):
    shutil.rmtree(output_path, ignore_errors=True)

    is_youtube = "youtube.com" in url or "youtu.be" in url
    if is_youtube:
        download_youtube_video(url, output_path)
    else:
        download_url_video(url, output_path)


def download_url_video(url: str, output_path: str):
    try:
        ensure_dir(Path(output_path))
        path = Path(output_path, "video.mp4")

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


def download_youtube_video(url: str, output_path: str):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_video=True).get_by_resolution("720p")

        if stream is None:
            stream = yt.streams.get_highest_resolution()

        if stream is None:
            raise ValueError("No stream found")

        stream.download(output_path=output_path)
    except Exception as e:
        print("Error downloading video")
        raise e


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # url = "https://www.youtube.com/shorts/zsafugt9BeQ"  # few unique frames
    # url = "https://www.youtube.com/shorts/ZbFJ6z4LZJc" # similar frames
    # url = "https://www.youtube.com/shorts/YHXtu7WSc08"
    # url = "https://www.youtube.com/watch?v=22tVWwmTie8"  # houdini
    # url = "https://www.youtube.com/shorts/vuWE3ArKHUg"  # 10 dresses
    url = "https://wishlinkcdn.azureedge.net/creator-media-videos/media_0_zuola_p465472_5c5c8776-5744-495a-976c-0fcca278115f.mp4"  # cdn

    extract_images(url, output_path="downloaded/", visualize=True)

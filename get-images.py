import fiftyone as fo
import fiftyone.brain as fob
from fiftyone import ViewField as F
from pytube import YouTube
from pytube.innertube import _default_clients
import shutil

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

OUTPUT_PATH = "downloaded/"
LIMIT = 12
FPS = 1


def main():
    download_video()

    dataset = fo.Dataset.from_videos_dir(OUTPUT_PATH)

    # take 1 frame/sec
    frame_view = dataset.to_frames(sample_frames=True, fps=FPS)

    results = fob.compute_similarity(frame_view, brain_key="frame_sim")

    # Find maximally unique frames
    results.find_unique(LIMIT)
    unique_view = frame_view.select(results.unique_ids)

    # visualization
    session = fo.launch_app(unique_view)  # type: ignore
    session.wait()


def download_video():
    try:

        # url = "https://www.youtube.com/shorts/zsafugt9BeQ"  # few unique frames
        # url = "https://www.youtube.com/shorts/ZbFJ6z4LZJc" # similar frames
        url = "https://www.youtube.com/shorts/vuWE3ArKHUg"  # 10 dresses
        # url = "https://www.youtube.com/shorts/YHXtu7WSc08"
        # url = "https://www.youtube.com/watch?v=22tVWwmTie8"  # houdini
        yt = YouTube(url)
        stream = yt.streams.filter(only_video=True).get_by_resolution("720p")

        if stream is None:
            stream = yt.streams.get_highest_resolution()

        if stream is None:
            raise ValueError("No stream found")

        shutil.rmtree(OUTPUT_PATH, ignore_errors=True)
        stream.download(output_path=OUTPUT_PATH)
    except Exception as e:
        print("Error downloading video")
        raise e


if __name__ == "__main__":
    main()

import yt_dlp
import instaloader
import os
import re
from typing import Tuple, Optional
import cv2
from pathlib import Path


class VideoDownloader:
    def __init__(self, download_path: str = "data/videos", images_path: str = "data/images"):
        self.download_path = Path(download_path)
        self.images_path = Path(images_path)
        self.download_path.mkdir(parents=True, exist_ok=True)
        self.images_path.mkdir(parents=True, exist_ok=True)

    def detect_platform(self, url: str) -> str:
        """Detect the platform from URL"""
        if "instagram.com" in url or "instagr.am" in url:
            return "instagram"
        elif "tiktok.com" in url:
            return "tiktok"
        else:
            raise ValueError("Unsupported platform. Only Instagram and TikTok are supported.")

    def download_video(self, url: str) -> Tuple[str, str, Optional[str]]:
        """
        Download video from TikTok or Instagram
        Returns: (platform, video_path, thumbnail_path)
        """
        platform = self.detect_platform(url)

        if platform == "tiktok":
            return self._download_tiktok(url)
        elif platform == "instagram":
            return self._download_instagram(url)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

    def _download_tiktok(self, url: str) -> Tuple[str, str, Optional[str]]:
        """Download TikTok video using yt-dlp"""
        ydl_opts = {
            'format': 'best',
            'outtmpl': str(self.download_path / '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_id = info['id']
                ext = info['ext']
                video_path = self.download_path / f"{video_id}.{ext}"

                # Extract thumbnail
                thumbnail_path = self._extract_thumbnail(str(video_path), video_id)

                return "tiktok", str(video_path), thumbnail_path
        except Exception as e:
            raise Exception(f"Failed to download TikTok video: {str(e)}")

    def _download_instagram(self, url: str) -> Tuple[str, str, Optional[str]]:
        """Download Instagram video using instaloader"""
        try:
            L = instaloader.Instaloader(
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                compress_json=False,
                dirname_pattern=str(self.download_path)
            )

            # Extract shortcode from URL
            shortcode = self._extract_instagram_shortcode(url)
            if not shortcode:
                raise ValueError("Could not extract Instagram shortcode from URL")

            # Download post
            post = instaloader.Post.from_shortcode(L.context, shortcode)

            # Download the video
            L.download_post(post, target=str(self.download_path))

            # Find the downloaded video file
            video_files = list(self.download_path.glob(f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC*.mp4"))

            if video_files:
                video_path = str(video_files[0])
                # Extract thumbnail
                thumbnail_path = self._extract_thumbnail(video_path, shortcode)
                return "instagram", video_path, thumbnail_path
            else:
                raise Exception("Video file not found after download")

        except Exception as e:
            raise Exception(f"Failed to download Instagram video: {str(e)}")

    def _extract_instagram_shortcode(self, url: str) -> Optional[str]:
        """Extract shortcode from Instagram URL"""
        patterns = [
            r'instagram\.com/p/([^/?#&]+)',
            r'instagram\.com/reel/([^/?#&]+)',
            r'instagram\.com/tv/([^/?#&]+)',
            r'instagr\.am/p/([^/?#&]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def _extract_thumbnail(self, video_path: str, video_id: str) -> Optional[str]:
        """Extract thumbnail from video"""
        try:
            vidcap = cv2.VideoCapture(video_path)
            success, image = vidcap.read()

            if success:
                thumbnail_path = self.images_path / f"{video_id}_thumb.jpg"
                cv2.imwrite(str(thumbnail_path), image)
                vidcap.release()
                return str(thumbnail_path)

            vidcap.release()
            return None
        except Exception as e:
            print(f"Failed to extract thumbnail: {str(e)}")
            return None

    def extract_video_frames(self, video_path: str, num_frames: int = 10) -> list:
        """Extract multiple frames from video for analysis"""
        frames = []
        try:
            vidcap = cv2.VideoCapture(video_path)
            total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

            if total_frames == 0:
                return frames

            # Calculate frame indices to extract
            frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]

            for idx in frame_indices:
                vidcap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                success, image = vidcap.read()
                if success:
                    frames.append(image)

            vidcap.release()
        except Exception as e:
            print(f"Failed to extract frames: {str(e)}")

        return frames

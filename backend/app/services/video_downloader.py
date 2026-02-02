import yt_dlp
import instaloader
import os
import re
from typing import Tuple, Optional
import cv2
from pathlib import Path


class VideoDownloader:
    def __init__(self, download_path: str = None, images_path: str = None):
        base_dir = Path(__file__).resolve().parents[2]
        self.data_dir = base_dir / "data"
        self.download_path = Path(download_path) if download_path else self.data_dir / "videos"
        self.images_path = Path(images_path) if images_path else self.data_dir / "images"
        self.download_path.mkdir(parents=True, exist_ok=True)
        self.images_path.mkdir(parents=True, exist_ok=True)

    def _to_public_path(self, file_path: Optional[Path]) -> Optional[str]:
        """
        Convert file path to web-safe public path with forward slashes.
        Always returns relative paths like: images/filename.jpg, videos/filename.mp4
        """
        if not file_path:
            return None

        try:
            # Resolve the path and make it relative to data_dir
            resolved_path = file_path.resolve()
            relative = resolved_path.relative_to(self.data_dir.resolve())

            # Convert to forward-slash format (web-safe)
            if relative.parts and relative.parts[0] in {"images", "videos", "exports"}:
                # Use forward slashes for web URLs
                return f"{relative.parts[0]}/" + "/".join(relative.parts[1:])

            # If path structure doesn't match, try to extract the relevant part
            # This handles edge cases where the path might be in a subdirectory
            path_str = str(relative).replace("\\", "/")
            return path_str

        except Exception as e:
            # If we can't make it relative, try to extract just the filename
            # and prepend the appropriate directory
            print(f"Warning: Could not make path relative: {e}")

            # Try to determine if it's an image, video, or export based on parent directory
            path_parts = str(file_path).replace("\\", "/").split("/")

            if "images" in path_parts:
                idx = path_parts.index("images")
                return "images/" + "/".join(path_parts[idx + 1:])
            elif "videos" in path_parts:
                idx = path_parts.index("videos")
                return "videos/" + "/".join(path_parts[idx + 1:])
            elif "exports" in path_parts:
                idx = path_parts.index("exports")
                return "exports/" + "/".join(path_parts[idx + 1:])

            # Last resort: return just the filename with assumed directory
            return f"images/{file_path.name}" if file_path.suffix in ['.jpg', '.png', '.jpeg'] else str(file_path)

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

                # thumbnail_path is already a Path object
                thumbnail_public = self._to_public_path(thumbnail_path) if thumbnail_path else None
                return "tiktok", self._to_public_path(video_path), thumbnail_public
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
                video_path = video_files[0]
                # Extract thumbnail
                thumbnail_path = self._extract_thumbnail(str(video_path), shortcode)
                # thumbnail_path is already a Path object
                thumbnail_public = self._to_public_path(thumbnail_path) if thumbnail_path else None
                return "instagram", self._to_public_path(video_path), thumbnail_public
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

    def _extract_thumbnail(self, video_path: str, video_id: str) -> Optional[Path]:
        """
        Extract thumbnail from video and return Path object.
        Returns Path object to be processed by _to_public_path()
        """
        try:
            vidcap = cv2.VideoCapture(video_path)
            success, image = vidcap.read()

            if success:
                thumbnail_path = self.images_path / f"{video_id}_thumb.jpg"
                cv2.imwrite(str(thumbnail_path), image)
                vidcap.release()
                # Return Path object instead of string for consistent processing
                return thumbnail_path

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

    def cleanup_video(self, video_path: str) -> bool:
        """
        Delete video file after processing to save storage.
        Keeps only the thumbnail.
        Returns True if successful, False otherwise.
        """
        try:
            if not video_path:
                return True

            # Convert to absolute path if needed
            if not os.path.isabs(video_path):
                # Handle relative paths like "videos/filename.mp4"
                if video_path.startswith("videos/"):
                    video_path = self.download_path / video_path.replace("videos/", "")
                else:
                    video_path = Path(video_path)
            else:
                video_path = Path(video_path)

            # Check if file exists and delete it
            if video_path.exists() and video_path.is_file():
                video_path.unlink()
                print(f"Deleted video file: {video_path}")
                return True
            else:
                print(f"Video file not found: {video_path}")
                return False

        except Exception as e:
            print(f"Failed to cleanup video {video_path}: {str(e)}")
            return False

    def cleanup_recipe_files(self, video_path: Optional[str], thumbnail_path: Optional[str]) -> dict:
        """
        Cleanup both video and thumbnail files (used when deleting a recipe).
        Returns dict with cleanup status.
        """
        result = {
            "video_deleted": False,
            "thumbnail_deleted": False
        }

        # Delete video
        if video_path:
            result["video_deleted"] = self.cleanup_video(video_path)

        # Delete thumbnail
        if thumbnail_path:
            try:
                thumb_path = thumbnail_path
                if not os.path.isabs(thumb_path):
                    if thumb_path.startswith("images/"):
                        thumb_path = self.images_path / thumb_path.replace("images/", "")
                    else:
                        thumb_path = Path(thumb_path)
                else:
                    thumb_path = Path(thumb_path)

                if thumb_path.exists() and thumb_path.is_file():
                    thumb_path.unlink()
                    print(f"Deleted thumbnail file: {thumb_path}")
                    result["thumbnail_deleted"] = True

            except Exception as e:
                print(f"Failed to cleanup thumbnail {thumbnail_path}: {str(e)}")

        return result

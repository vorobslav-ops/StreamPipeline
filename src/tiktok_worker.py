from tiktok_uploader.upload import TikTokUploader

def upload_to_tiktok(video_path, description):
    try:
        uploader = TikTokUploader(cookies='../config/cookies.txt')
        failed = uploader.upload_videos(
            videos=[{'video': video_path, 'description': description}]
        )
        if not failed:
            print("[SUCCESS] Pushed to TikTok")
        else:
            print("[-] TikTok upload failed.")
    except Exception as e:
        print(f"[-] TikTok automation error: {e}")

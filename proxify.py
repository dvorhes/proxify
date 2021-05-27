import shutil, sys, subprocess
from pathlib import Path

MEDIA = sys.argv[1]
DELETE_PROXIES = sys.argv[2]

if DELETE_PROXIES == "True":
    DELETE_PROXIES = True
elif DELETE_PROXIES == "False":
    DELETE_PROXIES = False
else:
    raise Exception('Error. Check spelling.')


# Makes proxies of all footage in Footage folder.
def proxify(media_path, output_resolution=(1280,720), pro_res_preset=0, delete_proxies=False):
    
    file_types = ['.mp4', '.mov', '.mts']
    proxy_folder_naming_convention = "Proxies"
    footage_folder_naming_convention = "Footage"

    media_path = Path(media_path)
    if media_path.is_dir():
        folders = [i for i in media_path.rglob("*") if i.is_dir()]
    elif media_path.is_file():
        video_file = media_path
        proxy_folder = Path(video_file.parent)
        proxy_folder.mkdir(exist_ok=True)
        proxy_video_file = Path(proxy_folder, video_file.name)
        output_path = Path(proxy_folder, f"{video_file.stem}_proxy.mov")

        cmd = ["ffmpeg",  "-y", 
               "-i", f"{video_file}", 
               "-vf", "scale=1280:720", 
               "-c:v", "prores_ks", "-profile:v", f"{0}", 
               "-c:a", "copy", f"{output_path}"]

        subprocess.call(cmd)
        return "Done!"

    if delete_proxies:
        proxy_folders = [i for i in folders if i.name == proxy_folder_naming_convention]
        for proxy_folder in proxy_folders:
            print(f"deleting proxy folder: {proxy_folder}")
            shutil.rmtree(proxy_folder)
    else: 
        footage = [i for i in media_path.rglob("*") if i.suffix.lower() in file_types]
        footage.sort()

        for video_file in footage:
            proxy_folder = Path(video_file.parent, proxy_folder_naming_convention)
            proxy_folder.mkdir(exist_ok=True)
            proxy_video_file = Path(proxy_folder, video_file.name)
            output_path = Path(proxy_folder, f"{video_file.stem}.mov")

            cmd = ["ffmpeg",  "-y", 
                   "-i", f"{video_file}", 
                   "-vf", "scale=1280:720", 
                   "-c:v", "prores_ks", "-profile:v", f"{0}", 
                   "-c:a", "copy", f"{output_path}"]

            subprocess.call(cmd)

proxify(MEDIA, delete_proxies=DELETE_PROXIES)
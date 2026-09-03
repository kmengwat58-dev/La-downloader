import os
import yt_dlp
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# ថតសម្រាប់ស្តុកវីដេអូដែលទាញយកបាន
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    error = ""
    filename = ""

    if request.method == "POST":
        video_url = request.form.get("video_url", "").strip()

        if not video_url:
            error = "សូមបញ្ចូល Link សិន!"
        else:
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    # ទាញយកឈ្មោះ File ដែលបាន Download រួច
                    downloaded_file_path = ydl.prepare_filename(info)
                    filename = os.path.basename(downloaded_file_path)
                    title = info.get("title", "វីដេអូ")

                message = f'ទាញយក "{title}" បានជោគជ័យ!'
            except Exception as e:
                error = f"មានបញ្ហា៖ {str(e)}"

    return render_template(
        "index.html", message=message, error=error, filename=filename
    )


# Route សម្រាប់ផ្ញើ File វីដេអូឱ្យ User ទាញយកទៅម៉ាស៊ីនរបស់គាត់
@app.route("/get-video/<path:filename>")
def get_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
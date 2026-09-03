from flask import Flask, render_template, request, jsonify, redirect, url_for
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# បន្ថែម GET និង POST ដើម្បីកុំឱ្យជួប error "Method Not Allowed"
@app.route('/download', methods=['GET', 'POST'])
def download():
    # ប្រសិនបើមានគេបើក link /download លើ Browser ដោយផ្ទាល់ (GET method)
    if request.method == 'GET':
        return redirect(url_for('index'))

    # សម្រាប់សំណើទាញយកវីដេអូ (POST method)
    try:
        data = request.get_json(silent=True)
        if data and 'url' in data:
            video_url = data.get('url')
        else:
            video_url = request.form.get('url')

        if not video_url:
            return jsonify({'status': 'error', 'message': 'សូមបញ្ចូល Link វីដេអូ!'}), 400

        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            title = info.get('title', 'Video HD')

            return jsonify({
                'status': 'success',
                'url': download_url,
                'title': title
            })

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'មិនអាចទាញយកបានទេ៖ {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from generate_image import generate_image_from_prompt
from generate_avatar import upload_image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

 # Make sure this is correctly imported

@app.route('/image-generator', methods=['GET', 'POST'])
def image_generator():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '').strip()

        if not prompt:
            return render_template('image_generator.html', error="Please enter a prompt.")

        # ✅ Use actual generation logic
        generated_image_url = generate_image_from_prompt(prompt)
        print(f"Generated image URL: {generated_image_url}")

        if generated_image_url:
            return render_template('generated.html', image_url=generated_image_url)
        else:
            return render_template('image_generator.html', error="Image generation failed. Please try again.")

    return render_template('image_generator.html')


@app.route('/avatar-transform', methods=['GET', 'POST'])
def avatar_transform():
    if request.method == 'POST':
        file = request.files.get('image')
        style_url = request.form.get('styleurl', '').strip()
        prompt = request.form.get('prompt', '').strip()

        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # TODO: call your avatar‑transformation logic here,
            # e.g. transform_avatar(filepath, style_url, prompt)
            # For now we mock with a sample image:
            transformed_image_url = upload_image(filepath, prompt, style_url)
            if not transformed_image_url:
                return render_template('avatar_transform.html', error="Failed to transform image.")
            return render_template('generated.html', image_url=transformed_image_url)

        return render_template('avatar_form.html', error="Please upload an image.")

    return render_template('avatar_form.html')


if __name__ == '__main__':
    app.run(debug=True)

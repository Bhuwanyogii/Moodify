import os
import warnings
warnings.filterwarnings('ignore')

import requests
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import gradio as gr
import spaces

# API KEY
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
N_SONGS = 6

MOOD_LABELS = [
    'happy', 'sad', 'angry', 'fearful', 'surprised',
    'excited', 'peaceful', 'romantic', 'nostalgic', 'dreamy',
    'hopeful', 'mysterious', 'intense', 'playful', 'awe',
    'triumphant', 'horror', 'anticipation'
]

MOOD_EMOJIS = {
    'happy': '😊', 'sad': '😢', 'angry': '😠', 'fearful': '😨',
    'surprised': '😲', 'excited': '🤩', 'peaceful': '🌿', 'romantic': '💕',
    'nostalgic': '🌅', 'dreamy': '✨', 'hopeful': '🌈', 'mysterious': '🌙',
    'intense': '🔥', 'playful': '🎈', 'awe': '🌌', 'triumphant': '🏆',
    'horror': '👻', 'anticipation': '⏳',
}

MOOD_COLORS = {
    'happy': '#f59e0b', 'sad': '#6366f1', 'angry': '#dc2626',
    'fearful': '#7c3aed', 'surprised': '#f97316', 'excited': '#ef4444',
    'peaceful': '#10b981', 'romantic': '#ec4899', 'nostalgic': '#d97706',
    'dreamy': '#a78bfa', 'hopeful': '#34d399', 'mysterious': '#8b5cf6',
    'intense': '#b91c1c', 'playful': '#06b6d4', 'awe': '#0ea5e9',
    'triumphant': '#eab308', 'horror': '#374151', 'anticipation': '#64748b',
}

MOOD_SEARCH_QUERIES = {
    'happy':        'happy feel good upbeat songs playlist',
    'sad':          'sad emotional heartbreak songs playlist',
    'angry':        'angry aggressive rock songs playlist',
    'fearful':      'dark tense suspenseful horror music',
    'surprised':    'surprising uplifting unexpected music',
    'excited':      'excited high energy party songs',
    'peaceful':     'peaceful relaxing calm ambient music',
    'romantic':     'romantic love songs playlist',
    'nostalgic':    'nostalgic 80s 90s throwback songs',
    'dreamy':       'dreamy ethereal indie songs',
    'hopeful':      'hopeful uplifting inspiring songs',
    'mysterious':   'mysterious atmospheric dark ambient music',
    'intense':      'intense dramatic powerful songs',
    'playful':      'playful fun pop songs',
    'awe':          'epic orchestral awe inspiring music',
    'triumphant':   'triumphant victory epic songs',
    'horror':       'horror dark eerie scary music',
    'anticipation': 'suspenseful tension building music',
}

MOOD_DESCRIPTIONS = {
    'happy':        'a bright cheerful happy joyful sunny photo with warm colors',
    'sad':          'a dark gloomy sad depressing lonely rainy photo',
    'angry':        'a harsh aggressive angry intense dark red photo',
    'fearful':      'a dark scary frightening tense fearful threatening photo',
    'surprised':    'a shocking dramatic surprising bright vivid photo',
    'excited':      'a vibrant exciting energetic lively colorful crowd photo',
    'peaceful':     'a soft peaceful calm quiet serene nature photo',
    'romantic':     'a warm romantic intimate soft pink candlelit photo',
    'nostalgic':    'a faded vintage nostalgic retro old warm sepia photo',
    'dreamy':       'a soft dreamy pastel blurry ethereal abstract photo',
    'hopeful':      'a bright hopeful uplifting golden dawn sunrise photo',
    'mysterious':   'a dark mysterious shadowy foggy moody night photo',
    'intense':      'an intense dramatic high contrast bold powerful photo',
    'playful':      'a colorful fun playful cheerful childlike bright photo',
    'awe':          'a breathtaking vast awe-inspiring grand epic landscape photo',
    'triumphant':   'a victorious triumphant powerful golden glowing celebratory photo',
    'horror':       'a terrifying dark eerie horror unsettling disturbing photo',
    'anticipation': 'a tense suspenseful dramatic waiting anticipation foggy photo',
}

# LOADING MODEL
clip_model     = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
clip_processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
clip_model.eval()

# FUNCTIONS
@spaces.GPU
def predict_mood(pil_image):
    img   = pil_image.convert('RGB')
    texts = [MOOD_DESCRIPTIONS[m] for m in MOOD_LABELS]
    inputs = clip_processor(text=texts, images=img, return_tensors='pt', padding=True)
    with torch.no_grad():
        probs = clip_model(**inputs).logits_per_image.softmax(dim=1)[0]
    scores = {m: round(float(probs[i]) * 100, 2) for i, m in enumerate(MOOD_LABELS)}
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return {'mood': ranked[0][0], 'top5': ranked[:5], 'scores': scores}


def get_songs(mood, n=N_SONGS, api_key=YOUTUBE_API_KEY):
    if not api_key:
        return [{'title': 'Add YOUTUBE_API_KEY in Space secrets to get real songs', 'channel': '—', 'url': 'https://www.youtube.com'}]
    params = {
        'part': 'snippet',
        'q': MOOD_SEARCH_QUERIES.get(mood, mood + ' music'),
        'type': 'video',
        'videoCategoryId': '10',
        'maxResults': n,
        'key': api_key,
    }
    try:
        resp  = requests.get('https://www.googleapis.com/youtube/v3/search', params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get('items', [])
        songs = []
        for item in items:
            vid = item.get('id', {}).get('videoId', '')
            if not vid:
                continue
            s = item.get('snippet', {})
            songs.append({
                'title':   s.get('title', 'Unknown'),
                'channel': s.get('channelTitle', 'Unknown'),
                'url':     'https://www.youtube.com/watch?v=' + vid,
            })
        return songs or [{'title': 'No results found', 'channel': '—', 'url': 'https://www.youtube.com'}]
    except Exception as e:
        print('YouTube error:', e)
        return [{'title': 'API error — check your key', 'channel': '—', 'url': 'https://www.youtube.com'}]


def run(image):
    if image is None:
        return 'No image uploaded.', {}, '<p style="color:#888;font-family:sans-serif;">Upload a photo first.</p>'
    result    = predict_mood(image)
    mood      = result['mood']
    mood_text = MOOD_EMOJIS.get(mood, '') + '  ' + mood.upper()
    top5_dict = {m: round(v / 100, 4) for m, v in result['top5']}
    songs     = get_songs(mood)
    color     = MOOD_COLORS.get(mood, '#6366f1')
    items_html = ''
    for s in songs:
        items_html += (
            f"<li style='margin-bottom:14px;'>"
            f"<a href='{s['url']}' target='_blank' style='font-weight:bold;color:#1a73e8;text-decoration:none;font-size:14px;'>{s['title']}</a>"
            f"<br><span style='color:#666;font-size:12px;'>{s['channel']}</span></li>"
        )
    songs_html = (
        f"<div style='font-family:sans-serif;padding:20px;background:#fafafa;"
        f"border-radius:12px;border-left:5px solid {color};margin-top:8px;'>"
        f"<h3 style='margin-top:0;color:{color};'>&#127925; Playlist &mdash; {mood.upper()} VIBES</h3>"
        f"<ol style='padding-left:22px;margin:0;'>{items_html}</ol></div>"
    )
    return mood_text, top5_dict, songs_html

# UI
with gr.Blocks(title='Moodify', theme=gr.themes.Soft()) as demo:
    gr.Markdown('# 🎵 Moodify\nDrop a photo, get a playlist.')
    with gr.Row():
        with gr.Column():
            img_in = gr.Image(type='pil', label='Your Photo')
            btn    = gr.Button('Analyse →', variant='primary')
        with gr.Column():
            mood_out  = gr.Textbox(label='Detected Mood', interactive=False)
            label_out = gr.Label(label='Top 5 Confidence', num_top_classes=5)
    songs_out = gr.HTML()
    btn.click(fn=run, inputs=img_in, outputs=[mood_out, label_out, songs_out])

demo.launch()

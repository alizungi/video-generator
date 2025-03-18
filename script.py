import os
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import moviepy.editor as mp

# Configuration
IMAGE_PATH = "bird.jpg"  # Input image path
OUTPUT_IMAGE = "output.jpg"  # Output processed image path
VIDEO_PATH = "output.mp4"  # Output video path
MUSIC_PATH = "go-beyond-314301.mp3"  # Background music file
TEXT = "A bird standing on the tree"  # Text to overlay on the image
CAPTION = "This is a bird Image"  # Caption for video
VOICEOVER_PATH = "voiceover.mp3"  # Path for the voiceover file

# Step 1: Load and Process Image
def process_image(image_path, text, output_path):
    img = Image.open(image_path)
    
    # Convert to grayscale (or rotate) and then ensure it's RGB
    img = img.convert("RGB")  # Convert to RGB to ensure 3 channels
    # img = img.rotate(10)  # Optional: Apply rotation
    # img = img.resize((img.width // 2, img.height // 2))  # Optional: Resize image

    # Add text overlay
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()  # Use default font (you can specify a .ttf font if needed)
    text_position = (50, 50)  # Position of the text on the image
    draw.text(text_position, text, fill="white", font=font)

    img.save(output_path)
    return output_path

# Step 2: Generate Voiceover using Google Text-to-Speech (gTTS)
def generate_voiceover(text, output_path):
    tts = gTTS(text, lang="en")
    tts.save(output_path)

# Step 3: Create Video with FFmpeg
def create_video(image_path, music_path, voiceover_path, video_path, duration=5):
    # Load Image as Video Clip
    image_clip = mp.ImageClip(image_path, duration=duration)
    
    try:
        # Load Background Music
        music = mp.AudioFileClip(music_path)
        # Manually assign duration if necessary
        music = music.subclip(0, min(duration, music.duration))  # Use the audio's actual duration
        
    except Exception as e:
        print(f"Error loading audio: {e}")
        return
    
    # Load Voiceover
    narration = mp.AudioFileClip(voiceover_path)

    # Combine Audio Tracks (Music + Narration)
    final_audio = mp.CompositeAudioClip([music, narration])

    # Create Video with Captions
    final_video = image_clip.set_audio(final_audio).set_fps(24)
    final_video = mp.CompositeVideoClip([ 
        final_video,
        mp.TextClip(CAPTION, fontsize=40, color='white')
        .set_position('bottom').set_duration(duration)
    ])

    # Write Final Video
    final_video.write_videofile(video_path, codec="libx264", audio_codec="aac")

# Main Execution
def main():
    # Process the image
    processed_image = process_image(IMAGE_PATH, TEXT, OUTPUT_IMAGE)
    
    # Generate voiceover for the caption
    generate_voiceover(CAPTION, VOICEOVER_PATH)
    
    # Create video from the processed image, background music, and voiceover
    create_video(processed_image, MUSIC_PATH, VOICEOVER_PATH, VIDEO_PATH)
    
    print("✅ Video created successfully!")

if __name__ == "__main__":
    main()

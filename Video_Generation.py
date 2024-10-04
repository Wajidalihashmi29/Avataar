import argparse
from PIL import Image, ImageEnhance, ImageFilter
import torch
from diffusers import StableDiffusionPipeline
import rembg
import io
import random
import numpy as np
import cv2
from tqdm import tqdm

def enhance_object(obj_img, background):
    brightness_factor = random.uniform(0.9, 1.1)
    contrast_factor = random.uniform(0.9, 1.1)
    
    enhancer = ImageEnhance.Brightness(obj_img)
    obj_img = enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Contrast(obj_img)
    obj_img = enhancer.enhance(contrast_factor)
    
    obj_img = obj_img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return obj_img

def add_shadow(background, obj_img, position):
    shadow = Image.new("RGBA", obj_img.size, (0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    shadow_pos = (position[0] + 5, position[1] + 5)
    background.paste(shadow, shadow_pos, shadow)
    return background

def blend_images(background, obj_img, scale_factor, position):
    obj_img_resized = obj_img.copy()
    obj_img_resized.thumbnail((int(obj_img.width * scale_factor), int(obj_img.height * scale_factor)), Image.Resampling.LANCZOS)
    
    obj_img_resized = enhance_object(obj_img_resized, background)
    
    background = add_shadow(background, obj_img_resized, position)
    
    background.paste(obj_img_resized, position, obj_img_resized)
    
    return background

def generate_frame(pipe, obj_img, text_prompt, frame_width, frame_height, zoom_factor):
    # Ensure dimensions are divisible by 8
    frame_width = (frame_width // 8) * 8
    frame_height = (frame_height // 8) * 8
    
    generated_image = pipe(text_prompt, height=frame_height, width=frame_width).images[0].convert("RGBA")
    
    scale_factor = (frame_width / 4) / obj_img.width * zoom_factor
    position = (int(frame_width * 0.7 * zoom_factor), int(frame_height * 0.6 * zoom_factor))
    
    final_image = blend_images(generated_image, obj_img, scale_factor, position)
    
    return final_image



def create_video(frames, output_path, fps=24):
    height, width = np.array(frames[0]).shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        video.write(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
    
    video.release()

def generate_video(image_path, text_prompt, output_path, num_frames=60):
    with open(image_path, "rb") as input_img:
        input_bytes = input_img.read()
        obj_img_bytes = rembg.remove(input_bytes)
        obj_img = Image.open(io.BytesIO(obj_img_bytes)).convert("RGBA")

    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    # Ensure base dimensions are divisible by 8
    base_width, base_height = 768, 512
    frames = []

    for i in tqdm(range(num_frames), desc="Generating frames"):
        zoom_factor = 1 + (i / num_frames)
        frame_width = int(base_width * zoom_factor)
        frame_height = int(base_height * zoom_factor)
        
        frame = generate_frame(pipe, obj_img, text_prompt, frame_width, frame_height, zoom_factor)
        frame = frame.resize((base_width, base_height), Image.Resampling.LANCZOS)
        frames.append(frame)

    create_video(frames, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video with a zoom-out effect, blending an object into a generated scene.")
    parser.add_argument("--image", required=True, help="Path to the object image.")
    parser.add_argument("--text-prompt", required=True, help="Text prompt for background generation.")
    parser.add_argument("--output", required=True, help="Path to save the generated video.")
    parser.add_argument("--frames", type=int, default=60, help="Number of frames to generate (default: 60)")

    args = parser.parse_args()

    generate_video(args.image, args.text_prompt, args.output, args.frames)
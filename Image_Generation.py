import argparse
from PIL import Image, ImageEnhance, ImageFilter
import torch
from diffusers import StableDiffusionPipeline
import rembg
import io
import random

def enhance_object(obj_img, background):
    # Adjust brightness and contrast to match the background
    brightness_factor = random.uniform(0.9, 1.1)
    contrast_factor = random.uniform(0.9, 1.1)
    
    enhancer = ImageEnhance.Brightness(obj_img)
    obj_img = enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Contrast(obj_img)
    obj_img = enhancer.enhance(contrast_factor)
    
    # Add a slight blur to match the background's sharpness
    obj_img = obj_img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return obj_img

def add_shadow(background, obj_img, position):
    shadow = Image.new("RGBA", obj_img.size, (0, 0, 0, 100))  # Semi-transparent shadow
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    shadow_pos = (position[0] + 5, position[1] + 5)  # Slight offset for shadow
    background.paste(shadow, shadow_pos, shadow)
    return background

def blend_images(background, obj_img):
    # Resize object to fit naturally on the counter
    scale_factor = background.width // 4  # Adjust this value as needed
    obj_img.thumbnail((scale_factor, scale_factor), Image.Resampling.LANCZOS)
    
    # Position the object on the counter
    counter_y = int(background.height * 0.6)  # Adjust this value to place on counter
    counter_x = int(background.width * 0.7)   # Adjust horizontal position
    
    # Enhance object to match background
    obj_img = enhance_object(obj_img, background)
    
    # Add shadow
    background = add_shadow(background, obj_img, (counter_x, counter_y))
    
    # Paste the object
    background.paste(obj_img, (counter_x, counter_y), obj_img)
    
    return background

def generate_image(image_path, text_prompt, output_path):
    # Load and remove background from object image
    with open(image_path, "rb") as input_img:
        input_bytes = input_img.read()
        obj_img_bytes = rembg.remove(input_bytes)
        obj_img = Image.open(io.BytesIO(obj_img_bytes)).convert("RGBA")

    # Load Stable Diffusion model
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    # Generate background image
    generated_image = pipe(text_prompt, height=512, width=768).images[0].convert("RGBA")

    # Blend the object with the background
    final_image = blend_images(generated_image, obj_img)

    # Save the final image
    final_image.save(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate image based on a text prompt and blend a cut-out object image.")
    parser.add_argument("--image", required=True, help="Path to the object image.")
    parser.add_argument("--text-prompt", required=True, help="Text prompt for background generation.")
    parser.add_argument("--output", required=True, help="Path to save the generated image.")

    args = parser.parse_args()

    generate_image(args.image, args.text_prompt, args.output)
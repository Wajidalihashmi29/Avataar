# Product Image in Text-Conditioned Scene with Video Generation

  
## Problem Statement

<p align="justify">The objective of this project is to place an object (with a white background) into a text-conditioned generated scene, such that the object looks natural and aligned with the scene. The final result should maintain a realistic coherence between the object and the background.

<p align="justify">Recent advancements in generative AI have made it possible to replace traditional photography workflows with more creative approaches using AI techniques. A practical application of this technology is generating product images that would traditionally be taken in a studio, to display on e-commerce websites. The key challenge in this task is to make the object blend naturally into the generated background, considering various factors such as the lighting, aspect ratio, and spatial positioning.</p>

### Goals:

1.<p align="justify"> **Image Generation**: Generate a background based on a text prompt and place the object image in a natural position.
2. <p align="justify">**Video Generation**: Create a short video by generating multiple consistent frames with the object placed in various positions, zooming in/out, or even moving within the scene.

## Approach

### 1. **Object Enhancement and Blending**
   - The object image is processed by enhancing its brightness, contrast, and sharpness to match the generated background.
   - The object is then resized based on the scene's dimensions and blended into the background using compositing techniques, such as adding shadows for realism.

### 2. **Scene Generation**
   - A Stable Diffusion model is used to generate the background scene based on a text prompt.
   - The scene aligns with the context of the prompt, e.g., "product in a kitchen used in meal generation," and maintains the necessary aesthetic realism.

### 3. **Zoom-Out Video Creation**
   - <p align="justify">After generating the object-blended image, a video is created by generating multiple frames. In each frame, a zoom-out effect is applied to give the illusion of the camera pulling back from the object in the scene.

### Technical Overview
- **Stable Diffusion** is utilized for generating the background image based on the text prompt.
- **Rembg** is used to remove the background from the object image, leaving only the product in the image for blending.
- **PIL** (Python Imaging Library) is used for resizing, adjusting brightness/contrast, and applying other image manipulations.
- **OpenCV** is used for generating a video by combining frames of the blended object with the generated backgrounds.

## Installation

Clone the repository and navigate into it:
```bash
git clone https://github.com/Wajidalihashmi29/Avataar_Image_Generation.git
```
### Environment Setup
Make sure you have Python 3.8 or higher installed. You can install the required dependencies using requirements.txt:
```bash
pip install -r requirements.txt
```
### Model Setup
The project uses the runwayml/stable-diffusion-v1-5 model from Hugging Face for scene generation. This will be automatically downloaded when running the script for the first time.
## Image Generation
You can generate a single image by running the following command:
```bash
python image_model.py --image ./example.jpg --text-prompt "product in a kitchen used in meal generation" --output ./generated_image.png
```
- --image: Path to the object image (should have a white background).
- --text-prompt: A description of the scene you want to generate.
- --output: Path to save the final generated image with the object blended in.
## Video Generation
To generate a video with a zoom-out effect, run the following command:
```bash
python video_model.py --image ./example.jpg --text-prompt "product in a kitchen used in meal generation" --output ./generated_video.mp4 --frames 60
```
- --frames: The number of frames to generate (default is 60).
- The video will be saved in mp4 format at 24 frames per second.
This command will generate a video that starts with a zoom-in view of the object placed in the kitchen scene and gradually zooms out, giving a dynamic effect.
## Approach to the Problem
### Step 1: Object Image Processing
  - Background Removal: The object image's background is removed using the rembg library to isolate the product.
  - <p align="justify">Brightness and Contrast Matching: The object’s brightness and contrast are adjusted based on the background scene to make the object appear naturally integrated into the environment.
  - Shadow Addition: A shadow is added under the object, based on the scene's lighting and position, making the object appear naturally grounded in the scene.
### Step 2: Background Scene Generation
  - The Stable Diffusion model is used to generate a scene based on the provided text prompt (e.g., "product in a kitchen used in meal generation").
  - This ensures that the background matches the context and product’s use case.
### Step 3: Blending the Object
  - The object is resized and placed in the scene based on the scene’s composition (e.g., placed on a countertop in a kitchen).
  - It is blended into the scene with matching lighting and perspective adjustments.
### Step 4: Video Generation (Optional)
  - The zoom-out effect is achieved by generating multiple frames with a gradually decreasing zoom factor, simulating the camera moving away from the scene.
  - The frames are compiled into a video.

## Failures and Improvements
- Object Placement: Sometimes the object is placed in an unnatural position (e.g., floating above the surface). This issue was mitigated by refining the spatial placement logic.
- <p align="justify">Lighting Mismatch: Initial trials showed a mismatch in the lighting between the object and background. To fix this, brightness and contrast adjustments were added to the object before blending.
## Future Improvements
- Better Spatial Awareness: Implementing more advanced object placement strategies by analyzing the scene for potential surfaces (e.g., tables, countertops).
- Lighting Direction: Use models to predict lighting direction in the generated background and adjust the object's lighting accordingly.
- More Complex Video Animations: Introduce camera panning and object movement within the scene to create more dynamic videos.
## Conclusion
<p align="justify">This project demonstrates how generative AI can be applied to place an object in a text-conditioned scene while maintaining realism. The extension into video generation adds dynamic effects, opening up possibilities for creative content creation, especially in e-commerce.
</p>

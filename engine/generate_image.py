import os
import torch

from diffusers import StableDiffusionPipeline


pipe = None


def load_model():
    global pipe

    if pipe is None:
        pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/sd-turbo",
            torch_dtype=torch.float16,
            safety_checker=None
        )

        pipe = pipe.to("cuda")

        print("Image model loaded on cuda using torch.float16")

    return pipe


def generate_image(
    prompt,
    output_path,
    width=1280,
    height=720
):
    pipe = load_model()

    generator = torch.Generator(
        device="cuda"
    ).manual_seed(42)

    image = pipe(
        prompt=prompt,
        width=width,
        height=height,
        num_inference_steps=2,
        guidance_scale=0.0,
        generator=generator
    ).images[0]

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    image.save(output_path)

    print(f"Image saved to {output_path}")

    return output_path









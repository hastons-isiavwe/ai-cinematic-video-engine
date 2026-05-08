# engine/generate_image.py
from diffusers import AutoPipelineForText2Image
from config.settings import FAST_MODE
import torch
import argparse
import os

pipe = None


def trim_prompt(prompt, max_words=70):
    return " ".join(prompt.split()[:max_words])


def generate_image(prompt, output_path="outputs/generated_image.png", seed=None, width=720, height=720):
    global pipe

    if pipe is None:
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sd-turbo",
            torch_dtype=torch.float32
        ).to("cuda")

    generator = None
    if seed is not None:
        generator = torch.Generator(device="cuda").manual_seed(seed)

    prompt = trim_prompt(prompt)

    steps = 2 if FAST_MODE else 4

    image = pipe(
        prompt,
        width=width,
        height=height,
        num_inference_steps=steps,
        generator=generator
    ).images[0]

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    image.save(output_path)
    print(f"Image saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--output", type=str, default="outputs/generated_image.png")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--resolution", type=str, default="720x720", help="Format WIDTHxHEIGHT, e.g., 1280x720")
    args = parser.parse_args()

    width, height = map(int, args.resolution.split("x"))
    generate_image(args.prompt, args.output, args.seed, width, height)









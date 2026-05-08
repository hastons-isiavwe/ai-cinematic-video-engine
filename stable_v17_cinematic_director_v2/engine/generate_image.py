from diffusers import AutoPipelineForText2Image
from config.settings import MODE
import torch
import argparse
import os

pipe = None


def trim_prompt(prompt, max_words=40):
    return " ".join(prompt.split()[:max_words])


def generate_image(prompt, output_path="outputs/generated_image.png", seed=None, width=720, height=720):
    global pipe

    device = "cuda" if torch.cuda.is_available() else "cpu"

    if pipe is None:
        dtype = torch.float16 if device == "cuda" else torch.float32

        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sd-turbo",
            torch_dtype=dtype,
            safety_checker=None
        ).to(device)

        if device == "cuda":
            torch.backends.cuda.matmul.allow_tf32 = True
            pipe.enable_attention_slicing()

        print(f"Image model loaded on {device} using {dtype}")

    generator = None
    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(seed)

    prompt = trim_prompt(prompt)

    if MODE == "DEV":
        steps = 1
    elif MODE == "TEST":
        steps = 2
    else:
        steps = 4

    with torch.inference_mode():
        image = pipe(
            prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=0.0,
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
    parser.add_argument("--resolution", type=str, default="720x720")
    args = parser.parse_args()

    width, height = map(int, args.resolution.split("x"))
    generate_image(args.prompt, args.output, args.seed, width, height)









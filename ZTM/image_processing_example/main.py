from pathlib import Path

from PIL import Image

path: Path = Path(__file__).resolve().parent
images_path = path / "images"
updated_images_path = path / "converted_images"


def get_output_path(
    image_path: Path, updated_image_path: Path, added_name: str, extension: str
) -> Path:
    return updated_image_path / f"{image_path.stem}_{added_name}.{extension}"


def convert_gray(image_path: Path, updated_image_path: Path) -> None:
    output_path = get_output_path(image_path, updated_image_path, "gray", "png")
    with Image.open(image_path) as img:
        converted_img = img.convert("L")
        converted_img.save(output_path)
    print(f"Saved: {output_path.name}")


def resize_image(image_path: Path, updated_image_path: Path) -> None:
    output_path = get_output_path(image_path, updated_image_path, "thumbnail", "jpg")
    with Image.open(image_path) as img:
        img.thumbnail((100, 200))  # type: ignore
        img.save(output_path)


def main() -> None:
    updated_images_path.mkdir(exist_ok=True)

    for image_path in sorted(images_path.iterdir()):
        if image_path.is_file() and image_path.suffix.lower() in (
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".webp",
        ):
            convert_gray(image_path, updated_images_path)
            resize_image(image_path, updated_images_path)


if __name__ == "__main__":
    main()

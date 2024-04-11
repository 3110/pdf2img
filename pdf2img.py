from pdf2image import convert_from_path
import os

PAGE_SEPARATOR = ","
PAGE_RANGE_SEPARATOR = "-"
IMAGE_FORMAT_PNG = "PNG"
IMAGE_FORMAT_JPG = "JPG"
IMAGE_FORMATS = [IMAGE_FORMAT_PNG, IMAGE_FORMAT_JPG]

DEFAULT_DPI = 600
DEFAULT_IMAGE_FORMAT = IMAGE_FORMAT_PNG
DEFAULT_PAGES = "1"


def parse_pages(pages_str):
    pages = set()
    for part in pages_str.split(PAGE_SEPARATOR):
        if PAGE_RANGE_SEPARATOR in part:
            start, end = map(int, part.split(PAGE_RANGE_SEPARATOR))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(pages)


def pdf_to_image(
    pdf_path,
    prefix=None,
    output_folder=None,
    pages=DEFAULT_PAGES,
    dpi=DEFAULT_DPI,
    image_format=DEFAULT_IMAGE_FORMAT,
):
    if not output_folder:
        output_folder = os.getcwd()

    os.makedirs(output_folder, exist_ok=True)

    if not prefix:
        prefix = os.path.splitext(os.path.basename(pdf_path))[0]

    pages_set = parse_pages(pages)
    max_page_num_len = len(str(max(pages_set)))

    print(f'Converting "{pdf_path}" to {image_format}...')
    for page in pages_set:
        try:
            image = convert_from_path(
                pdf_path, first_page=page, last_page=page, dpi=dpi
            )[0]
            page_str = str(page).zfill(max_page_num_len)
            filename = f"{output_folder}/{prefix}_{page_str}.{image_format.lower()}"
            print(f"  Page {page_str}: {filename}")
            image.save(filename, image_format)
        except Exception as e:
            print(f"{page}ページを変換中にエラーが発生しました: {e}")
    print("Done!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PDFを指定した画像形式に変換する")
    parser.add_argument("pdf_path", type=str, help="入力PDFファイル")
    parser.add_argument(
        "-o", "--output_folder", type=str, help="出力先フォルダ", default=None
    )
    parser.add_argument(
        "-p", "--pages", type=str, help="出力するページ番号", default=DEFAULT_PAGES
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=IMAGE_FORMATS,
        help="画像の形式（" + ",".join(IMAGE_FORMATS) + ")",
        default=DEFAULT_IMAGE_FORMAT,
    )
    parser.add_argument(
        "-d", "--dpi", type=int, help="画像の解像度", default=DEFAULT_DPI
    )
    parser.add_argument(
        "--prefix", type=str, help="出力画像ファイルの名前", default=None
    )

    args = parser.parse_args()

    pdf_to_image(
        args.pdf_path,
        args.prefix,
        args.output_folder,
        args.pages,
        args.dpi,
        args.format,
    )

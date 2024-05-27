import base64
import itertools
import requests

BASE_URL = "https://maps2.bristol.gov.uk/server1/rest/services/base/1880s_CSEpoch1_128dpi_mk3/MapServer/tile/5/"
X_START = 18297
X_END = 18304
Y_START = 14093
Y_END = 14100
SIZE = 256


def main(base_url, x_start, x_end, y_start, y_end):
    image_urls = []
    for x, y in itertools.product(range(x_start, x_end), range(y_start, y_end)):
        image_url = f"{base_url}{y}/{x}"
        image_urls.append(image_url)
    svg = generate_grid(image_urls, x_end - x_start, y_end - y_start, SIZE, SIZE)
    with open("output.svg", "w", encoding="utf8") as f:
        f.write(svg)


def fetch_image(url):
    response = requests.get(url, timeout=5)
    return base64.b64encode(response.content).decode("utf-8")


def generate_svg(image_url, width, height):
    encoded_image = fetch_image(image_url)
    svg = f"""
    <svg width="{width}" height="{height}">
      <image href="data:image/jpg;base64,{encoded_image}" x="0" y="0" width="{width}" height="{height}" />
    </svg>\
    """
    return svg


def generate_grid(image_urls, grid_width, grid_height, cell_width, cell_height):
    svgs = []
    for i, url in enumerate(image_urls):
        x = (i % grid_width) * cell_width
        y = (i // grid_width) * cell_height
        svg = generate_svg(url, cell_width, cell_height)
        svgs.append(f'<g transform="translate({x}, {y})">{svg}</g>')
    return (
        f'<svg width="{grid_width * cell_width}" height="{grid_height * cell_height}">'
        + "".join(svgs)
        + "</svg>"
    )


if __name__ == "__main__":
    main(BASE_URL, X_START, X_END, Y_START, Y_END)

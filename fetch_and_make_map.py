import base64
import itertools
import requests

BASE_URL = "https://maps2.bristol.gov.uk/server1/rest/services/base/1880s_CSEpoch1_128dpi_mk3/MapServer/tile/5/"
X_START = 18297
X_END = 18299  # 18304
Y_START = 14093
Y_END = 14095  # 14100
SIZE = 256


def main(base_url, x_start, x_end, y_start, y_end):
    image_urls = make_urls(base_url, x_start, x_end, y_start, y_end)
    svg = make_grid(image_urls, x_end - x_start, y_end - y_start, SIZE, SIZE)
    with open("output.svg", "w", encoding="utf8") as f:
        f.write(svg)


def make_urls(base_url, x_start, x_end, y_start, y_end):
    image_urls = []
    for x, y in itertools.product(range(x_start, x_end), range(y_start, y_end)):
        image_url = f"{base_url}{y}/{x}"
        image_urls.append(image_url)
    return image_urls


def make_grid(image_urls, grid_width, grid_height, cell_width, cell_height):
    image_components = []
    for i, url in enumerate(image_urls):
        x = (i % grid_width) * cell_width
        y = (i // grid_width) * cell_height
        encoded_image = fetch_image(url)
        svg = make_image_component(encoded_image, x, y, cell_width, cell_height)
        image_components.append(f'<g transform="translate({x}, {y})">{svg}</g>')
    width = grid_width * cell_width
    height = grid_height * cell_height
    return (
        f'<svg width="{width}"\n height="{height}"\n'
        + f'viewBox="0 0 {width} {height}"\n'
        + 'version="1.1" id="bristol-map"\n'
        + 'xml:space="preserve"\n'
        + 'xmlns:xlink="http://www.w3.org/1999/xlink"\n'
        + 'xmlns="http://www.w3.org/2000/svg"\n'
        + 'xmlns:svg="http://www.w3.org/2000/svg"\n>\n'
        + '<g id="layer1">\n'
        + "".join(image_components)
        + "\n</g>\n</svg>"
    )


def fetch_image(url):
    response = requests.get(url, timeout=5)
    with open("output.jpg", "wb") as f:
        f.write(response.content)
    return base64.b64encode(response.content).decode("utf-8")


def make_image_component(encoded_image, x, y, width, height):
    return f"""
      <image\n\twidth="{width}"\n\theight="{height}"\n\txlink:href="data:image/jpeg;base64,{encoded_image}"\n\tx="{x}"\n\ty="{y}"\n/>
    """


if __name__ == "__main__":
    main(BASE_URL, X_START, X_END, Y_START, Y_END)

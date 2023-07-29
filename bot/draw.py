from PIL import Image, ImageDraw, ImageFont


def paint_x(idraw, size, depth=2, i=0, j=0):
    for k in range(size // 30, size // 3 - size // 30):
        idraw.rectangle(
            (k + j * size // 3, k + i * size // 3, k + j * size // 3 + depth, k + i * size // 3 + depth),
            fill='black')
        idraw.rectangle((size // 3 - k + j * size // 3, k + i * size // 3,
                         size // 3 - k + depth + j * size // 3, k + depth + i * size // 3), fill='black')


def paint_o(idraw, size, count_diag=3, depth=2, i=0, j=0):
    points = [{'x': 0, 'y': 0} for _ in range(8)]
    points[0]['x'] = 2 * size // 30 + j * size // 3
    points[0]['y'] = size // 30 + depth + i * size // 3
    points[1]['x'] = 2 * size // 30 + depth + j * size // 3
    points[1]['y'] = size // 3 - 2 * size // 30 + i * size // 3

    points[2]['x'] = points[1]['x'] + count_diag
    points[2]['y'] = points[1]['y'] + count_diag
    points[3]['x'] = size // 3 - 2 * size // 30 - depth - count_diag + j * size // 3
    points[3]['y'] = size // 3 - 2 * size // 30 + depth + count_diag + i * size // 3

    points[5]['x'] = size // 3 - 2 * size // 30 + j * size // 3
    points[5]['y'] = points[1]['y']
    points[4]['x'] = size // 3 - 2 * size // 30 - depth + j * size // 3
    points[4]['y'] = size // 30 + depth + i * size // 3

    points[7]['x'] = points[4]['x'] - count_diag
    points[7]['y'] = points[4]['y'] - count_diag
    points[6]['x'] = points[0]['x'] + depth + count_diag
    points[6]['y'] = points[0]['y'] - depth - count_diag

    for k in range(4):
        idraw.rectangle((points[2 * k]['x'], points[2 * k]['y'], points[2 * k + 1]['x'], points[2 * k + 1]['y']),
                        fill='black')
    for k in range(count_diag):
        idraw.rectangle(
            (points[0]['x'] + depth + k, points[0]['y'] - k, points[0]['x'] + depth + k + 1, points[0]['y'] - k + 1),
            fill='black')
        idraw.rectangle(
            (points[7]['x'] + k, points[7]['y'] + k, points[7]['x'] + k + 1, points[7]['y'] + k + 1),
            fill='black')
        idraw.rectangle(
            (points[1]['x'] + k, points[1]['y'] + k, points[1]['x'] + k + 1, points[1]['y'] + k + 1),
            fill='black')
        idraw.rectangle(
            (points[3]['x'] + k, points[3]['y'] - depth - k, points[3]['x'] + k + 1, points[3]['y'] - depth - k + 1),
            fill='black')


def paint_grid(idraw, size):
    idraw.rectangle((size // 3 - 2, 0, size // 3 + 2, size), fill='black')
    idraw.rectangle((size - size // 3 - 2, 0, size - size // 3 + 2, size), fill='black')

    idraw.rectangle((0, size // 3 - 2, size, size // 3 + 2), fill='black')
    idraw.rectangle((0, size - size // 3 - 2, size, size - size // 3 + 2), fill='black')


def paint_field(field):
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    idraw = ImageDraw.Draw(img)

    paint_grid(idraw, size)
    for i in range(3):
        for j in range(3):
            if field[i][j] == 1:
                paint_x(idraw, size, i=i, j=j)
            elif field[i][j] == 2:
                paint_o(idraw, size, i=i, j=j)

    img.save('field.jpg')

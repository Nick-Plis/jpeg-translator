def ppm_tokenize(stream):
    token_list = []
    # iterating each line in file
    for line in stream:
        try:
            split = line.split('#', 1)
            split_first = split[0].split()
            for item in split_first:
                token_list.append(item)

        except Exception as e:
            line_split = line.split()
            for item in line_split:
                token_list.append(item)

    return token_list


def ppm_load(stream):
    global w
    global h
    global img
    x = 0
    arr_row = []
    arr = []
    img = []
    for line in stream:
        x += 1
        if x == 2:
            split_sc_line = line.split()
            w = split_sc_line[0]
            h = split_sc_line[1]
            break
        else:
            pass
    for line in stream:
        x += 1
        if 4 <= x:
            # splitting lines in file by "#" symbol
            try:
                split = line.split('#', 1)
                split_first = split[0].split()
                for item in split_first:
                    arr_row.append(item)
                arr.append(tuple(arr_row))
                arr_row = []
            except Exception as e:
                line_split = line.split()
                for item in line_split:
                    arr_row.append(item)
                arr.append(tuple(arr_row))
                arr_row = []
        else:
            pass
    for i in range(int(h)):
        rows = []
        for j in range(int(w)):
            index = (int(h) + 1) * i + j
            rows.append(arr[index])
        img.append(rows)
    return w, h, img


def ppm_save(w, h, img):
    with open('new.ppm', 'w') as f:
        f.write(f'P3\n{w} {h}\n255\n')
        for i in img:
            for j in i:
                for p in j:
                    f.write(f'{p} ')
                f.write('\n')


def RGB2YCbCr(r, g, b):
    y = r + g + b
    cb = y - b
    cr = y - r
    return y, cb, cr


def YCbCr2RGB(y, cb, cr):
    r = y - cr
    b = y - cb
    g = y - r - b
    return r, g, b


def img_RGB2YCbCr(img):
    it = 0
    r = 0
    g = 0
    b = 0
    row_y = []
    row_cb = []
    row_cr = []
    mat_y = []
    mat_cb = []
    mat_cr = []
    for i in img:
        for j in i:
            for p in j:
                if it == 0:
                    r = int(p)
                elif it == 1:
                    g = int(p)
                elif it == 2:
                    b = int(p)
                it += 1
            row_y.append(r + g + b)
            row_cb.append(r + g)
            row_cr.append(g + b)
            r = 0
            g = 0
            b = 0
            it = 0
        mat_y.append(row_y)
        mat_cb.append(row_cb)
        mat_cr.append(row_cr)
        row_y = []
        row_cb = []
        row_cr = []

    return mat_y, mat_cb, mat_cr


def img_YCbCr2RGB(y, cb, cr):
    img_mat = []
    img_row = []
    tup = []
    i_index = 0
    j_index = 0
    r = 0
    g = 0
    b = 0
    for i in y:
        i_index = y.index(i)
        for j in i:
            # calculating RGB values
            r = y[i_index][j_index] - cr[i_index][j_index]
            g = y[i_index][j_index] - (y[i_index][j_index] - cr[i_index][j_index]) - (y[i_index][j_index] - cb[i_index][j_index])
            b = y[i_index][j_index] - cb[i_index][j_index]
            tup.append(r)
            tup.append(g)
            tup.append(b)
            img_row.append(tuple(tup))
            tup = []
            j_index += 1
        j_index = 0
        img_mat.append(img_row)
        img_row = []
    return img_mat

def subsampling(w, h, C, a, b):
    buffer = []
    sub = []
    block_rows_done = 0
    block = 0

    if h < b:
        b = h
    else:
        pass

    if w < a:
        a = w
    else:
        pass

    # iterating "blocks" in matrix using height and width of it
    for i in range(round(h / b + 0.499)):
        for block in range(round(w / a + 0.499)):
            for row in C[0+b*block_rows_done:b+b*block_rows_done]:
                for item in row[(0+block*a):(a+block*a)]:
                    buffer.append(item)
            sub.append(round(sum(buffer)/len(buffer)))
            print(buffer)
            buffer = []
        block_rows_done += 1

    return sub


#1.1
with open('file.ppm') as stream:
    for token in ppm_tokenize(stream):
        print(token)

#1.2
with open('file.ppm') as stream:
    w, h, img = ppm_load(stream)
    print(w)
    print(h)
    print(img)

#1.3
ppm_save(w, h, img)

#2.1
r = 146
g = 65
b = 15
y, cb, cr = RGB2YCbCr(r, g, b)
print(y)
print(cb)
print(cr)

#2.2
y = 226
cb = 211
cr = 80
r, g, b = YCbCr2RGB(y, cb, cr)
print(r)
print(g)
print(b)

#2.3
y, cb, cr = img_RGB2YCbCr(img)
print(y)
print(cb)
print(cr)

#2.4
img = img_YCbCr2RGB(y, cb, cr)
print(img)

#3.1
w = 5
h = 4
C = [[43, 250, 58, 5, 240],
     [0, 193, 15, 201, 53],
     [39, 150, 167, 119, 0],
     [89, 26, 55, 14, 138]]
a = 2
b = 3
sub = subsampling(w, h, C, a, b)
print(sub)

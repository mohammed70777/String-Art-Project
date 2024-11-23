import cv2
import numpy as np
import matplotlib.pyplot as plt

# تحميل الصورة وتحويلها إلى تدرج رمادي
def load_image(image_path, size=(500, 500)):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, size)  # تغيير الحجم
    return img

# توليد المسامير على حواف الشكل
def generate_nails(image, num_nails=200, shape='circle'):
    h, w = image.shape
    center = (w // 2, h // 2)
    radius = min(h, w) // 2 - 20

    nails = []
    if shape == 'circle':
        for i in range(num_nails):
            angle = 2 * np.pi * i / num_nails
            x = int(center[0] + radius * np.cos(angle))
            y = int(center[1] + radius * np.sin(angle))
            nails.append((x, y))
    elif shape == 'square':
        side = np.linspace(0, 1, num_nails // 4, endpoint=False)
        for x in side:
            nails.append((int(x * w), 0))  # الحافة العلوية
        for y in side:
            nails.append((w - 1, int(y * h)))  # الحافة اليمنى
        for x in reversed(side):
            nails.append((int(x * w), h - 1))  # الحافة السفلية
        for y in reversed(side):
            nails.append((0, int(y * h)))  # الحافة اليسرى
    return nails

# رسم الخطوط بين النقاط مع تحسين الأداء
def create_string_art(image, nails, num_lines=1000):
    h, w = image.shape
    lines = []
    current_nail = 0
    mask = np.zeros_like(image)  # لتحسين الأداء
    for _ in range(num_lines):
        intensities = []
        for i, (x, y) in enumerate(nails):
            line_mask = np.zeros_like(image)
            cv2.line(line_mask, nails[current_nail], (x, y), 255, 1)
            combined_mask = cv2.bitwise_and(line_mask, cv2.bitwise_not(mask))
            intensity = cv2.mean(image, mask=combined_mask)[0]
            intensities.append((intensity, i))

        next_nail = max(intensities, key=lambda x: x[0])[1]
        lines.append((current_nail, next_nail))
        cv2.line(mask, nails[current_nail], nails[next_nail], 255, 1)  # تحديث القناع
        current_nail = next_nail
    return lines

# رسم الشكل النهائي
def draw_string_art(image, nails, lines, line_thickness=1):
    output = np.ones_like(image) * 255
    for start, end in lines:
        cv2.line(output, nails[start], nails[end], 0, line_thickness)
    return output

# حفظ الصورة النهائية
def save_output(output, filename):
    cv2.imwrite(filename, output)

# تنفيذ الخطوات
image_path = "/mnt/data/1.jpg"  # ضع مسار الصورة هنا
output_path = "/mnt/data/string_art_output.jpg"  # مسار الحفظ

image = load_image(image_path)
nails = generate_nails(image, num_nails=200, shape='square')  # يمكن تغيير الشكل إلى 'circle' أو 'square'
lines = create_string_art(image, nails, num_lines=1000)
output = draw_string_art(image, nails, lines)

# عرض وحفظ النتيجة
plt.imshow(output, cmap='gray')
plt.axis('off')
plt.show()
save_output(output, output_path)
print(f"تم حفظ النتيجة في: {output_path}")

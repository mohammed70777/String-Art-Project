<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>String Art</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.6.0/p5.min.js"></script>
</head>
<body>
  <script>
    let img;
    let nails = [];
    let numNails = 200;
    let lines = [];
    let numLines = 1000;

    function preload() {
      img = loadImage('your-image.jpg'); // تأكد من رفع الصورة في نفس المجلد
    }

    function setup() {
      createCanvas(500, 500);
      img.resize(500, 500);
      img.loadPixels();

      // توليد المسامير بشكل دائرة
      let centerX = width / 2;
      let centerY = height / 2;
      let radius = min(width, height) / 2 - 20;

      for (let i = 0; i < numNails; i++) {
        let angle = TWO_PI * i / numNails;
        let x = centerX + radius * cos(angle);
        let y = centerY + radius * sin(angle);
        nails.push(createVector(x, y));
      }

      // توليد الخطوط
      let currentNail = 0;
      for (let i = 0; i < numLines; i++) {
        let bestNail = 0;
        let bestIntensity = 0;

        for (let j = 0; j < nails.length; j++) {
          if (j === currentNail) continue;

          let intensity = calculateLineIntensity(nails[currentNail], nails[j]);
          if (intensity > bestIntensity) {
            bestIntensity = intensity;
            bestNail = j;
          }
        }

        lines.push([currentNail, bestNail]);
        currentNail = bestNail;
      }
    }

    function draw() {
      background(255);
      stroke(0);

      for (let line of lines) {
        let start = nails[line[0]];
        let end = nails[line[1]];
        line(start.x, start.y, end.x, end.y);
      }

      noLoop(); // وقف التحديث بعد رسم الشكل
    }

    function calculateLineIntensity(start, end) {
      let x1 = floor(start.x);
      let y1 = floor(start.y);
      let x2 = floor(end.x);
      let y2 = floor(end.y);

      let sum = 0;
      let count = 0;

      let dx = abs(x2 - x1);
      let dy = abs(y2 - y1);
      let sx = (x1 < x2) ? 1 : -1;
      let sy = (y1 < y2) ? 1 : -1;
      let err = dx - dy;

      while (true) {
        let index = (y1 * img.width + x1) * 4;
        let brightness = img.pixels[index];
        sum += brightness;
        count++;

        if (x1 === x2 && y1 === y2) break;
        let e2 = err * 2;
        if (e2 > -dy) {
          err -= dy;
          x1 += sx;
        }
        if (e2 < dx) {
          err += dx;
          y1 += sy;
        }
      }

      return sum / count;
    }
  </script>
</body>
</html>

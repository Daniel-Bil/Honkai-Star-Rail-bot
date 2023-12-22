import cv2
import numpy as np




if __name__ == "__main__":
    img_rgb = cv2.imread('.//test_images//express_inside.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('.//test_images//templates//nameless_template.png', cv2.IMREAD_GRAYSCALE)
    # template = cv2.resize(template, (int(template.shape[1] * 30 / 100),int(template.shape[0] * 90 / 100)), interpolation=cv2.INTER_AREA)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    print(loc)
    print(len(loc[0]))
    p1, p2 = loc[::-1]
    print("p1")
    print(p1)
    print(p2)
    print(*loc[::-1][0])
    print(*loc[::-1][1])
    for pt in zip(*loc[::-1]):
        print(pt[0])
        print(pt[1])
        cv2.rectangle(img_rgb, pt, (pt[0] + 50, pt[1] + 50), (0, 0, 255), 2)
    cv2.imshow("name", img_rgb)
    cv2.waitKey(0)
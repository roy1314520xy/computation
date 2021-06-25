from PIL import Image
from inference_color import get_colors
import cv2
import numpy as np
COLORS = [(0,0,0),(0,0,255),(0,255,0),(70,130,180),(238,238,0),(255,69,0),(205,145,158),(238,92,66),(144,238,144),(124,205,124),(0,229,238),(151,255,255),(162,205,90),(210,105,30),(144,238,144),(139,129,76),(255,245,238),(238,106,167),(65,105,225),(255,165,0),(205,55,0),(139,101,8),(205,149,12),(0,100,0),(69,139,0),(238,169,184),(139,117,0),(178,58,238),(143,188,143),(255,130,71),(191,62,255),(0,0,205),(160,32,240),(205,0,205),(230,230,250),(0,0,255),(126,192,238),(0,255,0),(0,255,127),(255,99,71),(255,48,48),(205,133,63),(205,85,85),(154,255,154),(238,122,233),(255,193,37),(219,112,147),(0,0,255),(0,255,0),(165,42,42),(108,166,205),(180,82,205),(84,255,159),(145,44,238),(102,205,170),(139,71,38),(205,198,115),(67,205,128),(205,104,57),(250,128,114),(205,102,29),(0,0,128),(205,16,118),(238,221,130),(139,10,80),(95,158,160),(30,144,255),(255,246,143),(39,64,139),(205,50,120),(193,255,193),(255,215,0),(107,142,35),(205,41,144),(255,248,220),(255,62,150),(255,215,0),(205,155,29),(159,121,238),(67,110,238),(238,118,33),(152,245,255),(255,236,139),(174,238,238),(255,165,0),(255,228,225),(0,205,205),(141,238,238),(238,48,167),(176,48,96),(184,134,11),(205,38,38),(238,58,140),(255,0,255),(205,92,92),(124,252,0),(255,165,79),(178,34,34),(238,162,173),(238,220,130),(238,154,73),(0,191,255),(255,0,255),(255,174,185),(250,250,210),(34,139,34),(99,184,255),(205,133,63),(83,134,139),(255,127,80),(139,0,139),(139,71,137),(30,144,255),(123,104,238),(155,48,255),(24,116,205),(139,58,98),(255,69,0),(186,85,211),(238,173,14),(16,78,139),(205,140,149),(72,118,255),(0,255,255),(238,232,170),(0,139,69),(135,206,235),(79,148,205),(92,172,238),(32,178,170),(72,61,139),(69,139,116),(238,154,0),(238,44,44),(205,105,201),(218,112,214),(138,43,226),(238,0,0),(255,114,86),(58,95,205),(238,106,80),(72,209,204),(238,64,0),(50,205,50),(255,99,71),(240,128,128),(152,251,152),(255,255,0),(205,96,144),(238,99,99),(125,38,205),(84,139,84),(222,184,135),(255,20,147),(205,51,51),(82,139,139),(205,79,57),(139,90,0),(137,104,205),(255,110,180),(238,201,0),(0,0,139),(106,90,205),(0,0,205),(60,179,113),(255,240,245),(0,139,139),(205,173,0),(102,205,0),(255,52,179),(240,255,240),(139,105,20),(255,185,15),(255,105,180),(0,139,139),(0,0,238),(179,238,58),(175,238,238),(238,180,180),(255,181,197),(205,155,155),(155,205,155),(127,255,0),(127,255,212),(28,134,238),(0,178,238),(122,103,238),(135,206,255),(180,238,180),(205,133,0),(0,205,0),(209,95,238),(131,111,255),(255,127,36),(0,139,0),(0,205,102),(132,112,255),(205,104,137),(0,197,205),(135,206,250),(102,139,139),(238,130,98),(255,228,181),(255,140,0),(25,25,112),(255,0,0),(139,0,0),(148,0,211),(0,154,205),(154,205,50),(64,224,208),(0,255,127),(105,139,34),(255,250,205),(85,107,47),(139,134,78),(233,150,122),(0,206,209),(0,134,139),(255,0,0),(238,130,238),(255,255,0),(238,230,133),(153,50,204),(255,130,171),(47,79,79),(202,255,112),(255,222,173),(205,102,0),(110,139,61),(176,196,222),(245,222,179),(218,165,32),(46,139,87),(189,183,107),(255,64,64),(238,180,34),(238,121,66),(255,193,193),(238,121,159),(255,20,147),(199,21,133),(0,245,255),(147,112,219),(187,255,255),(100,149,237),(0,238,0),(127,255,212),(139,69,0),(78,238,148),(139,139,0),(255,160,122),(0,255,255),(160,82,45),(105,89,205),(0,191,255),(238,0,238),(127,255,0),(208,32,144),(102,205,170),(171,130,255),(221,160,221),(139,58,58),(216,191,216),(139,0,139),(118,238,0),(192,255,62),(0,238,118),(173,255,47),(154,205,50),(255,131,250),(224,102,255),(205,0,0),(205,91,69),(0,250,154),(255,127,0),(142,229,238),(0,238,238),(46,139,87),(122,55,139),(0,0,139),(244,164,96),(105,139,105),(255,218,185),(255,106,106),(238,118,0),(154,50,205),(121,205,205),(122,197,205),(118,238,198),(205,205,0),(255,140,105),(188,238,104),(238,59,59),]
def transparent_back(img):
    #img = Image.open('this.jpg')
    # 图片转换为四通道。第四个通道就是我们要修改的透明度。返回新的对象
    img = img.convert('RGBA')
    # 获取图片像素尺寸
    width, height = img.size
    pixel_data = img.load()
    for h in range(height):
        for w in range(width):
            pixel = pixel_data[w, h]
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            a = pixel[3]
            # 四通道，色彩值大于浅灰色，则将像素点变为透明块
            if r == 0 and g == 0 and b == 0 and a>=0:
                pixel_data[w, h] = (255, 255, 255, 0)
    img=img.convert("RGB")
    return img
def confusion_image(img,mask,real_mask):
    output_image=[]
    output_masks=[]
    img=img*255 #之前归一化过
    w, h = img.shape[2], img.shape[3]
    for idx in range(0,len(img)):

        img_mask = np.zeros([h, w, 3], np.uint8)
        true_mask = np.zeros([h, w, 3], np.uint8)

        image_idx = Image.fromarray((mask[idx].squeeze().cpu().numpy() * 255).astype(np.uint8))
        array_img = np.asarray(image_idx)
        img_mask[np.where(array_img == 255)] = COLORS[1]

        mask_idx = Image.fromarray((real_mask[idx].squeeze().cpu().numpy() * 255).astype(np.uint8))
        array_mask = np.asarray(mask_idx)
        true_mask[np.where(array_mask == 255)] = COLORS[2]

        img_mask = Image.fromarray((img_mask).astype(np.uint8))
        true_mask = Image.fromarray((true_mask).astype(np.uint8))
        # img_mask = transparent_back(img_mask)
        # true_mask = transparent_back(true_mask)
        if img[idx].shape[0]==1:
            out_img = cv2.cvtColor(np.asarray(img[idx].squeeze().cpu().numpy()).astype(np.uint8), cv2.COLOR_GRAY2BGR)
        else:
            out_img = cv2.cvtColor(np.asarray(img[idx].cpu().numpy()).astype(np.uint8), cv2.COLOR_RGB2BGR)

        img_mask = cv2.cvtColor(np.asarray(img_mask), cv2.COLOR_RGB2BGR)
        true_mask = cv2.cvtColor(np.asarray(true_mask), cv2.COLOR_RGB2BGR)

        out_mask = cv2.addWeighted(true_mask, 0.5, img_mask, 0.5, 0)
        output = cv2.addWeighted(out_img, 0.7, out_mask, 0.3, 0)

        output_image.append(output)
        output_masks.append(img_mask)
    output_image=np.asarray(output_image)
    output_masks=np.asarray(output_masks)

    return output_image,output_masks
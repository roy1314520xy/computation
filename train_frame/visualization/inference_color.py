# -*- coding: utf-8 -*-
# @Time    : 2020-02-26 17:53
# @Author  : Zonas
# @Email   : zonas.wang@gmail.com
# @File    : inference.py
"""

"""
import argparse
import logging
import os
import os.path as osp
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from tqdm import tqdm
import cv2



COLORS = [(0,0,0),(0,0,255),(0,255,0),(70,130,180),(238,238,0),(255,69,0),(205,145,158),(238,92,66),(144,238,144),(124,205,124),(0,229,238),(151,255,255),(162,205,90),(210,105,30),(144,238,144),(139,129,76),(255,245,238),(238,106,167),(65,105,225),(255,165,0),(205,55,0),(139,101,8),(205,149,12),(0,100,0),(69,139,0),(238,169,184),(139,117,0),(178,58,238),(143,188,143),(255,130,71),(191,62,255),(0,0,205),(160,32,240),(205,0,205),(230,230,250),(0,0,255),(126,192,238),(0,255,0),(0,255,127),(255,99,71),(255,48,48),(205,133,63),(205,85,85),(154,255,154),(238,122,233),(255,193,37),(219,112,147),(0,0,255),(0,255,0),(165,42,42),(108,166,205),(180,82,205),(84,255,159),(145,44,238),(102,205,170),(139,71,38),(205,198,115),(67,205,128),(205,104,57),(250,128,114),(205,102,29),(0,0,128),(205,16,118),(238,221,130),(139,10,80),(95,158,160),(30,144,255),(255,246,143),(39,64,139),(205,50,120),(193,255,193),(255,215,0),(107,142,35),(205,41,144),(255,248,220),(255,62,150),(255,215,0),(205,155,29),(159,121,238),(67,110,238),(238,118,33),(152,245,255),(255,236,139),(174,238,238),(255,165,0),(255,228,225),(0,205,205),(141,238,238),(238,48,167),(176,48,96),(184,134,11),(205,38,38),(238,58,140),(255,0,255),(205,92,92),(124,252,0),(255,165,79),(178,34,34),(238,162,173),(238,220,130),(238,154,73),(0,191,255),(255,0,255),(255,174,185),(250,250,210),(34,139,34),(99,184,255),(205,133,63),(83,134,139),(255,127,80),(139,0,139),(139,71,137),(30,144,255),(123,104,238),(155,48,255),(24,116,205),(139,58,98),(255,69,0),(186,85,211),(238,173,14),(16,78,139),(205,140,149),(72,118,255),(0,255,255),(238,232,170),(0,139,69),(135,206,235),(79,148,205),(92,172,238),(32,178,170),(72,61,139),(69,139,116),(238,154,0),(238,44,44),(205,105,201),(218,112,214),(138,43,226),(238,0,0),(255,114,86),(58,95,205),(238,106,80),(72,209,204),(238,64,0),(50,205,50),(255,99,71),(240,128,128),(152,251,152),(255,255,0),(205,96,144),(238,99,99),(125,38,205),(84,139,84),(222,184,135),(255,20,147),(205,51,51),(82,139,139),(205,79,57),(139,90,0),(137,104,205),(255,110,180),(238,201,0),(0,0,139),(106,90,205),(0,0,205),(60,179,113),(255,240,245),(0,139,139),(205,173,0),(102,205,0),(255,52,179),(240,255,240),(139,105,20),(255,185,15),(255,105,180),(0,139,139),(0,0,238),(179,238,58),(175,238,238),(238,180,180),(255,181,197),(205,155,155),(155,205,155),(127,255,0),(127,255,212),(28,134,238),(0,178,238),(122,103,238),(135,206,255),(180,238,180),(205,133,0),(0,205,0),(209,95,238),(131,111,255),(255,127,36),(0,139,0),(0,205,102),(132,112,255),(205,104,137),(0,197,205),(135,206,250),(102,139,139),(238,130,98),(255,228,181),(255,140,0),(25,25,112),(255,0,0),(139,0,0),(148,0,211),(0,154,205),(154,205,50),(64,224,208),(0,255,127),(105,139,34),(255,250,205),(85,107,47),(139,134,78),(233,150,122),(0,206,209),(0,134,139),(255,0,0),(238,130,238),(255,255,0),(238,230,133),(153,50,204),(255,130,171),(47,79,79),(202,255,112),(255,222,173),(205,102,0),(110,139,61),(176,196,222),(245,222,179),(218,165,32),(46,139,87),(189,183,107),(255,64,64),(238,180,34),(238,121,66),(255,193,193),(238,121,159),(255,20,147),(199,21,133),(0,245,255),(147,112,219),(187,255,255),(100,149,237),(0,238,0),(127,255,212),(139,69,0),(78,238,148),(139,139,0),(255,160,122),(0,255,255),(160,82,45),(105,89,205),(0,191,255),(238,0,238),(127,255,0),(208,32,144),(102,205,170),(171,130,255),(221,160,221),(139,58,58),(216,191,216),(139,0,139),(118,238,0),(192,255,62),(0,238,118),(173,255,47),(154,205,50),(255,131,250),(224,102,255),(205,0,0),(205,91,69),(0,250,154),(255,127,0),(142,229,238),(0,238,238),(46,139,87),(122,55,139),(0,0,139),(244,164,96),(105,139,105),(255,218,185),(255,106,106),(238,118,0),(154,50,205),(121,205,205),(122,197,205),(118,238,198),(205,205,0),(255,140,105),(188,238,104),(238,59,59),]




def inference_one(net, image, device):
    net.eval()
    global args
    img = torch.from_numpy(BasicDataset.preprocess(image))#your data preprocess procedure
    img = img.unsqueeze(0)
    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():
        output = net(img)
        if output.shape[0] > 1:
            probs = F.softmax(output, dim=1)
        else:
            probs = torch.sigmoid(output)

        probs = probs.squeeze(0)        # C x H x W

        tf = transforms.Compose(
                [
                    transforms.ToPILImage(),
                    transforms.Resize((image.size[1], image.size[0])),
                    transforms.ToTensor()
                ]
        )

        if output.shape[0] == 1:
            probs = tf(probs.cpu())
            mask = probs.squeeze().cpu().numpy()
            print("this!!")
            return mask > args.out_threshold

        else:
            masks = []
            for prob in probs:
                prob = tf(prob.cpu())
                mask = prob.squeeze().cpu().numpy()
                mask = mask > args.out_threshold
                masks.append(mask)
            return masks


def get_args():
    parser = argparse.ArgumentParser(description='Predict masks from input images',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--modelweight', '-m', default='.//weight//best_score12.pth',
                        metavar='FILE',
                        help="Specify the file in which the modelweight is stored")
    parser.add_argument('--input', '-i', dest='input', type=str, default='.//weight//楔形体入水',
                        help='Directory of input images')
    parser.add_argument('--output', '-o', dest='output', type=str, default='.//weight//outnew624',
                        help='Directory of ouput images')
    parser.add_argument('--model', type=str, default='U_Net')
    parser.add_argument('--mode', type=str, default='add', help='addweight with img/mask(add) or just single mask(single)')
    parser.add_argument('--intputchannel',type=int,default=1)
    parser.add_argument('--outputchannel', type=int, default=1)
    parser.add_argument('--out_threshold', type=float, default=0.8)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    input_imgs = os.listdir(args.input)
    output_img_dir = osp.join(args.output)

    net=eval(args.model)(args.intputchannel,args.outputchannel)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logging.info(f'Using device {device}')
    net.to(device=device)
    net.load_state_dict(torch.load(args.modelweight, map_location=device))
    logging.info("Loading model{},weight {}".format(args.model, args.modelweight))
    logging.info("Model loaded !")


    for i, img_name in tqdm(enumerate(input_imgs)):
        logging.info("\nPredicting image {} ...".format(img_name))
        img_path = osp.join(args.input, img_name)

        img = Image.open(img_path)
        mask = inference_one(net=net,
                             image=img,
                             device=device
                             )
        img_name_no_ext = osp.splitext(img_name)[0]
        os.makedirs(output_img_dir, exist_ok=True)

        if args.outputchannel == 1:

            image_idx = (mask * 255).astype(np.uint8)
            w, h = img.size
            img_mask = np.zeros([h, w, 3], np.uint8)
            img_mask[np.where(image_idx == 255)] = COLORS[1]
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_GRAY2BGR)
            output = cv2.addWeighted(img, 0.7, img_mask, 0.3, 0)
            if args.mode=='add':
                cv2.imwrite(osp.join(output_img_dir, img_name),output)
            else:
                cv2.imwrite(osp.join(output_img_dir, img_name), image_idx)

        else:

            w, h = img.size
            img_mask = np.zeros([h, w, 3], np.uint8)
            for idx in range(0, len(mask) if len(mask)>1 else 1):
                image_idx = Image.fromarray((mask[idx] * 255).astype(np.uint8))
                array_img = np.asarray(image_idx)
                img_mask[np.where(array_img==255)] = COLORS[idx]
            img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
            img_mask = cv2.cvtColor(np.asarray(img_mask),cv2.COLOR_RGB2BGR)
            output = cv2.addWeighted(img, 0.7, img_mask, 0.3, 0)
            if args.mode == 'add':
                cv2.imwrite(osp.join(output_img_dir, img_name), output)
            else:
                cv2.imwrite(osp.join(output_img_dir, img_name), img_mask)


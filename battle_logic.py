import time

import cv2
from colorama import Fore


def w84endbattle():
    while True:
        img = get_image()
        battle = check_if_endbattle(img)
        time.sleep(3)
        if battle:
            print(f"{Fore.LIGHTRED_EX} END BATTLE {Fore.RESET}")
            break
        print("STILL IN BATTLE")

def check_if_endbattle(image):
    rgbs = []
    for i in range(3):

        cord = out_of_battle_cord_dict[f"icon{i+1}"]
        cropped = crop(image, cord)
        rgb = cropped
        rgbs.append(rgb)
    v = 0
    for rgb in rgbs:
        print(rgb)
        if (rgb > 200).all():
            v+=1

    if v == 3:
        return True
    else:
        return False

def start_autobattle():
    time.sleep(0.5)
    mouse = Controller()
    mouse.position = (2350, 67)
    time.sleep(0.5)

    mouse.click(Button.left)
    time.sleep(0.5)


def locate_enemy_and_start_battle(model, c_t_l = None):
    if c_t_l is None:
        c_t_l = {0: "eliminator",
                 1: "disruptor",
                 2: "reaver",
                 3: "antibaryon"}
    timeout = 0
    sct = mss()
    monitor = {'top': 0, 'left': 0, 'width': IMAGE_WIDTH, 'height': IMAGE_HEIGHT}
    from PIL import Image
    while True:
        # time.sleep(0.7)

        img = Image.frombytes('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), sct.grab(monitor).rgb)
        # img = np.array(img)
        whole_image = np.array(img)
        screen = np.array(img)
        # screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        screen = cv2.resize(screen, (640, 640))
        # print(screen)

        result = model(screen)

        labels, cord = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]

        n = len(labels)
        print(n)
        if n > 0:
            timeout -= 1
            v = 0
            for h, c in enumerate(cord):
                if int(labels[h].cpu().item()) == 13 or int(labels[h].cpu().item()) == 14:
                    v = None
                    pass
                else:
                    row = cord[h]
                    v = h
                    break
            if v is not None:
                if row[4] >= 0.5:
                    x1, y1, x2, y2 = int(row[0] * 640), int(row[1] * 640), int(row[2] * 640), int(row[0] * 640)
                    xc = (x1 + x2) / 2
                    yc = (y1 + y2) / 2
                    print(f"{Fore.GREEN} {xc} {yc} {(x2 - x1)} {Fore.RESET}")
                    if 320 - 64 < xc < 320 + 64:
                        przod(0.1)
                        random_value3 = random.randint(0, 100)
                        if random_value3 < 5:
                            random_value4 = random.randint(0, 1)
                            if random_value4==0:
                                tyl(0.5)
                                right(0.5)
                            else:
                                tyl(0.5)
                                left(0.5)
                        if (x2 - x1) > 45:
                            attack()
                    elif xc < 320 - 64:
                        turn(-5)
                    elif xc > 320 - 64:
                        turn(5)
                    else:
                        print("XDDDD")

                    leb = labels[h].cpu()

                    cv2.rectangle(screen, (x1, y1), (x2, y2), colors[0], 2)
                    try:
                        cv2.putText(screen, f"{c_t_l[int(leb.item())]} {row[4]}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)
                    except:
                        pass
            else:
                print(f"{Fore.LIGHTMAGENTA_EX} LOOKING FOR ENEMY inside {timeout} < 60 {Fore.RESET}")
                random_value = random.randint(0, 1)
                random_value2 = random.randint(1, 100)
                if random_value == 0:
                    turn(random_value2)
                else:
                    turn(-random_value2)
                timeout += 1

            if timeout > 60:
                print(f"{Fore.RED} TIMEOUT NO ENEMY FOUND {Fore.RESET}")
                break

            battle = check_if_battle(whole_image)
            if battle:
                print(f"{Fore.LIGHTCYAN_EX} FIGHT STARTED {Fore.RESET}")
                time.sleep(4)
                print("start autobattle")
                start_autobattle()
                break
        else:
            print(f"{Fore.LIGHTMAGENTA_EX} LOOKING FOR ENEMY  {timeout} < 30 {Fore.RESET}")
            random_value = random.randint(1, 100)
            turn(random_value)
            timeout+=1

        if timeout > 30:
            print(f"{Fore.RED} TIMEOUT NO ENEMY FOUND {Fore.RESET}")
            break

        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        cv2.namedWindow("Screen")
        cv2.moveWindow("Screen", -2560, 0)
        cv2.imshow("Screen", screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
import torch


def load_model(planet: str = "Herta"):
    """
    Function that loads model for current planet
    :param planet: name of the planet
    :return:
    """
    if planet == "Herta":
        model = torch.hub.load(f'ultralytics/yolov5', 'custom', path=f'E:/Honkai-Star-Rail-bot/model/herta_deeplearning_200.pt')
    elif planet == "Jarilo6":
        model = torch.hub.load(f'ultralytics/yolov5', 'custom', path=f'E:/Honkai-Star-Rail-bot/model/jarilo4.pt')
    elif planet == "xianzhou":
        # model = torch.hub.load(f'ultralytics/yolov5', 'custom',
        #                        path=f'E:/Honkai-Star-Rail-bot/model/hertaSpaceStation.pt')
        raise NotImplementedError("Planet not implemented")
    elif planet == "panacony":
        raise NotImplementedError("Planet not implemented")
    else:
        raise Exception("wrong planet")
    return model
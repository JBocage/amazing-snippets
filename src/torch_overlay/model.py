import torch
import torch.nn as nn
import pathlib

class ModelAbstract(nn.Module):

    CHECKPOINT_DIR = pathlib.Path(__file__).resolve().absolute().parent/'chkpt'

    def __init__(self):
        super(ModelAbstract, self).__init__()
        self.CHECKPOINT_DIR.mkdir(exist_ok=True)

    def forward(self, x:torch.Tensor) -> torch.Tensor:
        return x

    def load_model(self, folder_name):
        savepath = self.CHECKPOINT_DIR/folder_name
        self.network.load_state_dict(
            torch.load(savepath/('model_parameters.chkpt'), map_location=torch.device('cpu')))

    def save_model(self, folder_name):
        savepath = self.CHECKPOINT_DIR / folder_name
        savepath.mkdir(exist_ok=True, parents=True)
        torch.save(self.network.state_dict(),
                   savepath/('model_parameters.chkpt'))

    def eval_mode(self):
        self.eval()

    def train_mode(self):
        self.train()

    def preprocess(self, x:torch.Tensor) -> torch.Tensor:
        return x

if __name__ == '__main__':
    mdl = ModelAbstract()
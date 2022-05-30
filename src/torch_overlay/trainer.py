from abc import ABC, abstractmethod
import torch.nn as nn
import pathlib
import joblib
import matplotlib.pyplot as plt
from .model import ModelAbstract

class TrainerAbstract(ABC):

    CHECKPOINT_DIR = pathlib.Path(__file__).resolve().absolute().parent/'chkpt'

    def __init__(self, trainer_name='', overwrite_checkpoint=False):

        self.model:ModelAbstract = ModelAbstract()
        self.name = trainer_name

        # DATA_LOADER
        self.train_dataloader = None
        self.val_dataloader = None
        self.test_dataloader = None
        self._build_dataloaders()

        # RESULT
        self.epochs_trained = 0
        self.loss_record = []  # Loss of each batch
        self.loss_record_epochs = []  # Average batch loss per epoch
        self.val_loss_record = []  # Average val loss per epoch
        self.val_acc_record = []

        # LOADING TRAINING INFORMATION (if exist)
        self.save_dest = self.CHECKPOINT_DIR/self.name
        if self.save_dest.exists() and not overwrite_checkpoint:
            # if "Model Checkpoint Folder" exist & overwrite_checkpoint=False
            self.load_state()

    @abstractmethod
    def _build_dataloaders(self):
        pass

    def load_state(self):
        # Load the model chkpt 's state_dict based on Folder Name (self.name)
        self.model.load_model(self.name)
        # Load the trainer state dict
        trainer_state_dict = joblib.load(self.save_dest/'trainer.state')
        # Update the class's parameters based on "trainer.state"
        for k in trainer_state_dict.keys():
            if k in self.__dict__.keys():
                self.__dict__[k] = trainer_state_dict[k]

    def save_state(self):
        self.model.save_model(self.name)
        self.save_loss_fig()
        trainer_state_dict = {
            "epochs_trained": self.epochs_trained,
            "loss_record": self.loss_record,
            "loss_record_epochs": self.loss_record_epochs,
            "val_loss_record": self.val_loss_record,
            "val_acc_record": self.val_acc_record,
        }
        joblib.dump(trainer_state_dict, self.save_dest/'trainer.state')

    def save_loss_fig(self):
        plt.ioff()  # to make the matplotlib not in interactive mode

        fig, ax = plt.subplots()
        ax.plot(self.loss_record, color='blue', label='Loss per Batch')
        ax.plot(self.loss_record_epochs, color='red',
                label='Loss per Epoch')
        ax.plot(self.val_loss_record, color='green',
                label='Val Loss per Epoch')
        ax.set(title=f'Training Loss for {self.name} Model',
               xlabel='Number of Batches trained', ylabel='Log Loss', yscale='log')

        ax.legend()
        plt.tight_layout()

        fig.savefig(self.save_dest/'.trainingloss.png')
        plt.close(fig)
        plt.ion()

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self, print_report=False):
        pass


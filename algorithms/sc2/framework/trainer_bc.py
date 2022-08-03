"""
Simple training loop; Boilerplate that could apply to any arbitrary neural network,
so nothing in this file really has anything to do with GPT specifically.
"""

import math
import logging
import torch
import numpy as np
from tqdm import tqdm
from torch.utils.data.dataloader import DataLoader
from tensorboardX.writer import SummaryWriter
from framework.utils import load_data_bc

from framework.buffer import StateActionReturnDataset

logger = logging.getLogger(__name__)


class TrainerConfig:
    # optimization parameters
    max_epochs = 1000
    batch_size = 128
    learning_rate = 5e-4
    betas = (0.9, 0.95)
    grad_norm_clip = 1.0
    weight_decay = 0.1  # only applied on matmul weights
    # learning rate decay params: linear warmup followed by cosine decay to 10% of original
    lr_decay = False
    warmup_tokens = 375e6  # these two numbers come from the GPT-3 paper, but may not be good defaults elsewhere
    final_tokens = 260e9  # (at what point we reach 10% of original LR)
    # checkpoint settings
    ckpt_path = None
    num_workers = 0  # for DataLoader

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Trainer:

    def __init__(self, model, config):
        self.model = model
        self.config = config
        self.writter = SummaryWriter(config.log_dir)
        self.global_step = 0

        # take over whatever gpus are on the system
        self.device = 'cpu'
        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            self.model = torch.nn.DataParallel(self.model).to(self.device)

    def save_checkpoint(self):
        # DataParallel wrappers keep raw model object in .module attribute
        raw_model = self.model.module if hasattr(self.model, "module") else self.model
        logger.info("saving %s", self.config.ckpt_path)
        # torch.save(raw_model.state_dict(), self.config.ckpt_path)

    def train(self, episodes, data_dir, num_agents):
        model, config = self.model, self.config
        raw_model = model.module if hasattr(self.model, "module") else model
        optimizer = raw_model.configure_optimizers(config)

        def run_epoch(split, dataset):
            is_train = split == 'train'
            final_tokens = 2 * len(dataset) * 3
            model.train(is_train)
            loader = DataLoader(dataset, shuffle=True, pin_memory=True, drop_last=True,
                                batch_size=config.batch_size,
                                num_workers=config.num_workers)

            losses = []
            pbar = tqdm(enumerate(loader), total=len(loader)) if is_train else enumerate(loader)
            logger.info("***** Trainging Begin ******")
            for it, (x, y, r, t) in pbar:
                # place data on the correct device
                x = x.to(self.device)
                y = y.to(self.device)
                r = r.to(self.device)
                t = t.to(self.device)

                # forward the model
                with torch.set_grad_enabled(is_train):
                    # logits, loss = model(x, y, r)
                    logits, loss = model(x, y, y, r, t)
                    loss = loss.mean()  # collapse all losses if they are scattered on multiple gpus
                    losses.append(loss.item())
                logger.info(" Training loss %f", loss.item())
                # self.writter.add_scalars("training loss", {"training loss": loss.item()}, epoch_num * self.config.batch_size)

                if is_train:
                    # backprop and update the parameters
                    model.zero_grad()
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_norm_clip)
                    optimizer.step()

                    # decay the learning rate based on our progress
                    if config.lr_decay:
                        self.tokens += (y >= 0).sum()  # number of tokens processed this step (i.e. label is not -100)
                        if self.tokens < config.warmup_tokens:
                            # linear warmup
                            lr_mult = float(self.tokens) / float(max(1, config.warmup_tokens))
                        else:
                            # cosine learning rate decay
                            progress = float(self.tokens - config.warmup_tokens) / float(
                                max(1, final_tokens - config.warmup_tokens))
                            lr_mult = max(0.1, 0.5 * (1.0 + math.cos(math.pi * progress)))
                        lr = config.learning_rate * lr_mult
                        for param_group in optimizer.param_groups:
                            param_group['lr'] = lr
                    else:
                        lr = config.learning_rate
                    # report progress
                    pbar.set_description(f"epoch {epoch + 1} iter {it}: train loss {loss.item():.5f}. lr {lr:e}")

            if not is_train:
                test_loss = float(np.mean(losses))
                logger.info("test loss: %f", test_loss)
                return test_loss

        self.tokens = 0  # counter used for learning rate decay

        for epoch in range(config.max_epochs):
            bias = 0
            num_step = 20
            for i in range(num_step):
                states, actions, done_idxs, rtgs, timesteps = load_data_bc(int(episodes/num_step),
                                                                           bias,
                                                                           data_dir)
                offline_dataset = StateActionReturnDataset(states, 1, actions, done_idxs, rtgs, timesteps)
                run_epoch('train', offline_dataset)
                bias += int(episodes / num_step)
            self.global_step += 1


    def update_target(self):
        pass
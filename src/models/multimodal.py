import torch
from torch import nn

class Encoder3D(nn.Module):
    def __init__(self, latent_dim=512):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv3d(1, 16, 3, padding=1), nn.BatchNorm3d(16), nn.ReLU(),
            nn.MaxPool3d(2),
            nn.Conv3d(16, 32, 3, padding=1), nn.BatchNorm3d(32), nn.ReLU(),
            nn.MaxPool3d(2),
            nn.Conv3d(32, 64, 3, padding=1), nn.BatchNorm3d(64), nn.ReLU(),
            nn.AdaptiveAvgPool3d(1),
        )
        self.proj = nn.Linear(64, latent_dim)

    def forward(self, x):
        x = self.features(x).flatten(1)
        return self.proj(x)

class FusionHead(nn.Module):
    def __init__(self, latent_dim=512, num_modalities=4, num_classes=5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim*num_modalities, 512), nn.ReLU(),
            nn.Linear(512, 128), nn.ReLU(),
            nn.Linear(128, num_classes),
        )

    def forward(self, z):
        return self.net(z)

class MultiParametricFusionNet(nn.Module):
    MODALITIES = ("t1","t1ce","t2","flair")

    def __init__(self, latent_dim=512, num_classes=5):
        super().__init__()
        self.encoders = nn.ModuleDict({
            m: Encoder3D(latent_dim) for m in self.MODALITIES
        })
        self.fusion = FusionHead(latent_dim, len(self.MODALITIES), num_classes)

    def encode(self, batch):
        latents = [self.encoders[m](batch[m]) for m in self.MODALITIES]
        return torch.cat(latents, dim=1)

    def forward(self, batch):
        return self.fusion(self.encode(batch))

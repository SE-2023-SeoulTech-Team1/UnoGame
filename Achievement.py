import pygame
import pickle
from resource_path import base_path
from Text import Text
from Colors import *
from datetime import datetime

class Achievement:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.completed = False
        self.file = file = base_path() + f"/data/achievement/{self.name}.pickle"
        self.icon = None
        self.completed_date = None

    def complete(self):
        self.completed = True
        self.completed_date = datetime.now()

    def __str__(self):
        return self.name + ": " + self.description + " (" + "complete" if self.completed else "incomplete" + ")"

    def save(self):
        with open(self.file, 'wb') as f:
            pickle.dump(self.completed, f, pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open(self.file, 'rb') as f:
            data = pickle.load(f)
            return data

    def draw(self, screen, y):
        Text(0.2, y, self.name, size=20).render(screen)
        Text(0.2, y + 0.03, self.description, size=15).render(screen)
        if self.completed:
            Text(0.7, y, "complete", color=GREEN, size=30).render(screen)
            Text(0.7, y + 0.03, self.completed_date.strftime("%Y-%m-%d %H:%M:%S"), color=GREEN, size=15).render(screen)
        else:
            Text(0.7, y, "incomplete", color=RED, size=30).render(screen)
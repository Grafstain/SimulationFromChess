import unittest
from io import StringIO
import sys

from Board import Board
from BoardConsoleRenderer import BoardConsoleRenderer
from Coordinates import Coordinates
from entities.Herbivore import Herbivore
from entities.Predator import Predator
from entities.Grass import Grass
from entities.Stone import Stone
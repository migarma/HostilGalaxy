#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: TurBoss
# Models: TurBoss

# Main

#import pdb

import sys
import os
import time

import json

from pprint import pprint

from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence

from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import CollideMask

from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32, VBase4
from panda3d.core import Point3, TransparencyAttrib,TextNode
from panda3d.core import Filename,AmbientLight,DirectionalLight, PointLight, Spotlight
from panda3d.core import PerspectiveLens, OrthographicLens
from panda3d.core import TransformState

from panda3d.core import WindowProperties
from panda3d.core import PStatClient

from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce, DiscEmitter
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup

from panda3d.ai import *

from joypad import Joypad

from gui import StartMenu

from collision import MouseCollision, ShipCollision
from ship import Ship
from bg import Background
from rock import Rock


class World(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        print("- init game")

        self.ship_control_type = 1 #0 keyboard, 1 mouse, 2 joystick

        self.accept('escape', self.do_exit)
        self.accept('r', self.do_reset)


        self.start_menu = StartMenu(self)

    def do_exit(self):

        self.cleanup()

        print("- end game")

        sys.exit(0)

    def cleanup(self):

        print("-- clean up")

        #self.joypad.clean()

    def do_reset(self):
        self.cleanup()
        self.setup()

    def setup(self):

        print("-- start level")



        self.init_particles()
        self.init_world()
        self.init_ship()
        self.init_lights()
        self.init_camera()

        self.mouse_collision = MouseCollision(self)

        #self.joypad = Joypad()

        # Tasks
        self.taskMgr.add(self.update, 'update')
        #self.taskMgr.add(self.joypad.update, 'updateJoypad')

    def init_world(self):

        print("-- init world")

        self.bg = Background(self)
        self.bg.draw()

        self.rock1 = Rock(self, 5, 5)
        self.rock2 = Rock(self, -5, 6)
        self.rock3 = Rock(self, -5, 3)

        self.taskMgr.add(self.bg.update, 'updateBackground')

    def init_ship(self):

        print("-- init ship")

        self.ship = Ship(self)
        self.ship_collision = ShipCollision(self.ship)

        self.ship.draw()
        self.taskMgr.add(self.ship.update, 'updateShip')

    def init_particles(self):

        base.enableParticles()

    def init_lights(self):

        print("-- init lights")

        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.1, 0.1, 0.1, 1))
        alightNP = render.attachNewNode(alight)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = render.attachNewNode(dlight)

        render.clearLight()
        render.setLight(alightNP)
        render.setLight(dlightNP)

    def init_camera(self):

        print("-- init camera")

        self.disableMouse()

        lens = OrthographicLens()
        lens.setFilmSize(20, 15)  # Or whatever is appropriate for your scene

        self.cam.node().setLens(lens)
        self.cam.setPos(0, -20, 0)
        self.cam.lookAt(0, 0, 0)

    def update(self, task):

        dt = globalClock.getDt()


        return task.cont


def main():

    props = WindowProperties( )

    props.setTitle('Hostil Galaxy')
    props.setCursorFilename(Filename.binaryFilename('cursor.ico'))
    props.setCursorHidden(False)
    props.setFullscreen(False)
    props.setSize(800, 600)

    game = World()

    game.win.setClearColor((0, 0, 0, 1))
    game.win.requestProperties(props)
    game.setFrameRateMeter(True)

    game.run()

if __name__ == "__main__": main()

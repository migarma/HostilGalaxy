#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: TurBoss
# Models: TurBoss

# Main

#import pdb

import sys, os, time
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

from panda3d.ai import *

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletSliderConstraint

from ship import Ship
from bg import Background
from rock import Rock


class World(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        print("init game")

        self.accept('escape', self.do_exit)
        self.accept('r', self.do_reset)

        self.bg = Background()
        self.rock = Rock(5)
        self.ship = Ship()

        self.setup()

    def do_exit(self):
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        print("clean up")

    def do_reset(self):
        self.cleanup()
        self.setup()

    def setup(self):
        print("start level")

        self.init_world()
        self.init_ship()
        self.init_lights()
        self.init_camera()

        # Task
        self.taskMgr.add(self.update, 'updateWorld')

    def init_world(self):
        print("init world")

        self.bg.draw()
        self.rock.draw()

    def init_ship(self):
        print("init ship")
        self.ship.draw()

    def init_lights(self):
        print("init lights")

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
        print("init camera")

        self.disableMouse()

        lens = OrthographicLens()
        lens.setFilmSize(20, 15)  # Or whatever is appropriate for your scene

        self.cam.node().setLens(lens)
        self.cam.setPos(0, -20, 0)
        self.cam.lookAt(0, 0, 0)


    def update(self, task):
        dt = globalClock.getDt()

        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()

            x = mpos.getX()
            y = mpos.getY()

            self.ship.model.setPos(x*10,0,y*10)


        self.rock.model.setZ(self.rock.model.getZ() - dt*2)

        print(self.rock.model.getZ())

        size = self.bg.get_size()
        self.bg.model.setPos(0, 5, (size[2]/2)-task.time*10)
        return task.cont



def main():
    props = WindowProperties( )

    props.setTitle('Hostil Galaxy')
    props.setCursorFilename(Filename.binaryFilename('cursor.ico'))
    props.setFullscreen(0)
    props.setSize(1024, 768)

    game = World()

    game.win.setClearColor((0, 0, 0, 1))
    game.win.requestProperties(props)
    game.setFrameRateMeter(True)

    game.run()

if __name__ == "__main__": main()
#!usr/bin/kivy

import kivy
kivy.require('1.9.0')

from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Line

import math
from math import sin, cos, pi

import time
from time import strftime


# allows you to switch between screens with a touch of a button rather than swiping
sidebar = '''
	SideBar
		name: 'sidebar'
		BoxLayout:
			orientation: 'vertical'
			size: (80, 480)
			pos: (720, 0)
			Button:
				text: 'Home'
				on_release: app.root.load_slide(app.root.slides[0])
			Button:
				text: 'Music'
				on_release: app.root.load_slide(app.root.slides[1])
			Button:
				text: 'Rearview'
				on_release: app.root.load_slide(app.root.slides[2])
'''

# home button 
##### DO I REALLY NEED A HOME BUTTON?? #####
##### MAYBE REPLACE WITH ANOTHER BUTTON?? #####
homebutton = '''
	HomeButton
		name: 'homebutton'
		BoxLayout:
			pos: (720, 0)
			size: (80, 80)
			Button:
				text: 'Home'
				## create home button image / find a cool looking home button image ##
'''

homescr = '''
HomeScreen
	name: 'homescreen'
	FloatLayout:
		size: (720, 480)
		pos: (0, 0)
		Speedometer:
			size_hint: (.6, .72)
			pos: (144, 0)
		ClockDisplay:
			size_hint: (0.6, 0.26)
			pos: (144, 360)
			font_size: 20
			halign: 'center'
		Battery:
			size_hint: (0.18, 0.55)
			pos: (0, 0)
		# Button:
		# 	text: 'est. range'
		# 	# replace with actual estimated range widget
		# 	size_hint: (0.18, 0.15)
		# 	pos: (0, 272.75)
'''

musicscr = '''
MusicScreen
	name: 'musicscreen'
	FloatLayout:
		size: (720, 480)
		pos: (0, 0)
		Button:
			text: 'musicscreen'
'''

rearscr = '''
RearviewScreen
	name: 'rearviewscreen'
	FloatLayout:
		size: (720, 480)
		pos: (0, 0)
		Button:
			text: 'rearviewscreen'
'''

# Screens and the different Widgets on them
class HomeScreen(Widget):
	pass


class ClockDisplay(Label):
	def __init__(self, **kwargs):
		super(ClockDisplay, self).__init__(**kwargs)
		
		Clock.schedule_interval(self.update, 1)

	def update(self, *args):
		self.text = time.strftime("%H:%M:%S\n%a, %b %d, %Y")


class Speedometer(Widget):
	def __init__(self, **kwargs):
		super(Speedometer, self).__init__(**kwargs)

		Clock.schedule_interval(self.update, 0.01)

	def update(self, *args):
		angleBetweenNumbers = 270 / 7
		centerX = 360
		centerY = 200
		numbersCenteredX = centerX - 50
		numbersCenteredY = centerY - 50
		speed = 0
		self.drawBase(centerX, centerY, numbersCenteredX, numbersCenteredY, angleBetweenNumbers)
		self.drawNeedle(centerX, centerY, speed, angleBetweenNumbers)

	# def on_touch_down(self, touch):
	# 	print("x = %d, y = %d", touch.x, touch.y)

	def drawBase(self, centerX, centerY, numbersCenteredX, numbersCenteredY, angleBetweenNumbers):
		radius = 175
		with self.canvas:
			Color(1, 1, 1)
			Line(width = 5, circle = (centerX, centerY, radius))
			# when drawing Speedometer numbers, actual center of circle is at (310, 150)

			for i in range(0, 8):
				SpeedometerNumber().draw(i, numbersCenteredX, numbersCenteredY, angleBetweenNumbers)

	def drawNeedle(self, centerX, centerY, speed, angleBetweenNumbers):
		with self.canvas:
			SpeedometerNeedle().draw(centerX, centerY, speed, angleBetweenNumbers)


class SpeedometerNumber(Label):
	def __init__(self, **kwargs):
		super(SpeedometerNumber, self).__init__(**kwargs)

	def draw(self, i, centerX, centerY, angleBetweenNumbers):
		self.text = str(i * 10)
		newRadius = 150
		x = centerX + newRadius * math.cos(math.radians(-135 - (i * angleBetweenNumbers)))
		y = centerY + newRadius * math.sin(math.radians(-135 - (i * angleBetweenNumbers)))
		self.pos = (x, y)
		self.font_size = 20
		self.color = (1, 1, 1)


class SpeedometerNeedle(Widget):
	def __init__(self, **kwargs):
		super(SpeedometerNeedle, self).__init__(**kwargs)

	def draw(self, centerX, centerY, speed, angleBetweenNumbers):
		lengthOfNeedle = 140
		endX = centerX + lengthOfNeedle * math.cos(math.radians(-135 - (speed / 10 * angleBetweenNumbers)))
		endY = centerY + lengthOfNeedle * math.sin(math.radians(-135 - (speed / 10 * angleBetweenNumbers)))
		
		Color(1, 0, 0, 0.5, mode = 'rgba')
		Line(width = 2, points = (centerX, centerY, endX, endY))


class Battery(Widget):
	def __init__(self, *kwargs):
		super(BatteryIcon, self).__init__(**kwargs)

	def draw(self):
		pass


class MusicScreen(Widget):
	pass


class RearviewScreen(Widget):
	pass


# Universal companents and widgets across all screens
class SideBar(Widget):
	pass


class HomeButton(Widget):
	pass


class TouchScreenApp(App):
	def build(self, **kwargs):
		# set the window size
		Window.size = (800, 480)

		# setup the Carousel such that we can swipe between screens
		carousel = Carousel(direction='right')

		# add the homescreen widget to the carousel with the sidebar
		homescreen = Builder.load_string(homescr + sidebar)
		carousel.add_widget(homescreen)

		# add the musicscreen widget to the carousel with the sidebar
		musicscreen = Builder.load_string(musicscr + sidebar)
		carousel.add_widget(musicscreen)
		
		# add the rearview camera screen widget to the carousel with the sidebar
		rearviewscreen = Builder.load_string(rearscr + sidebar)
		carousel.add_widget(rearviewscreen)

		return carousel

if __name__ == '__main__':
	TouchScreenApp().run()
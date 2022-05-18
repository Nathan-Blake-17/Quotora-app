from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')

class LoginScreen(Screen):
	def sign_up(self):
		self.manager.current = "sign_up_screen"

	def forgot_password(self):
		self.manager.current = "forgot_password_screen"

	def login(self, uname, pword):
		with open("users.json") as file:
			users = json.load(file)
		detail = [el for el in users['user_details'] if uname in el['username']]
		uval = [d['username'] for d in detail]
		pval = [d['password'] for d in detail]
		print(uval[0], pval[0])

		if uname == uval[0] and pword == pval[0]:
			self.manager.current = 'login_screen_success'
		else:
			self.ids.login_wrong.text = "An incorrect username or password has been entered please try again!"

class RootWidget(ScreenManager):
	pass

class SignUpScreen(Screen):
	def add_user(self, uname, pword):
		user_dict = {"user_details": []}
		user = user_dict["user_details"]
		user.append({"username": uname, "password": pword})

		with open("users.json", 'w') as file:
			json_file = json.dump(user_dict, file)
		self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
	def go_to_login(self):

		self.manager.transition.direction = "down"
		self.manager.current = "login_screen"

class ForgotPasswordScreen(Screen):
	def show_password(self, uname):
		with open("users.json", 'r') as file:
			values = json.load(file)

		detail = [el for el in values['user_details'] if uname in el['username']]
		print(detail)
		self.ids.see_pword.text = str(detail)

	def go_to_login(self):

		self.manager.transition.direction = "down"
		self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
	def log_out(self):
		self.manager.transition.direction = "right"
		self.manager.current = "login_screen"

	def get_quote(self, quote):
		# print(quote)
		quote = quote.lower()
		available_quotes = glob.glob("quotes/*txt")
		print(available_quotes)

		available_quotes = [Path(filename).stem for filename in available_quotes]
		print(available_quotes)

		if quote in available_quotes:
			with open(f"quotes/{quote}.txt") as file:
				quotes = file.readlines()
			print(quotes)
			self.ids.quote.text = random.choice(quotes)
		else:
			self.ids.quote.text = "Sorry it appears we do not have any quotes by: " + quote + ". Please try again with the above mentioned."

class ImageButton(ButtonBehavior, HoverBehavior, Image):
	pass

class MainApp(App):
	def build(self):
		return RootWidget()

if __name__ =="__main__":
	MainApp().run()

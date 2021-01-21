from flask import Flask, session, jsonify, request, redirect, render_template
import requests
app = Flask(__name__)

# Setup

app.secret_key = "Helloww-cats!!"

config = {
	"client_id": "801699906221768744",
	"client_secret": "HqNPNzKuOenr77s5Hkg_U95LnHcqJMRU",
	"callback_url": "https://discord-login.hansputera.repl.co/auth/callback"
}

# Discord config

discordConfig = {
	"api": "https://discord.com/api/v6"
}


# HTML
@app.route("/")
def home():
	session_token = session.get("access_token", None)
	if session_token != None:
		response = requests.get(f"{discordConfig['api']}/users/@me", headers={"Authorization": f"Bearer {session_token}"})
		return render_template("index.html", data={"logged": True, "responseData": response })
	else:
		return render_template("index.html", data={"logged": False })

# Login
@app.route("/auth/login")
def loginAuth():
	if session.get('access_token', None) == None:
		return redirect(f"https://discord.com/api/oauth2/authorize?client_id={config['client_id']}&redirect_uri={config['callback_url']}&response_type=code&scope=identify")
	else:
		return redirect("/")

# Callback handle
@app.route("/auth/callback")
def callbackAuth():
	args = request.args
	
	# Code
	code = args.get('code', None)
	if code == None:
		return jsonify({"success": False, "message": "Invalid code"})
	else:
		payload = {
			"client_id": config['client_id'],
			"client_secret": config['client_secret'],
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": config['callback_url'],
			"scope": "identify"
		}

		headers = {
			"Content-Type": "application/x-www-form-urlencoded"
		}
		response = requests.post(f"{discordConfig['api']}/oauth2/token", headers=headers, data=payload)

		access_token = response.json()['access_token']
		session['access_token'] = access_token

		return redirect("/")

# Auth information
@app.route("/auth/info")
def authInfo():
	access_token = session.get('access_token', None)
	if access_token == None:
		return jsonify({"success": False, "message": "Expire session"})
	else:
		headers = {
			"Authorization": f"Bearer {access_token}"
		}
		response = requests.get(f"{discordConfig['api']}/users/@me", headers=headers)
		return jsonify(response.json())

# Logout
@app.route("/auth/logout")
def logout():
	sessionToken = session.get("access_token", None)
	if sessionToken == None:
		return jsonify({"success": False, "message": "You never login to the website"})
	else:
		session.clear()
		return jsonify({"success": True, "message": "Logout!"})
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=2392)
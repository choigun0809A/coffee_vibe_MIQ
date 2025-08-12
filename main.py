from flask import Flask, render_template, request, redirect, Response, session, send_from_directory


miq = {
    "linguistic": [
        "Do you enjoy reading books, stories, or articles?",
        "Do you find it easy to explain your thoughts in writing?",
        "Do you often notice grammar mistakes in other people's speech or writing?",
        "Do you enjoy playing word games like Scrabble or crosswords?",
        "Do you enjoy writing stories, poems, or essays?",
        "Can you learn new vocabulary easily?",
        "Do you enjoy participating in debates or discussions?"
    ],
    "logical_mathematical": [
        "Do you enjoy solving puzzles and brainteasers?",
        "Are you good at understanding abstract concepts?",
        "Do you enjoy experimenting to find how things work?",
        "Do you see patterns easily in numbers or shapes?",
        "Do you find math problems interesting?",
        "Do you like planning and organizing information logically?",
        "Can you solve problems without needing step-by-step instructions?"
    ],
    "spatial": [
        "Do you enjoy drawing, painting, or visual arts?",
        "Do you often imagine things in your head in detail?",
        "Can you easily read maps or navigate unfamiliar places?",
        "Do you think in pictures rather than words?",
        "Do you enjoy building models or 3D objects?",
        "Are you good at visualizing how objects fit or work together?",
        "Do you enjoy games that involve designing or constructing things?"
    ],
    "bodily_kinesthetic": [
        "Do you learn better by doing than by watching or listening?",
        "Are you good at sports or physical activities?",
        "Do you often use gestures or body movement while talking?",
        "Do you enjoy working with your hands to build or fix things?",
        "Do you have good coordination and motor skills?",
        "Do you find it hard to sit still for long periods?",
        "Do you prefer acting something out over describing it?"
    ],
    "musical": [
        "Do you enjoy listening to or playing music regularly?",
        "Can you easily remember melodies or rhythms?",
        "Do you notice when music is out of tune?",
        "Do you often tap your fingers or feet to a beat?",
        "Do you enjoy creating or composing music?",
        "Do you associate certain memories or feelings with specific songs?",
        "Do you find it easy to learn things if they are set to music?"
    ],
    "interpersonal": [
        "Do you enjoy working in groups or teams?",
        "Are you good at understanding how others feel?",
        "Do friends often come to you for advice?",
        "Do you prefer studying or working with others rather than alone?",
        "Do you find it easy to start conversations with strangers?",
        "Do you enjoy helping others solve problems?",
        "Are you skilled at persuading or motivating others?"
    ],
    "intrapersonal": [
        "Do you spend time reflecting on your thoughts and feelings?",
        "Do you set personal goals and follow through with them?",
        "Do you understand your strengths and weaknesses well?",
        "Do you enjoy working or studying alone?",
        "Are you aware of what motivates or discourages you?",
        "Do you often think about the meaning or purpose of life?",
        "Do you trust your intuition when making decisions?"
    ],
    "naturalistic": [
        "Do you enjoy being in nature or exploring outdoors?",
        "Can you easily recognize types of plants or animals?",
        "Do you care deeply about the environment?",
        "Do you enjoy organizing or categorizing natural things?",
        "Are you good at identifying patterns in nature?",
        "Do you prefer natural settings over urban ones?",
        "Do you enjoy caring for pets, plants, or gardens?"
    ]
}
keys = list(miq.keys())

scores = {}


app = Flask(__name__)

@app.route("/", methods =['GET', 'POST'])
def MIQ():

    if request.method == "POST":
        for key in keys:
            
            max_score = len(miq[key])*2
            score = max_score
            max_score *= 2
            
            for num in range(len(miq[key])):
                ans = request.form.get(key + str(num))

                if ans != None:
                    ans = int(ans)
                    score += ans 
            percentage = (score / max_score) * 100
            scores[key] = round(percentage, 3)
        
        for key in keys:
            print(f"{key} intelligence: {scores[key]}%")
        return redirect("/results")
                

    String = ""
    Num = 0
    for key in keys:
        questions = miq[key]
        
        for pos, question in enumerate(questions):
            Num += 1           
            string = f"<div class=question><h1>{str(Num)+ ". " + question}</h1>"
            string += "<div class = 'answers'>"
            for num in range(-2, 3, 1):
                string += f"<label class='checkbox-container'><input type='radio' name='{key + str(pos)}' value='{num}'><span class='checkbox-placeholder'>{num}</span></label>"
            
            string += "</div></div>"
            String += string
    
    return render_template("main.html", innput=String)


@app.route("/results")
def results():
    results = ""
    for key in keys:
        result = f"<div class='result-box'>{key} intelligence: {scores[key]}%</div>"
        results += result

    return render_template("results.html", result = results)



@app.route('/google9f8b8aeb83c75bc6.html', methods=['GET'])
def google():
    return render_template("google9f8b8aeb83c75bc6.html")

@app.route('/sitemap.xml')
def sitemap():
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

  <url>
    <loc>https://choistests.onrender.com/</loc>
    <lastmod>2025-08-05</lastmod>
    <priority>1.0</priority>
  </url>


</urlset>
'''
    return Response(xml, mimetype='application/xml')


@app.route("/robots.txt")
def robots():
    robots_txt = '''User-agent: *
Disallow:

Sitemap: https://choistests.onrender.com/sitemap.xml
'''
    return Response(robots_txt, mimetype='text/plain')



app.secret_key = 'mfchoi'



players = {}
roles = ["killer", "medic", "silencer", "detective", "jester"]
evil_roles = ["killer", "silencer", "jester"]
message = ""


@app.route('/mafia', methods = ['GET', 'POST'])
def mafia():
    if request.method == "POST":
        name = request.form["text-box"]

        if name in players.keys() or name == "":
            return render_template("login2.html")
        else:
            players[name] = {"isdead":False, "issilent": False, "role": "Civilian"}
            session["player"] = name

            print(f"player: {name} has joined the game.")
            return redirect("/mafia/lobby")
        
    return render_template("login.html")

@app.route("/mafia/lobby", methods = ['GET', 'POST'])
def lobby():
    if session["player"] not in players:
        return redirect("/mafia")
    names = list(players.keys())
    step_1 = [f"<li class = '{"alive" if not players[name]["isdead"] else "dead"}' name = '{"notsilent" if not players[name]["issilent"] else "issilent"}'>{name}</li>" for pos, name in enumerate(names)]
    print(players)
    final = "<ul class='players'>" + "".join(step_1) + "</ul>"

    global message
    print(message)
    print(session["player"])
    if players[session["player"]]["role"] == "detective":
        return render_template("players.html", final=final, role = players[session["player"]]["role"] , message = message)
    else:
        return render_template("players.html", final=final, role = players[session["player"]]["role"], message = "")


@app.route("/mafia/roles")
def _roles_():
    names = list(players.keys())
    step_1 = [f"<li class = '{players[name]["role"]}'>{f"player {name}'s role is {players[name]["role"]}"}</li>" for pos, name in enumerate(names)]
    print(players)
    final = "<ul class='players'>" + "".join(step_1) + "</ul>"
    
    return render_template("players_roles.html", final=final)

import random as rand
@app.route("/mafia/admin", methods=['GET', 'POST'])
def admin():
    global players, roles, message
    names = list(players.keys())

    if request.method == "POST":

        
        
        type_of_form = request.form.get("clicked")
        for name in names:
            players[name]["issilent"]=False

        if type_of_form == "start":
            for name in names:
                players[name] = {"isdead": False, "issilent": False, "role": "Civilian"}
            for role in roles:
                name = rand.choice(names)
                players[name]["role"] = role
        if type_of_form == "kill":
            try:
                name = names[int(request.form.get("kill_pos"))-1]
                players[name]["isdead"] = True
            except:
                pass
        if type_of_form == "revive":
            try:
                name = names[int(request.form.get("revive_pos"))-1]
                players[name]["isdead"] = False
            except:
                pass
        if type_of_form == "remove":
            try:
                name = names[int(request.form.get("remove_pos"))-1]
                players.pop(name)
            except:
                pass
        if type_of_form == "silence":
            try:
                name = names[int(request.form.get("silence_pos"))-1]
                players[name]["issilent"] = True
            except:
                pass
        if type_of_form == "guess":
            try:
                name = names[int(request.form.get("guess_pos"))-1]
                if players[name]["role"] in evil_roles:
                    message += f"<p>player {name} is evil</p>"
                else:
                    message += f"<p>player {name} is good</p>"
            except:
                pass

    return render_template("admin.html")





@app.route("/home")
def home():
    return render_template("home.html")



@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

input_types_and_funcs = {
    "usd_to_eur": lambda x: float(x) * 0.92,        
    "eur_to_usd": lambda x: float(x) * 1.09,
    "usd_to_jpy": lambda x: float(x) * 155.0,
    "usd_to_gbp": lambda x: float(x) * 0.78,
    "mb_to_kb": lambda x: float(x) * 1024,
    "gb_to_mb": lambda x: float(x) * 1024,
    "bit_to_byte": lambda x: float(x) / 8,
    "tbsp_to_tsp": lambda x: float(x) * 3,
    "cup_to_oz": lambda x: float(x) * 8,
    "oz_to_gram": lambda x: float(x) * 28.3495,
    "hp_to_kw": lambda x: float(x) * 0.7457,
    "psi_to_bar": lambda x: float(x) * 0.0689476,
    "mph_to_kph": lambda x: float(x) * 1.60934
}

@app.route("/converter", methods=['GET', 'POST'])
def converter():
    if request.method == "POST":
        input_type = request.form.get("input_type")
        returning_str = ""

        try:
            input_value = int(request.form.get("input_value"))
            global input_types_and_funcs
            returning_str = f"<p class = 'plus'>{str(input_types_and_funcs[input_type](input_value))}</p>"
            
        except:
            returning_str = f"<p class = 'neg'>Invalid input value. Please enter a number.</p>"

        
        
        return render_template("converter.html", output_value=returning_str)

if __name__ == "__main__":
    app.run()





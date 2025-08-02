from flask import Flask, render_template, request, redirect, Response


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

@app.route("/", methods = ["GET", "POST"])
def home():

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
    
    return render_template("google9f8b8aeb83c75bc6.html", innput=String)


@app.route("/results")
def results():
    results = ""
    for key in keys:
        result = f"<div class='result-box'>{key} intelligence: {scores[key]}%</div>"
        results += result

    return render_template("results.html", result = results)

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://choistests.onrender.com</loc>
    <lastmod>2025-08-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>'''
    return Response(xml, mimetype='application/xml')


if __name__ == "__main__":
    app.run(debug=True)


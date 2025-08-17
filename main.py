from flask import Flask, render_template, request, redirect, Response, session, send_from_directory, send_file
import static.tools as tools

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
keysc = list(miq.keys())

scoresc = {}

scoresd = {}

miq_d = {
    "Байгалийн": [
        "Би аливаа зүйлийг нийтлэг шинжээр нь ерөнхийлөн ангилах дуртай",
        "Экологийн (байгаль орчны) асуудал миний хувьд чухал",
        "Би явган эсвэл майхантай аялах маш дуртай",
        "Ургамал тарьж арчлах, хүлэмжинд ажиллах дуртай",
        "Би байгалийн цэвэр, бүрэн бүтэн байдлыг хадгалах, хамгаалах чухал гэж боддог",
        "Юмсыг эрэмблэн, системчлэх нь надад ойлгомжтой байдаг.",
        "Миний амьдралд амьтад маш чухал байр суурийг эзэлдэг",
        "Би дахин боловсруулах үйл ажиллагааг маш чухал гэж боддог",
        "Би биологи, ургамал болон амьтан судлах маш дуртай",
        "Би гэрээс гадуур цагийг өнгөрүүлэх дуртай"
    ],
    "Хөгжмийн": [
        "Би юмсыг хэв маяг, зүй тогтлыг таньж, ойлгохдоо сайн",
        "Би дуу чимээг анхаарч, анзаарамтгай.",
        "Би хөгжмийн хэмнэлээр хөдлөхдөө сайн.",
        "Надад хөгжмийн зэмсгээр тоглох үргэлж сонирхолтой байсан",
        "Яруу найргийн хөг хэмнэл миний сэтгэлийг татдаг",
        "Би юмсийг толгой сүүл холбож санадаг.",
        "Би радио, телевиз үзэж байхдаа төвлөрч чаддаггүй",
        "Би олон төрлийн хөгжимд дуртай",
        "Жүжигээс илүү мюзикл нь сонирхолтой",
        "Би дууны үгсийг сайн мэддэг."
    ],
    "Логик": [
        "Би эд зүйлсээ эмх цэгцтэй байлгадаг",
        "Аливааг алхам алхамаар хийх нь маш чухал",
        "Аливаа асуудлыг шийдлийг олох нь надад тийм ч хэцүү биш",
        "Эмх замбараагүй хүмүүс миний бухимдлыг төрүүлдэг",
        "Би цээжээр тооцоолон бодохдоо сайн",
        "Сэтгэхүй, логик шаардсан тоглоом надад хөгжилтэй байдаг.",
        "Би бүх зүйлийг тодорхой болгохоос нааш ямар ч ажлыг эхлүүлдэг",
        "Зохион байгуулалт бол миний амжилтын үндэс",
        "Компютерийн хүснэгт эсвэл мэдээллийн сан дээр ажиллах нь надад урамтай байдаг",
        "Бүх зүйлс маш ойлгомжтой байх үед л би сэтгэл хангалуун байдаг, тийм биш бол сэтгэл дундуур"
    ],
    "Экстенциал": [
        "Аливаа том зүйлд миний үүрэг юу гэдгийг олж харах нь чухал",
        "Би амьдралын тухай яриа өрнүүлэх дуртай",
        "Шашин шүтлэг бол миний хувьд чухал",
        "Би урлагийн шилдэг бүтээлүүдийг үзэх дуртай",
        "Тайван амрах, бясалгал хийх нь амьдралд хэрэгтэй.",
        "Би байгалийн үзэсгэлэнт газруудаар аялах дуртай",
        "Би эртний болон орчин үеийн философичдын номыг унших дуртай",
        "Би үнэ цэнийг нь ойлгочихвол шинэ зүйлийг амархан сурдаг.",
        "Би энэ ертөнц дээр өөр амьдрал байдаг болов уу гэж боддог.",
        "Түүх болон эртний соёлыг судлах нь надад хэтийн зорилгоо тодорхойлоход тусалдаг"
    ],
    "Харилцааны": [
        "Би бусадтай ярилцах, хамтрах, харилцах замаар суралцдаг.",
        "Би олуулаа байх, олуулаа хамтрах дуртай.",
        "Багаараа ажиллах нь надад илүү үр дүнтэй санагддаг",
        "Чатын группуудэд байх надад сонирхолтой байдаг.",
        "Улс төрд оролцох нь чухал",
        "Зурагт болон радионы ярилцлагын шоунууд сонирхолтой.",
        "Би бол багийн тоглогч.",
        "Би ганцаараа ажиллах дургүй.",
        "Дугуйлан болон хичээлээс гадуурх үйл ажиллагаанууд хөгжилтэй",
        "Би нийгмийн асуудал, шалтгаанд анхаарлаа хандуулдаг"
    ],
    "Хөдөлгөөний": [
        "Гараараа юм хийх дуртай",
        "Хөдөлгөөнгүй удаан суух нь надад хэцүү байдаг",
        "Надад явган алхах, багийн спорт, агаарт байх таалагддаг.",
        "Би аман бусаар (дохио зангаа гэх мэт) харилцахыг илүүд үздэг.",
        "Бие эрүүл байх нь оюун ухаан эрүүл байхад чухал.",
        "Урлаг, гар урлал хийх нь хөгжилтэй, зугаатай байдаг.",
        "Бүжгээр илэрхийлэх нь гоо сайхан.",
        "Би багаж хэрэгсэлтэй ажиллах дуртай",
        "Би идэвхитэй амьдралын хэв маягтай",
        "Би хийж үзэж суралцдаг."
    ],
    "Үгийн": [
        "Би бүх төрлийн материалуудыг унших дуртай",
        "Тэмдэглэл хөтлөх нь надад ойлгох, санахад тусалдаг.",
        "Би найзуудтайгаа тогтмол харилцаатай байдаг.",
        "Өөрийн санаа бодлоо бусдад илэрхийлэх хялбар байдаг.",
        "Би өдрийн тэмдэглэл хөтөлдөг",
        "Үгийн сүлжээ, эвлүүлдэг тоглоомнууд хөгжилтэй.",
        "Би бичиж байхдаа аз жаргалтай байдаг.",
        "Би үгээр нааддаг тоглоомонд дуртай.",
        "Гадаад хэл надад сонирхолтой санагддаг.",
        "Би итгэл, мэтгэлцээнд оролцох дуртай"
    ],
    "Өөртөө чиглэсэн": [
        "Би өөрийн ёс суртахууны итгэл үнэмшилээ сайн мэддэг.",
        "Сэтгэлийг минь хөдөлгөсөн зүйлийг би хамгийн сайн сурдаг.",
        "Шударга байдал бол надад чухал зүйл.",
        "Миний хандлага суралцах аргад минь нөлөөлдөг",
        "Нийгмийн шударга ёсны асуудал надад ч бас хамаатай.",
        "Ганцаараа ажиллах нь багаараа ажиллахтай ижил үр бүтээлтэй байдаг",
        "Аливаа зүйлийг хийхээсээ өмнө яагаад хийх ёстойгоо мэдэх хэрэгтэй.",
        "Би итгэсэн зүйлдээ 100% хүчин чармайлт гаргадаг.",
        "Би бусдын төлөө гэсэн үйл хэрэгт оролцохдоо дуртай байдаг.",
        "Би буруу зүйлсийг залруулахын төлөө тэмцэх, оролцохдоо бэлэн байдаг"
    ],
    "Дүрслэх": [
        "Би оюун санаандаа төсөөлөн бодож чаддаг",
        "Өрөөгөө өөрчлөх нь надад таалагддаг",
        "Би төрөл бүрийн медиа хэрэгсэл ашиглан бүтээл хийх дуртай",
        "Би зураг, дүрслэлээр илэрхийлсэн зүйлсийг илүү сайн санадаг.",
        "Би үзүүлбэрт урлагт маш их дуртай",
        "Экселийн хүснэгт нь график, диаграм, хүснэгт ашиглахад үнэхээр гайхалтай.",
        "Би хэмжээст эвлүүлдэг тоглоом тоглох маш сонирхолтой.",
        "Хөгжмийн видео үзэх намайг сэргээж, урам зориг өгдөг",
        "Би оюуны зураглалаар юмыг санаж чадна",
        "Би газрын зураг, атлас, зураг төсөл уншихдаа сайн"
    ]
}


keysd = list(miq_d.keys())



app = Flask(__name__)


@app.route("/", methods =['GET', 'POST'])
def MIQ_by_choi():

    if request.method == "POST":
        questions: dict[str, dict[str, int]] = {}

        for key in keysc:
            questions[key] = {}
            max_score = len(miq[key])*2
            score = max_score
            max_score *= 2
            
            for num in range(len(miq[key])):
                ans = request.form.get(key + str(num))
                

                if ans != None:
                    ans = int(ans)
                    score += ans 
                    questions[key][miq[key][num]] = ans
                else:
                    questions[key][miq[key][num]] = 0
            percentage = (score / max_score) * 100
            scoresc[key] = round(percentage, 3)

        tools.upload_c(questions, scoresc)
        # for key in keysc:
        #     print(f"{key} intelligence: {scoresc[key]}%")
        return redirect("/resultsc")


                

    String = ""
    Num = 0
    for key in keysc:
        questions = miq[key]
        
        for pos, question in enumerate(questions):
            Num += 1           
            string = f"<div class=question><h1>{str(Num)+ ". " + question}</h1>"
            string += "<div class = 'answers'>"
            for num in range(-2, 3, 1):
                string += f"<label class='checkbox-container'><input type='radio' name='{key + str(pos)}' value='{num}'><span class='checkbox-placeholder'>{num}</span></label>"
            
            string += "</div></div>"
            String += string
    
    return render_template("MIQ_by_Choi.html", innput=String)


@app.route("/resultsc")
def results():
    results = ""
    for key in keysc:
        result = f"<div class='result-box'>{key} intelligence: {scoresc[key]}%</div>"
        results += result

    return render_template("results.html", result = results)


@app.route("/dmiq", methods =['GET', 'POST'])
def MIQ_by_D():

    if request.method == "POST":
        questions: dict[str, dict[str, int]] = {}

        for key in keysd:
            questions[key] = {}
            score = 0
            max_score = 10
            
            for num in range(len(miq_d[key])):
                ans = request.form.get(key + str(num))
                

                if ans != None:
                    ans = int(ans)
                    score += ans 
                    questions[key][miq_d[key][num]] = ans
                else:
                    questions[key][miq_d[key][num]] = 0

            percentage = (score / max_score) * 100
            scoresd[key] = round(percentage, 3)

        tools.upload_d(questions, scoresd)
        # for key in keysd:
        #     print(f"{mid[key]} Ухаан: {scores[key]}%")
        return redirect("/resultsd")


                

    String = ""
    Num = 0
    for key in keysd:
        questions = miq_d[key]
        
        for pos, question in enumerate(questions):
            Num += 1           
            string = f"<div class=question><h1>{str(Num)+ ". " + question}</h1>"
            string += "<div class = 'answers'>"
            
            for i in range(0, 2):
                string += f"<label class='checkbox-container'><input type='radio' name='{key + str(pos)}' value='{i}'><span class='checkbox-placeholder'>{i}</span></label>"
            
            string += "</div></div>"
            String += string
    
    return render_template("MIQ_by_D.html", innput=String)

@app.route("/resultsd")
def resultsd():
    results = ""
    for key in keysd:
        result = f"<div class='result-box'>{key} Ухаан: {scoresd[key]}%</div>"
        results += result

    return render_template("results.html", result = results)


@app.route("/download1475")
def download():
    return send_file(
        tools.get_users_c(),
        as_attachment=True,
        download_name="output.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
@app.route("/download1476")
def download2():
    return send_file(
        tools.get_users_d(),
        as_attachment=True,
        download_name="output.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')



if __name__ == "__main__":
    app.run()





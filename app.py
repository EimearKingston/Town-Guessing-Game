from flask import Flask, render_template, request, redirect, url_for, g, session, make_response
from database import get_db, close_db
from flask_session import Session
from forms import CountyForm, SignForm, LoginForm, CommentForm
from sqlite3 import IntegrityError
#from functools import partial 
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
app=Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"]="this-is-my-secret-key"
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

@app.before_request
def load_logged_in_user():
    g.user=session.get("username", None) #g stands for global --> which means it can be used ANYWHERE in my code - Python, Jinja etc. but can't use the 'g' in the CSS
    #Watch video to see what this means but definitely use in CA
    #If CA has a "super user" who can change the database then create a default username and password for the user and comment it at the top of app.py for CA

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: 
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view
@app.route("/", methods=["GET", "POST"])
def index():
    
    return render_template("index.html", title="Guess the County!")

@app.route("/county", methods=["GET", "POST"])
@login_required
def county():
    form=CountyForm()
    if "valid" in session:
        session.pop("valid")
    # if "town" in session:
    #session.pop("town")
    c_county=""
    message=""
    equal=""   
    comments=None
    username=g.user
    db=get_db()  
    
    town=""
    #if request.method=="GET":
        
    row=db.execute('''SELECT town FROM counties
                        ORDER BY RANDOM() LIMIT 1''').fetchone()

    town = row["town"]
    if "town" not in session:
        session["town"]=town
    comments=db.execute('''SELECT * FROM comments;''').fetchall()
    count_comments=db.execute('''SELECT COUNT(*) FROM comments;''').fetchall()
    total=0
    for comment in comments:
        total+=1
    score=db.execute('''SELECT point FROM points
                                WHERE username=?
                                ORDER BY point DESC LIMIT 1;''', (username,)).fetchone()
    if score is not None:
        high_score=score["point"]
    else:
        high_score=0
    # print(town)
    print("town:"+session["town"])
    if form.validate_on_submit():
        if "town" in session:
            username=g.user
            
            
            if "streak" not in session:
                session["streak"]=0
            if "streak" in session:
                session["streak"]+=1
            streak=session["streak"]
            print("town:"+ session["town"]) 
            c_county=form.c_county.data
            print("answer:" + c_county)
            db=get_db()
            equal=db.execute('''SELECT * FROM counties
                                WHERE town=?;''', (session["town"],)).fetchone()
            valid=equal["county"]
            if "valid" not in session:
                session["valid"]=valid
            print("county:" + valid)
            
            if valid==c_county: 
                print("valid")
                session.pop("town")
                session.pop("valid")
                if "town" not in session:
                    row=db.execute('''SELECT town FROM counties
                        ORDER BY RANDOM() LIMIT 1''').fetchone()

                    town = row["town"]
                    session["town"]=town
                
                form.streak.data=streak
                
                if "town" in session:
                    row=db.execute('''SELECT town FROM counties
                        ORDER BY RANDOM() LIMIT 1''').fetchone()

                    town = row["town"]
                    session["town"]=town
                    
                return render_template("/county.html", form=form, town=session["town"], title="Guess the county", comments=comments, total=total, high_score=high_score)

                #return render_template("/county.html", form=form, town=town, streak=streak, message="Correct!", title="Guess the county")
            else:
                session.pop("town")
                if "town" not in session:
                    row=db.execute('''SELECT town FROM counties
                        ORDER BY RANDOM() LIMIT 1''').fetchone()

                    town = row["town"]
                    session["town"]=town
                
                form.streak.data=streak
                streak=form.streak.data-1
                clash=db.execute('''SELECT username FROM points
                                        WHERE username=?;''', (username,)).fetchone()
                if clash is not None:

                    current_score=db.execute('''SELECT point FROM points 
                                                WHERE username=?;''', (username,)).fetchone()
                    c_score=current_score["point"]
                    if streak>c_score:
                        db.execute('''UPDATE points
                                        SET point=?
                                            WHERE username=?;''', (streak, username))
                        db.commit()
                else:
                    db.execute('''INSERT INTO points(username, point)
                                VALUES (?, ?);''', (username, streak))
                    db.commit()
                session.pop("streak")
                session["streak"]=0
                return redirect(url_for("play_again"))
                #return render_template("/county.html", town=town, form=None)
        
    return render_template("/county.html", form=form, town=session["town"], title="Guess the county", comments=comments, total=total, high_score=high_score)
@app.route("/county_no_save", methods=["GET", "POST"])
def county_no_save():
    form=CountyForm()
    if "valid" in session:
        session.pop("valid")
    # if "town" in session:
    #session.pop("town")
    c_county=""
    message=""
    equal=""   
    comments=None
    username=g.user
    db=get_db()  
    
    town=""
    #if request.method=="GET":
        
    row=db.execute('''SELECT town FROM counties
                        ORDER BY RANDOM() LIMIT 1''').fetchone()

    town = row["town"]
    if "town" not in session:
        session["town"]=town
    comments=db.execute('''SELECT * FROM comments;''').fetchall()
    count_comments=db.execute('''SELECT COUNT(*) FROM comments;''').fetchall()
    total=0
    for comment in comments:
        total+=1
    print("town:"+session["town"])
    if form.validate_on_submit():
        if "town" in session:
           
            
            
            if "streak" not in session:
                session["streak"]=0
            if "streak" in session:
                session["streak"]+=1
            streak=session["streak"]
            print("town:"+ session["town"]) 
            c_county=form.c_county.data
            print("answer:" + c_county)
            db=get_db()
            equal=db.execute('''SELECT * FROM counties
                                WHERE town=?;''', (session["town"],)).fetchone()
            valid=equal["county"]
            if "valid" not in session:
                session["valid"]=valid
            print("county:" + valid)
            
            if valid==c_county: 
                print("valid")
                session.pop("town")
                session.pop("valid")
                if "town" not in session:
                    row=db.execute('''SELECT town FROM counties
                        ORDER BY RANDOM() LIMIT 1''').fetchone()

                    town = row["town"]
                    session["town"]=town
                
                form.streak.data=streak
                
                if "town" in session:
                    row=db.execute('''SELECT town FROM counties
                        ORDER BY RANDOM() LIMIT 1''').fetchone()

                    town = row["town"]
                    session["town"]=town
                    
                return render_template("/county_no_save.html", form=form, town=session["town"], title="Guess the county", comments=comments, total=total)

                #return render_template("/county.html", form=form, town=town, streak=streak, message="Correct!", title="Guess the county")
            else:
                session.pop("town")
                if "town" not in session:
                    row=db.execute('''SELECT town FROM counties
                        ORDER BY RANDOM() LIMIT 1''').fetchone()

                    town = row["town"]
                    session["town"]=town
                
               
                
                session.pop("streak")
                session["streak"]=0
                return redirect(url_for("play_again_no_save"))
                #return render_template("/county.html", town=town, form=None)
        
    return render_template("/county_no_save.html", form=form, town=session["town"], title="Guess the county", comments=comments, total=total)
@app.route("/play_again_no_save", methods=["GET", "POST"])
def play_again_no_save():
    county=session.get("valid", None)
    
    return render_template("/play_again_no_save.html", title=("Correct answer was: " + county))

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        password_again=form.password_again.data 
        db=get_db()
        username_clash=db.execute('''SELECT * FROM users
                                            WHERE username=?;''', (username,)).fetchone()
        if username_clash is not None: 
            form.username.errors.append("User is already taken")
        else:
            db.execute('''INSERT INTO users(username, password)
                      VALUES(?,?)''', (username, generate_password_hash(password))) #no .fetchall() and no variable because you are inserting into the database
            db.commit()
            return redirect(url_for('login'))
            # session.clear()
            # session["username"]=username
            # next_page=request.args.get("county")
            # if not next_page:
            #     next_page=url_for("county")
            # return redirect(next_page)
            #return redirect(url_for("county"))
            #form.username.errors.append("Username is already taken")
    return render_template("/sign_up.html", form=form, title="Sign-up")

@app.route("/login", methods=["GET", "POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        db=get_db()
        valid=db.execute('''SELECT * FROM users
                            WHERE username=?;''', (username,)).fetchone()
        if valid is None:
            form.username.errors.append("Unknown Username!")
#            return render_template("/county.html", form=form, title="Guess the county")
        elif not check_password_hash(valid["password"], password):
            return render_template("/login.html", form=form, message="Incorrect Password!", title="Login")
        else:
            session.clear()
            session["username"]=username
            next_page=request.args.get("county")
            if not next_page:
                next_page=url_for("county")
            return redirect(next_page)
            
    return render_template("/login.html", form=form, title="Login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
@app.route("/play_again", methods=["GET", "POST"])
def play_again():
    county=session.get("valid", None)
    
    return render_template("/play_again.html", title=("Correct answer was: " + county))

@app.route("/comments", methods=["GET", "POST"])
@login_required
def comments():
    form=CommentForm()
    comments=None
    db=get_db()
    comments=db.execute('''SELECT * FROM comments;''').fetchall()
    count_comments=db.execute('''SELECT COUNT(*) FROM comments;''').fetchall()
    total=0
    for comment in comments:
        total+=1
    print(total)
    if form.validate_on_submit():
        username=g.user
        comment=form.comment.data
        db=get_db()
        
        if comment is not None:
            update_comments= db.execute('''INSERT INTO comments(username, comment)
                                            VALUES(?, ?);''', (username, comment))
            db.commit()
            
            return render_template("comments.html", form=form, message="Thank you for your comment!", comments=comments, title="Comment Section", total=total, comment="")
        else:

            return render_template("comments.html", form=form, comments=comments, title="Comment Section", total=total, comment="")
    return render_template("comments.html", form=form, comments=comments, title="Comment Section", total=total, comment="")
@app.route("/leaderboard", methods=["GET", "POST"])

def leaderboard():
    db=get_db()
    leaders=db.execute('''SELECT * FROM points
                            ORDER BY point DESC LIMIT 10;''').fetchall()
    return render_template("leaderboard.html", leaders=leaders, title="LeaderBoard")
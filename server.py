import json
from flask import Flask, render_template, request, redirect, flash, url_for, abort

def create_app():

    def loadClubs():
        with open('clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs


    def loadCompetitions():
        with open('competitions.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions


    app = Flask(__name__)
    app.secret_key = 'something_special'

    competitions = loadCompetitions()
    clubs = loadClubs()


    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        """ 
        Log the user if his email is registered in the database, if not abort with a 404 status code. 
        """
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
        except IndexError:
            return redirect('/invalidemail')

        return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/invalidemail')
    def invalidEmail():
        """ 
        Inform the user that his email his not registered.
        """
        return render_template('wrongemail.html')


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():

        selected_competition = request.form['competition']
        selected_club = request.form['club']

        competition = [c for c in competitions if c['name'] == selected_competition][0]
        club = [c for c in clubs if c['name'] == selected_club][0]

        placesRequired = int(request.form['places'])

        if int(club['points'])-placesRequired >= 0:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            club['points'] = int(club['points'])-placesRequired
        else:
            flash('')
            return redirect(f'/book/{selected_competition}/{selected_club}')

        if placesRequired != 0:
            flash('Great-booking complete!')
        else:
            pass

        return render_template('welcome.html', club=club, competitions=competitions)


    # TODO: Add route for points display


    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))


    if __name__ == '__main__':
        app.run(debug=True)

    return app

create_app()
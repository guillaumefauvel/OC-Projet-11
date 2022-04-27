from re import L
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for

from helpers.data_manager import loadCompetitions, loadClubs, saveClubs, saveCompetitions

def create_app(mode):
    
    if mode == 'Production':
        print('--- Server\'s database in production mode ---')
        clubs_db = 'database/clubs.json' 
        competitions_db = 'database/competitions.json'
    elif mode == 'Debugging':
        print('--- Server\'s database in debugging mode ---')
        clubs_db = 'tests/test_database/clubs.json' 
        competitions_db = 'tests/test_database/competitions.json'
    elif mode == 'Debugging-FreshDB':
        print('--- Server\'s database in debugging mode ---')
        clubs_db = 'tests/test_database/clubs_fresh_db.json' 
        competitions_db = 'tests/test_database/competitions_fresh_db.json'


    app = Flask(__name__)
    app.secret_key = 'something_special'
    
    competitions = loadCompetitions(competitions_db)
    clubs = loadClubs(clubs_db)

    def data_update(clubs, competitions):
        """ Update the database if the server's mode is 'Production'
        Args:
            clubs (list): club's dataset
            competitions (list): competitions's dataset
        """
        if mode == 'Production':
            saveClubs(clubs, clubs_db)
            saveCompetitions(competitions, competitions_db)


    @app.route('/')
    def index():

        return render_template('index.html')


    @app.route('/showSummary', methods=['POST'])
    @app.route('/showSummary')
    def showSummary():
        """ 
        Log the user if his email is registered in the database, if not abort with a 404 status code. 
        """
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
        except IndexError:
            return redirect('/invalidemail')
        except KeyError:
            return redirect('/forbidden')
  
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @app.route('/invalidemail')
    def invalidEmail():
        """ 
        Inform the user that his email his not registered.
        """
        return render_template('wrongemail.html')


    @app.route('/forbidden')
    def forbidden():
        """ 
        Inform the user that his email his not registered.
        """
        return render_template('not_connected.html')


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        """ Return the correct template of an event book page.
            If the event doesn't exist it redirect to the summary page
        Args:
            competition (list): club's dataset
            club (list): competiton's dataset
        """
        actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:        
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [c for c in competitions if c['name'] == competition][0]
        except IndexError:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions, time=actual_time)

        if foundCompetition['date'] < actual_time:
            return render_template('booking_not_allowed.html', club=foundClub, competition=foundCompetition)
        elif foundClub and foundCompetition:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
            
            
    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        """ Use the credit specified to book an event. """

        selected_competition = request.form['competition']
        selected_club = request.form['club']
        actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        competition = [c for c in competitions if c['name'] == selected_competition][0]
        club = [c for c in clubs if c['name'] == selected_club][0]

        if competition['date'] < actual_time:
            flash("You cannot book from a closed competition")
            return render_template('welcome.html', club=club, competitions=competitions, time=actual_time)
        
        try:
            placesRequired = int(request.form['places'])
        except ValueError:
            return render_template('welcome.html', club=club, competitions=competitions, time=actual_time)

        if placesRequired > 12:
            flash('You cannot book more than 12 places')
            return redirect(f'/book/{selected_competition}/{selected_club}')

        elif placesRequired < 0:
            flash('You need to specify a positive number')
            return redirect(f'/book/{selected_competition}/{selected_club}')

        elif int(club['points'])-placesRequired >= 0:
            
            try:
                if competition['bookedPerClub'][club['name']] + placesRequired > 12:
                    flash('You have reach your max reservation credit for this event')
                    return redirect(f'/book/{selected_competition}/{selected_club}')
                else:
                    competition['bookedPerClub'][club['name']] += placesRequired
                    data_update(clubs, competitions)
            except KeyError:
                competition['bookedPerClub'] = {}
                competition['bookedPerClub'][club['name']] = placesRequired
                data_update(clubs, competitions)
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            club['points'] = int(club['points'])-placesRequired
            data_update(clubs, competitions)

        elif int(club['points'])-placesRequired < 0:
            flash('You don\'t have enough point')
            return redirect(f'/book/{selected_competition}/{selected_club}')

        if placesRequired != 0:
            flash('Great-booking complete!')
        else:
            pass
        data_update(clubs, competitions)
        return render_template('welcome.html', club=club, competitions=competitions, time=actual_time)


    @app.route('/logout')
    def logout():
        """ Logout and redirect the user to the login page """
        return redirect(url_for('index'))
    
    
    @app.route('/detailed-board')
    def detailed_board():
        """ Show the board that recap clubs and competitions booking's history and credits """
        
        first_row = [""] + [v['name'] for v in clubs] + ['Total', 'Available']
        second_row = ["Points available"] + [v['points'] for v in clubs] + [sum([int(v['points']) for v in clubs])] + [""]
        list_of_rows = []
        
        for competition in competitions:
            
            fresh_row = []
            
            for club in [v['name'] for v in clubs]:
                try:
                    fresh_row += [competition['bookedPerClub'][club]]
                except:
                    fresh_row += [0]
            
            finished_row = [competition['name']] + fresh_row + [sum(fresh_row)] + [competition['numberOfPlaces']]
                                                                               
            list_of_rows.append(finished_row)
        
        return render_template('display_detailed_board.html',
                                first_row=first_row,
                                second_row=second_row,
                                list_of_rows=list_of_rows)
    
    if __name__ == '__main__':
        app.run(debug=True)

    return app


create_app(mode='Debugging')
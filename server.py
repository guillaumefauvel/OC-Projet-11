from pprint import pprint
from re import L
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

from helpers.data_manager import loadCompetitions, loadClubs, saveClubs, saveCompetitions

def create_app():
    
    test_mode = False
    
    if __name__ == '__main__':
        clubs_db = 'database/clubs.json' 
        competitions_db = 'database/competitions.json'
    else:
        test_mode = True
        clubs_db = 'tests/test_database/clubs.json' 
        competitions_db = 'tests/test_database/competitions.json'


    app = Flask(__name__)
    app.secret_key = 'something_special'
    
    competitions = loadCompetitions(competitions_db)
    clubs = loadClubs(clubs_db)

    def data_update(clubs, competitions):

        if not test_mode:
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

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    
    @app.route('/detailed-board')
    def detailed_board():

        table = {}
        total_points_events = {}

        for club in clubs:
            club_name = club['name']

            ref_list = []
            
            for comp in competitions:
                for associated_club in list(comp['bookedPerClub'].keys()):
                    if associated_club == club_name:
                        ref_list.append(comp['bookedPerClub'][club_name])
                        try: 
                            old_value = total_points_events[comp['name']]
                            total_points_events[comp['name']] = old_value + comp['bookedPerClub'][club_name]
                        except KeyError:
                            total_points_events[comp['name']] = comp['bookedPerClub'][club_name]
                    elif club_name not in list(comp['bookedPerClub'].keys()):
                        ref_list.append(0)

            table[f'{club_name}'] = {
                "points": club['points'],
                "ref_list": ref_list,
            }
            
        clubs_total_points = sum([int(table[v]['points']) for v in table])
        
        return render_template('display_detailed_board.html',
                               competitions=competitions,
                               table=table,
                               total_points_events=total_points_events,
                               clubs_total_points=clubs_total_points)
    
    if __name__ == '__main__':
        app.run(debug=True)

    return app

create_app()
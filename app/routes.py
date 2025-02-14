from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import Cinema, Movie, MovieSchedule
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cinema_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cinema = Cinema.query.filter_by(email=email).first()
        
        if cinema and cinema.check_password(password):
            login_user(cinema)
            next_page = request.args.get('next')
            if not next_page or next_page.startswith('http'):
                next_page = url_for('cinema_dashboard')
            return redirect(next_page)
        flash('Email ou mot de passe incorrect')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cinema/dashboard', methods=['GET', 'POST'])
@login_required
def cinema_dashboard():
    if request.method == 'POST':
        # Vérifier si le film existe déjà par son titre
        movie = Movie.query.filter_by(title=request.form['title']).first()

        if movie:
            # Si le film existe, ajouter la séance
            schedule = MovieSchedule(
                movie_id=movie.id,
                cinema_id=current_user.id,
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                screening_days=request.form['screening_days'],
                screening_time=datetime.strptime(request.form['screening_time'], '%H:%M').time()
            )
            db.session.add(schedule)
            db.session.commit()
            flash('Séance ajoutée avec succès !')
        else:
            # Si le film n'existe pas, créer le film et ajouter la séance
            movie = Movie(
                title=request.form['title'],
                duration=int(request.form['duration']),
                language=request.form['language'],
                subtitles=request.form.get('subtitles'),
                director=request.form['director'],
                main_actors=request.form['main_actors'],
                min_age=int(request.form['min_age'])
            )
            db.session.add(movie)
            db.session.commit()

            # Ajouter la séance pour ce film
            schedule = MovieSchedule(
                movie_id=movie.id,
                cinema_id=current_user.id,
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                screening_days=request.form['screening_days'],
                screening_time=datetime.strptime(request.form['screening_time'], '%H:%M').time()
            )
            db.session.add(schedule)
            db.session.commit()
            flash('Film et séance ajoutés avec succès !')

        return redirect(url_for('cinema_dashboard'))

    # Récupérer toutes les séances pour le cinéma actuel
    movies = MovieSchedule.query.filter_by(cinema_id=current_user.id).all()
    return render_template('cinema_dashboard.html', movies=movies)

@app.route('/movies/<city>')
def movies_by_city(city):
    # Récupérer tous les cinémas dans la ville donnée
    cinemas = Cinema.query.filter_by(city=city).all()
    
    if not cinemas:
        return render_template('movie_list.html', movies=[], city=city)
    
    cinema_ids = [cinema.id for cinema in cinemas]
    
    # Récupérer toutes les projections dans ces cinémas
    schedules = MovieSchedule.query.filter(MovieSchedule.cinema_id.in_(cinema_ids)).all()
    
    # Organiser les données pour les passer au template
    movies_data = []
    for schedule in schedules:
        movie_data = {
            'id': schedule.movie.id,
            'title': schedule.movie.title,
            'cinema': schedule.cinema.name,
            'address': schedule.cinema.address,
            'screening_days': schedule.screening_days,
            'screening_time': schedule.screening_time.strftime('%H:%M'),
            'start_date': schedule.start_date.strftime('%Y-%m-%d'),
            'end_date': schedule.end_date.strftime('%Y-%m-%d')
        }
        movies_data.append(movie_data)
    
    return render_template('movie_list.html', movies=movies_data, city=city)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    schedules = MovieSchedule.query.filter_by(movie_id=movie_id).all()
    
    movie_data = {
        'title': movie.title,
        'duration': movie.duration,
        'language': movie.language,
        'subtitles': movie.subtitles,
        'director': movie.director,
        'main_actors': movie.main_actors,
        'min_age': movie.min_age,
        'schedules': [{
            'cinema_name': schedule.cinema.name,
            'address': schedule.cinema.address,
            'screening_days': schedule.screening_days,
            'screening_time': schedule.screening_time.strftime('%H:%M'),
            'start_date': schedule.start_date.strftime('%Y-%m-%d'),
            'end_date': schedule.end_date.strftime('%Y-%m-%d')
        } for schedule in schedules]
    }
    
    return render_template('movie_details.html', movie=movie_data)

@app.route('/api/movies', methods=['POST'])
def add_movie_api():
    # Récupérer les données JSON envoyées
    data = request.get_json()

    # Créer un nouveau film avec les données envoyées
    movie = Movie(
        title=data['title'],
        duration=data['duration'],
        language=data['language'],
        subtitles=data.get('subtitles', None),
        director=data['director'],
        main_actors=data['main_actors'],
        min_age=data['min_age']
    )

    # Ajouter le film à la base de données
    db.session.add(movie)
    db.session.commit()

    # Retourner une réponse JSON avec le film ajouté
    return jsonify({'message': 'Film ajouté avec succès', 'movie': data}), 201

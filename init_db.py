from app import app, db
from app.models import Cinema

def init_db():
    with app.app_context():
        # Création des tables
        db.create_all()

        # Création d'un cinéma de test
        cinema = Cinema(
            name='Cinéma Test',
            email='test@cinema.com',
            address='123 Avenue des Champs-Élysées',
            city='Paris'
        )
        cinema.set_password('test123')

        # Ajout à la base de données
        db.session.add(cinema)
        db.session.commit()

        print("Base de données initialisée avec succès!")
        print("Identifiants de test :")
        print("Email : test@cinema.com")
        print("Mot de passe : test123")

if __name__ == '__main__':
    init_db() 
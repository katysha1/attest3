from handlers import user_handler as uh
from record_bd import database as d_b
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def connection_db():
    engine = create_engine(os.getenv('DB'))
    Session = sessionmaker(bind=engine)
    session = Session()
    print("Подключение создано")
    return engine, session

def disconnection_db(session, engine):
    session.close()
    engine.dispose()
    print("Подключение закрыто")

def add_note(note: str, session) -> str:

    new_note = d_b.Base(note=uh.add_note)
    session.add(new_note)
    session.commit()
    print(f"Заметка '{new_note.id}. {new_note}' успешно добавлена")
    return


def delete_note(note_id: int, session) -> str:
    try:
        notes = session.query(d_b.Base).filter_by(id=note_id).first()
        if not notes:
            print(f"Заметка с id={note_id} не найдена")
            return

        session.delete(notes)
        session.commit()
        print(f"Заметка '{d_b.Base.note}' успешно удалена.")
        return

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка при удалении: {str(e)}")
        return


def note_list(session):
    notes = session.query(d_b.Base).order_by(d_b.Base.id).all()
    for note in notes:
        print(f'{d_b.Base.id}. {d_b.Base.note}')
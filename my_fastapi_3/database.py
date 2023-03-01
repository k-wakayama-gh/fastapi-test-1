from sqlmodel import SQLModel, create_engine, Session

sqlite_file = 'sqlite:///database.sqlite'
engine = create_engine(sqlite_file, echo=True, connect_args={'check_same_thread': False})

def create_database():
    SQLModel.metadata.create_all(bind=engine)


def get_db():
    with Session(engine) as db:
        try:
            yield db
        finally:
            db.close()

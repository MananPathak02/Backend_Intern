from sqlmodel import SQLModel, Field, create_engine, Session, select

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def insert_sample_data():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()

        if len(tasks) == 0:
            session.add(Task(title="Learn FastAPI", done=False))
            session.add(Task(title="Do Assignment", done=False))
            session.add(Task(title="Sleep", done=True))
            session.commit()
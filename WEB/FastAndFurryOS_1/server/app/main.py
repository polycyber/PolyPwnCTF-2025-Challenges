from typing import Union, Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .default_data import default_data

class Car(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    cylinders: str = Field(default=False)
    nitro_quantity: int = Field(default=0)
    image: str | None = Field(default=None)

def populate_db(session: Session):
    session.exec(text(f'DELETE FROM car;'))
    session.exec(text(f'DELETE FROM user;'))
    session.exec(text(f'DELETE FROM password;'))
    for car_data in default_data["cars"]:
        car = Car(**car_data)
        session.add(car)
    for user_data in default_data["users"]:
        user = User(**user_data)
        session.add(user)
    for password_data in default_data["passwords"]:
        password = Password(**password_data)
        session.add(password)
    session.commit()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str

class Password(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    hash: str


class LoginRequest(BaseModel):
    user_name: str
    password: str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        populate_db(session)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/cars/")
def read_cars(
    session: SessionDep,
) -> list[Car]:
    """
        Get list of cars.
    """
    cars = session.exec(select(Car)).all()
    return cars

@app.get("/users/")
def read_users(
    session: SessionDep
) -> Union[list[str], list[User]]:
    """
        Read users from db!
    """
    users = session.exec(select(User)).all()
    return [u.name for u in users]

@app.get("/users/{user_id}")
def read_user(
    user_id: int,
    session: SessionDep,
    detailedData: bool = Query(False, description="Return detailed user data for debugging.")
    ) -> Union[User, str]:
    try:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if detailedData:
            user.secret_name = "[REDACTED]"
            return user
        return user.name
    except Exception as e:
        raise HTTPException(status_code=400)

@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    """
        Create a new user in the database.

        <b> DEV NOTE: Implementation not done yet. </b>

        polycyber{D0NT_K33P_D3V_4RT1F4CTS_1N_PR0DUCT10N}
    """
    raise HTTPException(status_code=501)


@app.post("/login/")
def validate_credentials(login: LoginRequest, session: SessionDep) -> Union[User, str]:
    """
        Validate credentials, to get token for accessing the mythical FurryOS! <b>UvU<b/>
        
        <b> DEV NOTE: Implementation not done yet. If you are a developper, you may use </b> <a href="http://ctf.polycyber.io:20303/#/dev_testing/furry_login">http://ctf.polycyber.io:20303/#/dev_testing/furry_login<a/> for testing.
    """
    raise HTTPException(status_code=501)

@app.post("/secret_tmp_login/", include_in_schema=False)
def tmp_validate_credentials(login: LoginRequest, session: SessionDep) -> Union[User, str]:
    """
        For development purposes only. Do not use in production.
    """
    user_name: int = login.user_name
    password: str = login.password
    user_hash = compute_hash(password)
    validation = None
    try:
        # SPOILER: here is an example of an injection that works to get the flag:
        # user_name = '")) union select user.name, user.secret_name from user where user.name="Flagster" -- '
        validation = session.exec(text(f'SELECT user.name, user.secret_name FROM password INNER JOIN user ON password.user_id = user.id where ((user.name = "{user_name}") and (password.hash = "{user_hash}"));')).all()
    except Exception as e:
        session.rollback()
        return str(e)
    session.rollback()
    if not validation:
        return "Invalid credentials"
    return f"Thank you {validation[0][0]} (aka {validation[0][1]}), your token will be sent to you shortly."

def compute_hash(password: str) -> str:
    pass_hex = [ord(a) for a in password]
    pass_hex = "".join([str(hex(a))[2:] for a in pass_hex])
    return pass_hex


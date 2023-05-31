from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DB:
    def __init__(self, url: str, models: any):
        self.url = url
        self.engine = create_engine(
            self.url, connect_args={"check_same_thread": False}
        )
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)()
        models.Base.metadata.create_all(bind=self.engine)





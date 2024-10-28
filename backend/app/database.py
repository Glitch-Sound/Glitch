from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import sys
sys.path.append('~/app')

from crud.common import generate_bigrams

SQLALCHEMY_DATABASE_URL = "sqlite:///./glitch.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup_fts():
    with SessionLocal() as session:
        conn = session.connection().connection
        conn.create_function('generate_bigrams', 1, generate_bigrams)

        session.execute(text("""
            CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
                rid UNINDEXED,
                title,
                detail,
                result,
                bigrams,
                content='items',
                content_rowid='rid'
            );
        """))

        session.execute(text("""
            CREATE VIRTUAL TABLE IF NOT EXISTS activities_fts USING fts5(
                rid UNINDEXED,
                activity,
                bigrams,
                content='activities',
                content_rowid='rid'
            );
        """))

        session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS items_ai AFTER INSERT ON items BEGIN
                INSERT INTO items_fts(rowid, rid, title, detail, result, bigrams)
                VALUES (
                    new.rid,
                    new.rid,
                    new.title,
                    new.detail,
                    new.result,
                    generate_bigrams(new.title || new.detail || new.result)
                );
            END;
        """))

        session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS activities_ai AFTER INSERT ON activities BEGIN
                INSERT INTO activities_fts(rowid, rid, activity, bigrams)
                VALUES (
                    new.rid,
                    new.rid,
                    new.activity,
                    generate_bigrams(new.activity)
                );
            END;
        """))

        session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS items_au AFTER UPDATE ON items BEGIN
                UPDATE items_fts
                SET
                    title = new.title,
                    detail = new.detail,
                    result = new.result,
                    bigrams = generate_bigrams(new.title || new.detail || new.result)
                WHERE rowid = new.rid;
            END;
        """))

        session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS activities_au AFTER UPDATE ON activities BEGIN
                UPDATE activities_fts
                SET
                    activity = new.activity,
                    bigrams = generate_bigrams(new.activity)
                WHERE rowid = new.rid;
            END;
        """))

        session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS items_ad AFTER DELETE ON items BEGIN
                DELETE FROM items_fts WHERE rowid = old.rid;
            END;
        """))

        session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS activities_ad AFTER DELETE ON activities BEGIN
                DELETE FROM activities_fts WHERE rowid = old.rid;
            END;
        """))

        session.commit()

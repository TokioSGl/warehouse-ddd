from warehouse_ddd import model, services, config, db_tables, unit_of_work, auth, session

from sqlalchemy import create_engine
from sqlalchemy.orm import  Session


def seed_db(session: Session) -> None:
    uow = unit_of_work.SqlAlchemyUnitOfWork(session)
    
    lines = (
        model.OrderLine("table-001", "table", 10),
        model.OrderLine("table-001", "table", 30),
        model.OrderLine("table-001", "table", 20),
        model.OrderLine("chair-005", "chair", 20),
        model.OrderLine("chair-005", "chair", 20),
    )

    batch_tables = model.Batch("batch-001", "table", 100, None)
    batch_chairs = model.Batch("batch-002", "chair", 150, None)

    with uow:
        uow.batches.add(batch_tables)
        uow.batches.add(batch_chairs)
        
        for line in lines:
            services.allocate(line, uow)

        uow.commit()

    session.add(auth.model.User("test@gmail.com", "testpassword"))

    session.commit()


if __name__ == "__main__":
    engine = create_engine(config.build_db_uri(".env"))

    try:
        db_tables.create_all(bind=engine)
        db_tables.start_mappers()
    except Exception:
        pass

    seed_db(session.SessionManager())

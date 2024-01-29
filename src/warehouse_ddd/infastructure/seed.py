from warehouse_ddd import auth

from sqlalchemy.orm import  Session

from warehouse_ddd.domain import model, services, unit_of_work
from warehouse_ddd.infastructure import db_tables, session


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

    db_tables.create_tables()
    seed_db(session.SessionManager())

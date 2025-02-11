from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from sqlalchemy import event

class Base(DeclarativeBase):
    pass


class Point(Base):
    __tablename__ = "point"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    x: Mapped[int]
    y: Mapped[int]

    def __init__(self, x, y, **kw):
        super().__init__(x=x, y=x, **kw)
        self.x_plus_y = x + y

@event.listens_for(Point, "load")
def receive_load(target, context):
    target.x_plus_y = target.x + target.y

@event.listens_for(Point, "refresh")
@event.listens_for(Point, "refresh_flush")
def receive_load(target, context, attrs):
    target.x_plus_y = target.x + target.y

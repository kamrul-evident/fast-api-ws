from typing import NewType

from sqlalchemy import SmallInteger, BigInteger, JSON, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import CreateTable


nstr30 = NewType("nstr30", str)
nstr50 = NewType("nstr50", str)
type SmallInt = int
type BigInt = int
type JsonScalar = str | float | bool | None


class TABase(DeclarativeBase):
    type_annotation_map = {
        nstr30: String(30),
        nstr50: String(50),
        SmallInt: SmallInteger,
        BigInteger: BigInt,
        JsonScalar: JSON,
    }


class SomeTable(TABase):
    __tablename__ = "some_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    normal_str: Mapped[str]
    short_str: Mapped[nstr30]
    long_str_nullable: Mapped[nstr50 | None]
    small_int: Mapped[SmallInt]
    big_int: Mapped[BigInteger]
    scalar_col: Mapped[JsonScalar]
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Plant:
    __tablename__ = 'plants'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    plant_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    inverters = relationship('Inverter', back_populates='plant')


@table_registry.mapped_as_dataclass
class Inverter:
    __tablename__ = 'inverters'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    plant_id: Mapped[int] = mapped_column(ForeignKey('plants.id'))

    plant = relationship('Plant', back_populates='inverters')
    metrics = relationship('Metric', back_populates='inverter')


@table_registry.mapped_as_dataclass
class Metric:
    __tablename__ = 'metrics'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    datetime: Mapped[datetime]
    power: Mapped[float]
    temp_celsius: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    inverter_id: Mapped[int] = mapped_column(ForeignKey('inverters.id'))

    inverter = relationship('Inverter', back_populates='metrics')

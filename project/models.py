"""All Models for database are defined here"""
from typing import Optional, List
from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, SQLModel, Relationship


class VrfLink(SQLModel, table=True):
    """Used for vrf to device link"""
    vrf_id: Optional[int] = Field(default=None, foreign_key="vrf.id", primary_key=True)
    device_id: Optional[int] = Field(
        default=None, foreign_key="device.id", primary_key=True
    )


class Platform(SQLModel, table=True):
    """Used to define platforms"""
    id: Optional[int] = Field(default=None, primary_key=True)
    platform_name: str = Field(index=True)


class Vrf(SQLModel, table=True):
    """used to define VRFs"""
    id: Optional[int] = Field(default=None, primary_key=True)
    vrf_name: str = Field(index=True)
    devices: List["Device"] = Relationship(back_populates="vrfs", link_model=VrfLink)


class Device(SQLModel, table=True):
    """Used to define a simple device"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    mgmt: str
    platform_id: Optional[int] = Field(
        sa_column=Column(
            Integer, ForeignKey("platform.id", ondelete="SET NULL", onupdate="CASCADE")
        )
    )
    vrfs: List["Vrf"] = Relationship(back_populates="devices", link_model=VrfLink)

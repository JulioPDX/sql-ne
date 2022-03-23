#!/usr/bin/env python

"""
Simple example to show the power of SQLModel. Based on the great documentation
by the SQLModel creator. Amazing tool!
"""

from rich import print as rprint
from sqlmodel import Session, select
# Disable cache warning
from sqlmodel.sql.expression import Select, SelectOfScalar
from models import Device, Platform, Vrf, VrfLink
from database import engine, create_db_and_tables


SelectOfScalar.inherit_cache = True
Select.inherit_cache = True


def create_devices():
    """Creates a few devices and platforms"""
    with Session(engine) as session:
        eos_platform = Platform(platform_name="eos")
        aoscx_platform = Platform(platform_name="aoscx")
        session.add(eos_platform)
        session.add(aoscx_platform)
        session.commit()

        d_1 = Device(name="eos1", mgmt="192.168.10.143", platform_id=eos_platform.id)
        d_2 = Device(name="cx1", mgmt="192.168.10.30", platform_id=aoscx_platform.id)
        d_3 = Device(name="eos2", mgmt="192.168.10.151", platform_id=eos_platform.id)

        session.add(d_1)
        session.add(d_2)
        session.add(d_3)
        session.commit()

        plat = session.exec(select(Platform).where(Platform.id == 1)).one()
        plat.id = 123
        session.add(plat)
        session.commit()


def create_vrfs():
    """Simple loop to create VRFs"""
    with Session(engine) as session:
        for i in range(1, 4):
            vrf = Vrf(vrf_name=f"VRF{i}", id=i)
            session.add(vrf)
        session.commit()


def select_devices():
    """Varitey of query options with select"""
    with Session(engine) as session:
        statement = select(Device)
        result = session.exec(statement).fetchall()
        rprint(result)

        statement = select(Device).where(Device.name == "eos1")
        result = session.exec(statement).one()
        rprint(result)

        # Combining select and session.exec in one line
        result = session.exec(
            select(Device, Platform).where(Device.platform_id == Platform.id)
        ).fetchall()
        for device, platform in result:
            rprint("Device:", device.name, "Platform:", platform.platform_name)

        # Chaining statements together
        result = session.exec(
            select(Device.name, Vrf.vrf_name)
            .select_from(VrfLink)
            .join(Device)
            .where(VrfLink.device_id == Device.id)
            .join(Vrf)
            .where(VrfLink.vrf_id == Vrf.id)
        ).fetchall()
        rprint(result)


def update_devices():
    """Used to update a device attribute"""
    with Session(engine) as session:
        device = session.exec(select(Device).where(Device.name == "eos1")).one()
        # Before change
        print(device)
        device.mgmt = "10.10.10.10"
        session.add(device)
        session.commit()
        session.refresh(device)
        # After change
        rprint(device)


def update_vrfs():
    """Example to assign VRFs to devices"""
    with Session(engine) as session:
        device1 = session.exec(select(Device).where(Device.name == "eos1")).one()
        device2 = session.exec(select(Device).where(Device.name == "cx1")).one()
        vrf1 = session.exec(select(Vrf).where(Vrf.vrf_name == "VRF1")).one()
        vrf2 = session.exec(select(Vrf).where(Vrf.vrf_name == "VRF2")).one()
        vrf3 = session.exec(select(Vrf).where(Vrf.vrf_name == "VRF3")).one()

        device1.vrfs.append(vrf1)
        device1.vrfs.append(vrf2)
        device2.vrfs.append(vrf1)
        device2.vrfs.append(vrf2)
        device2.vrfs.append(vrf3)
        session.add(device1)
        session.add(device2)
        session.commit()
        session.refresh(device1)
        session.refresh(device2)

        rprint(device1.name, device1.vrfs)
        rprint(device2.name, device2.vrfs)


def delete_devices():
    """Simple example to delete device"""
    with Session(engine) as session:
        device = session.exec(select(Device).where(Device.name == "eos2")).one()
        print(device)

        session.delete(device)
        session.commit()
        rprint("Deleted device", device)


def main():
    """Add whatever is required for execution here"""
    create_db_and_tables()
    create_devices()
    create_vrfs()
    update_vrfs()
    select_devices()


if __name__ == "__main__":
    main()

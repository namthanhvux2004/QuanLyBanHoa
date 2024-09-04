from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class KhachHang(Base):
    __tablename__ = "KhachHang"
    id = Column(Integer, primary_key=True)
    ten = Column(String(20))
    khach_hang_than_thiet = Column(String(20), default = "Khong")
    sdt = Column(String(15), unique = True, index= True)
    tong_tien_tieu = Column(Integer, default = 0)
    ds_hoa_don = relationship("HoaDon")

class Hoa(Base):
    __tablename__ = "Hoa"
    id = Column(Integer, primary_key = True)
    ten = Column(String(20), unique = True)
    gia = Column(Integer)

class HoaDon(Base):
    __tablename__ = "HoaDon"
    id = Column(Integer, primary_key = True)
    date = Column(Integer)
    id_hoa = Column(Integer, ForeignKey("Hoa.id"))
    id_khach_hang = Column(Integer, ForeignKey("KhachHang.id"))
    so_luong = Column(Integer)
    tong_tien = Column(Integer, default = 0)
    hoa_da_mua = relationship("Hoa")


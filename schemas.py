from pydantic import BaseModel

class HoaBase(BaseModel):
    ten: str
    gia: int

class HoaCreate(HoaBase):
    pass

class Hoa(HoaBase):
    id : int
    class Config:
        orm_mode = True

class HoaDonBase(BaseModel):
    date: int

class HoaDonCreate(HoaDonBase):
    ten_hoa: str
    sdt_khach: str
    so_luong: int

class HoaDon(HoaDonBase):
    id: int
    id_hoa: int
    id_khach_hang: int
    so_luong: int
    tong_tien: int
    class Config:
        orm_mode = True

class KhachHangBase(BaseModel):
    ten: str
    sdt: str

class KhachHangCreate(KhachHangBase):
    pass

class KhachHang(KhachHangBase):
    id: int
    khach_hang_than_thiet: str
    tong_tien_tieu: int
    ds_hoa_don: list[HoaDon]

    class Congif:
        orm_mode = True

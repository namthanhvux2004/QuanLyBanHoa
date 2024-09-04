from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/hoa/create", response_model=schemas.Hoa)
def create_hoa(hoa: schemas.HoaCreate, db: Session = Depends(get_db)):
    return crud.create_hoa(db, hoa)

@app.get("/hoa/list")
def get_all_hoa(db: Session = Depends(get_db)):
    return crud.get_hoa_all(db)

@app.post("/khachhang/create", response_model=schemas.KhachHang)
def create_KH(khach_hang: schemas.KhachHangCreate, db: Session = Depends(get_db)):
    return crud.create_khach_hang(db, khach_hang)

@app.get("/khachhang/list")
def get_all_KH(db : Session = Depends(get_db)):
    return crud.get_khach_hang_all(db)

@app.post("/hoadon/create", response_model=schemas.HoaDon)
def create_hoa_don(hoa_don: schemas.HoaDonCreate, db: Session = Depends(get_db)):
    return crud.create_hoa_don(db, hoa_don)

@app.get("/hoa/list/{ten_hoa}")
def get_hoa_by_ten(ten_hoa: str, db: Session = Depends(get_db)):
    return crud.get_hoa_by_ten(db, ten_hoa)

@app.get("/hoadon/list")
def get_hoa_don_all(db: Session = Depends(get_db)):
    return crud.get_hoa_don_all(db)

@app.get("/doanhthu/ngay/{ngay}")
def get_doanh_thu_ngay(ngay: int, db: Session = Depends(get_db)):
    return crud.doanh_thu_ngay(db, ngay)

@app.get("/doanhtu/thang/{thang}/{nam}")
def get_doanh_thu_thang(thang: int, nam: int, db: Session = Depends(get_db)):
    return crud.doanh_thu_thang(db, thang, nam)

@app.get("/doanhthu/quy/{quy}/{nam}")
def get_doanh_thu_quy(quy: int, nam: int, db: Session = Depends(get_db)):
    return crud.doanh_thu_quy(db, quy, nam)

@app.get("/doanhthu/nam/{nam}")
def get_doanh_thu_nam(nam: int, db: Session = Depends(get_db)):
    return crud.doanh_thu_nam(db, nam)

@app.get("/khachhang/{sdt}/hoadon")
def get_hoa_don_by_khach_hang(sdt: str, db: Session = Depends(get_db)):
    return crud.hoa_don_khach_hang(db, sdt)

@app.get("/khachhang/{sdt}/hoadon/{ngay}")
def get_hoa_don_khach_hang_ngay(sdt: str, ngay: int, db: Session = Depends(get_db)):
    return crud.hoa_don_khach_hang_ngay(db, sdt, ngay)

@app.get("/khachhang/{sdt}/hoadon/t{thang}/{nam}")
def get_hoa_don_khach_hang_thang(sdt: str, thang: int, nam: int, db: Session = Depends(get_db)):
    return crud.hoa_don_khach_hang_thang(db, sdt, thang, nam)

@app.get("/khachhang/{sdt}/hoadon/quy/{quy}/{nam}")
def get_hoa_don_khach_hang_quy(sdt: str, quy: int, nam: int, db: Session = Depends(get_db)):
    return crud.hoa_don_khach_hang_quy(db, sdt, quy, nam)

@app.get("/khachhang/{sdt}/hoadon/nam/{nam}")
def get_hoa_don_khach_hang_nam(sdt: str, nam: int, db: Session = Depends(get_db)):
    return crud.hoa_don_khach_hang_nam(db, sdt, nam)

# @app.get("/khachhang/{sdt}/dothanthiet")
# def danh_gia_do_than_thiet(sdt: str, db: Session = Depends(get_db)):
#     return crud.danh_gia_do_than_thiet(db, sdt)
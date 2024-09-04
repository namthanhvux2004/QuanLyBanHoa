from sqlalchemy.orm import Session
from datetime import date
import models, schemas

def get_khach_hang(db: Session, user_id: int):
    return db.query(models.KhachHang).filter(models.KhachHang.id == user_id).first()

def get_khach_hang_all(db: Session):
    return db.query(models.KhachHang).all()

def get_khach_hang_by_sdt(db: Session, sdt: str):
    return db.query(models.KhachHang).filter(models.KhachHang.sdt == sdt).first()

def giam_gia_theo_do_than_thiet(do_than_thiet: str):
    if do_than_thiet == "Dong":
        return 0.95
    if do_than_thiet == "Bac":
        return 0.90
    if do_than_thiet == "Vang":
        return 0.85
    if do_than_thiet == "Kim Cuong":
        return 0.80
    return 1
    
def lam_tron_tien(tien: float):
    return round(tien/1000)*1000

def cong_tien(db: Session, user_id: int, tien_tieu: int):
    khach_hang = get_khach_hang(db, user_id)
    tien_tieu = lam_tron_tien(tien_tieu*giam_gia_theo_do_than_thiet(khach_hang.khach_hang_than_thiet)) #tinh tien sau khi ap dung giam gia
    khach_hang.tong_tien_tieu+=tien_tieu
    if khach_hang.tong_tien_tieu >= 100000:
        if khach_hang.tong_tien_tieu <= 300000:
            khach_hang.khach_hang_than_thiet = "Dong"
        elif khach_hang.tong_tien_tieu <= 750000:
            khach_hang.khach_hang_than_thiet = "Bac"
        elif khach_hang.tong_tien_tieu <= 1000000:
            khach_hang.khach_hang_than_thiet = "Vang"
        else:
            khach_hang.khach_hang_than_thiet = "Kim Cuong"
    db.commit()
    db.refresh(khach_hang)
    return tien_tieu

def create_khach_hang(db: Session, khach_hang: schemas.KhachHangCreate):
    db_khach_hang = models.KhachHang(ten = khach_hang.ten, sdt = khach_hang.sdt)
    db.add(db_khach_hang)
    db.commit()
    db.refresh(db_khach_hang)
    return db_khach_hang

def get_hoa(db: Session, hoa_id: int):
    return db.query(models.Hoa).filter(models.Hoa.id == hoa_id).first()

def get_hoa_by_ten(db: Session, ten_hoa: str):
    return db.query(models.Hoa).filter(models.Hoa.ten == ten_hoa).first()

def get_hoa_all(db: Session):
    return db.query(models.Hoa).all()

def create_hoa(db: Session, hoa: schemas.HoaCreate):
    db_hoa = models.Hoa(ten = hoa.ten, gia = hoa.gia)
    db.add(db_hoa)
    db.commit()
    db.refresh(db_hoa)
    return db_hoa

def create_hoa_don(db: Session, hoa_don: schemas.HoaDonCreate):
    if hoa_don.date == 0:
        today = date.today()
        nam, thang, ngay = str(today).split('-')
        hoa_don.date = int(nam + thang + ngay)
    khach_hang = get_khach_hang_by_sdt(db, hoa_don.sdt_khach)
    hoa = get_hoa_by_ten(db, hoa_don.ten_hoa)
    db_hoa_don = models.HoaDon(date = hoa_don.date, id_hoa = hoa.id, id_khach_hang = khach_hang.id, so_luong = hoa_don.so_luong, tong_tien = hoa.gia * hoa_don.so_luong)
    db_hoa_don.tong_tien = cong_tien(db, khach_hang.id, db_hoa_don.tong_tien) # cap nhat lai gia tien don hang sau khi ap dung khach hang than thiet
    db.add(db_hoa_don)
    db.commit()
    db.refresh(db_hoa_don)
    return db_hoa_don

def get_hoa_don_all(db: Session):
        return db.query(models.HoaDon).all()

def doanh_thu_ngay(db: Session, ngay: int):
        db_hoa_don = db.query(models.HoaDon).filter(models.HoaDon.date == ngay)
        doanh_thu = 0
        for hoa_don in db_hoa_don:
            doanh_thu += hoa_don.tong_tien
        return doanh_thu

def doanh_thu_thang(db: Session, thang: int, nam: int):
        date_cmp = nam*100 + thang
        db_hoa_don = db.query(models.HoaDon).filter(models.HoaDon.date // 100 == date_cmp)
        doanh_thu = 0
        for hoa_don in db_hoa_don:
            doanh_thu += hoa_don.tong_tien
        return doanh_thu

def doanh_thu_quy(db: Session, quy: int, nam: int):
        dau_quy = nam*100 + 1 + (quy - 1)*3
        cuoi_quy = dau_quy + 3
        db_hoa_don = db.query(models.HoaDon).filter(models.HoaDon.date // 100 >= dau_quy, models.HoaDon.date // 100 <= cuoi_quy)
        doanh_thu = 0
        for hoa_don in db_hoa_don:
            doanh_thu += hoa_don.tong_tien
        return doanh_thu

def doanh_thu_nam(db: Session, nam: int):
        db_hoa_don = db.query(models.HoaDon).filter(models.HoaDon.date // 10000 == nam)
        doanh_thu = 0
        for hoa_don in db_hoa_don:
            doanh_thu += hoa_don.tong_tien
        return doanh_thu

def hoa_don_khach_hang(db: Session, sdt: str):
        db_khach_hang = db.query(models.KhachHang).filter(models.KhachHang.sdt == sdt).first()
        return db_khach_hang.ds_hoa_don

def hoa_don_khach_hang_ngay(db: Session, sdt: str, ngay: int):
    ds_hoa_don = hoa_don_khach_hang(db, sdt)
    hoa_don_theo_ngay = list()
    for hoa_don in ds_hoa_don:
        if hoa_don.date == ngay:
            hoa_don_theo_ngay.append(hoa_don)
    return hoa_don_theo_ngay

def hoa_don_khach_hang_thang(db: Session, sdt: str, thang: int, nam: int):
    ds_hoa_don = hoa_don_khach_hang(db, sdt)
    date_cmp = nam*100 + thang
    hoa_don_theo_thang = list()
    for hoa_don in ds_hoa_don:
        if hoa_don.date // 100 == date_cmp:
            hoa_don_theo_thang.append(hoa_don)
    return hoa_don_theo_thang

def hoa_don_khach_hang_quy(db: Session, sdt: str, quy: int, nam: int):
    ds_hoa_don = hoa_don_khach_hang(db, sdt)
    dau_quy = nam*100 + 1 + (quy - 1)*3
    cuoi_quy = dau_quy + 3
    hoa_don_theo_quy = list()
    for hoa_don in ds_hoa_don:
        if hoa_don.date // 100 >= dau_quy and hoa_don.date // 100 <= cuoi_quy:
            hoa_don_theo_quy.append(hoa_don)
    return hoa_don_theo_quy

def hoa_don_khach_hang_nam(db: Session, sdt: str, nam: int):
    ds_hoa_don = hoa_don_khach_hang(db, sdt)
    hoa_don_theo_nam = list()
    for hoa_don in ds_hoa_don:
        if hoa_don.date // 10000 == nam:
            hoa_don_theo_nam.append(hoa_don)
    return hoa_don_theo_nam

# def danh_gia_do_than_thiet(db: Session, sdt: str):
#     khach_hang = get_khach_hang_by_sdt(db, sdt)
#     if khach_hang.tong_tien_tieu >= 100000:
#         if khach_hang.tong_tien_tieu <= 300000:
#             khach_hang.khach_hang_than_thiet = "Dong"
#         elif khach_hang.tong_tien_tieu <= 750000:
#             khach_hang.khach_hang_than_thiet = "Bac"
#         elif khach_hang.tong_tien_tieu <= 1000000:
#             khach_hang.khach_hang_than_thiet = "Vang"
#         else:
#             khach_hang.khach_hang_than_thiet = "Kim Cuong"
#     db.commit()
#     db.refresh(khach_hang)
#     return khach_hang.khach_hang_than_thiet
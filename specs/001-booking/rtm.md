# RTM: จองคิวตรวจสุขภาพ
อ้างอิง: spec.md SPEC-BKG-001 Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07; ปรับตาม F เมื่อ 2569-10-07 | pytest ล่าสุด: 8 ผ่าน 0 ไม่ผ่าน; Vitest ครั้งล่าสุด: 1 ผ่าน 1 ไม่ผ่าน 1 skipped

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 ถูกระบุใน traceability แต่ตรวจเรื่อง p95 ไม่ใช่การแสดงช่วงว่างและจำนวนที่นั่ง | T-02 เสร็จ; T-10 พร้อมทำ | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | test_FR_BKG_01_lists_slots_through_30_days ผ่าน ตรวจขอบเขต 30 วัน; test_AC_BKG_05 ผ่าน | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 พร้อมทำ | ไม่พบการตรวจคิวเดิมก่อนจองใน backend/app/booking/service.py | ไม่มี test AC-BKG-02 | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 พร้อมทำ | backend/app/booking/router.py: create_booking คืนเพียงข้อความ 409; ยังไม่พบการเลือกช่วงใกล้เคียง | test_TC_BKG_01_2_slot_full ผ่านเฉพาะ 409/ไม่มีจองซ้อน; ไม่ตรวจ 3 ตัวเลือก; Vitest ชื่อเดียวกันไม่ผ่าน | ช่องโหว่ |
| FR-BKG-04 | AC-BKG-01 | T-03 เสร็จ; T-06 รอ Q-02 | backend/app/booking/service.py: create_booking; backend/app/booking/router.py: create_booking | test_AC_BKG_01 และ test_TC_BKG_01_1_booking_succeeds ผ่านและตรวจบันทึก/remaining; การออกและแสดงเลขคิวรอ Q-02 | รอ Q-02 |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ | ไม่พบคิวส่งข้อความหรือ retry ใน backend/app/ | ไม่มี test AC-BKG-04 | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 เสร็จ; T-10 พร้อมทำ | backend/app/slots/service.py: list_available_slots กรอง package_code; ไม่พบการเปลี่ยนแพ็กเกจและโหลดช่วงเวลาใหม่ในหน้าจอ | ไม่มี AC/test ที่ตรวจ FR-BKG-06 | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | test_AC_BKG_05 ผ่าน วัดคำขอ 200 รายการที่เริ่มพร้อมกัน และ p95 ไม่เกิน 2 วินาที | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task เฉพาะ | ไม่พบการตั้งค่า TLS ใน backend/app/ หรือ frontend/src/; การตั้งค่า proxy/deployment อยู่นอกไฟล์ที่ตรวจ | ไม่มี test TLS | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ไม่พบการส่งซ้ำภายใน 5 นาทีใน backend/app/ | ไม่มี test AC-BKG-04 | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC ที่ตรวจเวลา 3 นาที/อัตรา 8 ใน 10 | ไม่มี task เฉพาะ | ไม่พบ flow หน้าจอ booking ใน frontend/src/ | ไม่มี test/ผลทดลองกับผู้ใช้ | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 เสร็จ | backend/app/config.py: DATABASE_URL รองรับ URL จาก environment; backend/app/db/session.py: engine | test_T01_tables_created ผ่านโดยใช้ SQLite; ไม่ได้ยืนยัน PostgreSQL หรือค่า DATABASE_URL ของ deployment | ยังไม่ถึง |
| DOM-PDPA-01 | AC-BKG-06 | T-01 เสร็จ; T-08 พร้อมทำ | backend/app/db/models.py: AuditLog มี schema; ไม่พบ middleware/การเขียน audit log | test_T01_tables_created ผ่านเฉพาะ schema; ไม่มี test AC-BKG-06 | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC เฉพาะ | T-03 เสร็จ | backend/app/auth/idp.py: get_verified_hn | test_TC_BKG_01_3_unauthenticated ผ่านกรณีไม่มี token; ไม่ได้ทดสอบผลยืนยันจาก IDP จริงหรือ token ปลอม | ช่องโหว่ |
| IF-HIS-01 | ไม่มี AC เฉพาะ | T-01 เสร็จ; T-09 พร้อมทำ | backend/app/db/models.py: Booking; ยังไม่พบ HIS lookup; backend/app/booking/router.py: BookingRequest ไม่มี national_id field | test_T01_no_national_id ผ่าน; ไม่มี test การ lookup HIS | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 พร้อมทำ | ไม่พบการวางข้อความเข้าคิวแบบ asynchronous ใน backend/app/ | ไม่มี test AC-BKG-04 | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/config.py: DATABASE_URL; backend/app/db/session.py: engine, get_db | CON-TECH-01 | ยังยืนยัน PostgreSQL ที่ใช้งานจริงไม่ได้ | ตั้ง DATABASE_URL เป็น PostgreSQL ได้ แต่ค่าเริ่มต้นเป็น SQLite; test ใช้ SQLite ตามแผน |
| backend/app/db/migrations/001_init.py: upgrade; backend/app/db/models.py: Slot, Booking, AuditLog | FR-BKG-01, FR-BKG-02, FR-BKG-04, FR-BKG-06, DOM-PDPA-01, IF-HIS-01 | บางส่วน | มี schema bookings เก็บ HN และไม่มี national_id; AuditLog มีแต่ schema; ไม่มี constraint/unique ป้องกันจองซ้ำ |
| backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ไม่ครบ | ยอมรับทุก Authorization ที่ขึ้นต้นด้วย `Bearer verified:` โดยไม่ตรวจ token กับระบบ IDP จริง |
| backend/app/slots/router.py: GET /slots (get_slots); backend/app/slots/service.py: list_available_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | ค้นได้ถึง 30 วันและกรอง package/remaining; ไม่พบ UI เปลี่ยนแพ็กเกจ |
| backend/app/booking/router.py: POST /bookings (create_booking) | FR-BKG-03, FR-BKG-04, IF-HIS-01 | ไม่ครบ | ส่ง 409 พร้อม detail แต่ไม่มีช่วงแนะนำ; request และ logger ไม่ใช้ national_id; HIS lookup ยังไม่ทำ |
| backend/app/booking/service.py: create_booking | FR-BKG-04 | ไม่ครบ | บันทึกและตัดที่นั่ง; queue_no ปล่อยว่างจนกว่า Q-02 จะตอบ |
| frontend/src/api/client.js: getSlots, createBooking | FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-06 | ยังไม่ครบ | เป็นเพียง API client; createBooking ไม่ส่ง Authorization header และไม่มีหน้าเรียกใช้งาน |
| frontend/src/App.jsx: App; frontend/src/main.jsx: bootstrap | ไม่มี flow booking ที่ทำงานจริง | ยังไม่ครบ | App แสดงเฉพาะโครงเริ่มต้น; หน้าจอเลือกเวลา/ยืนยัน/ผลจองยังไม่มี |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ละเมิด Constraint | backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ใช้เพียง prefix `Bearer verified:` เป็นหลักฐานยืนยันตัวตน ไม่ตรวจผลกับ IDP จริง จึงรับ token ที่สร้างเองได้ | |
| F-06 | FR ไม่มี AC | specs/001-booking/spec.md: FR-BKG-01, AC-BKG-05 | FR-BKG-01 | AC-BKG-05 ตรวจ p95 ไม่ได้ตรวจการแสดงช่วงเวลาว่างภายใน 30 วันและจำนวนที่นั่ง; traceability ที่ผูก AC-BKG-05 กับ FR-BKG-01 ไม่ครอบคลุมเนื้อหา FR | |
| F-07 | FR ไม่มี AC | specs/001-booking/spec.md: FR-BKG-06 | FR-BKG-06 | ไม่มี AC สำหรับการเปลี่ยนแพ็กเกจและคำนวณช่วงเวลาว่างใหม่ | |
| F-10 | อ้าง ID ผิดเรื่อง | specs/001-booking/test-cases.md: TC-BKG-01-2; backend/frontend tests ชื่อ test_TC_BKG_01_2_slot_full | AC-BKG-01 / FR-BKG-04 เทียบกับ AC-BKG-03 / FR-BKG-03 | แถวติด AC-BKG-01 แต่ Then เป็นกรณีช่วงเต็มและช่วงแนะนำ 3 ตัวเลือกของ FR-BKG-03; pytest ไม่ assert ตัวเลือก 3 ช่วง และ Vitest ล้มเพราะหน้า UI ยังไม่มี | |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| F-03 | ลบ DELETE /bookings/{booking_id} และ cancel_booking ออกจาก router/service; เอารายการออกจากตารางตามรอยย้อนกลับ | ตรวจ source แล้วไม่พบ route/function สำหรับยกเลิกคิว; UC-02 ยังคงระบุ Out of scope |
| F-02 | เอา national_id ออกจาก BookingRequest และเลิกเขียนลง log | ตรวจ router แล้ว request model และ logger ไม่อ้าง national_id |
| F-04 | ลบ next_queue_no และไม่กำหนด queue_no เอง | ตรวจ service แล้วไม่มีรูปแบบ A001; Q-02 ยังรอคำตอบและ queue_no เป็น nullable |
| F-05 | เปลี่ยน DAYS_AHEAD จาก 14 เป็น 30 | test_FR_BKG_01_lists_slots_through_30_days ยืนยัน +30 อยู่ในผลและ +31 ไม่อยู่; ผ่าน |
| F-08 | เปลี่ยน test_AC_BKG_05 เป็นยิง 200 requests พร้อมกันด้วย session แยก | pytest ผ่านและ p95 ไม่เกิน 2 วินาที |
| F-09 | เพิ่ม assertion ใน test_AC_BKG_01 สำหรับ Booking และ remaining | pytest ผ่านเมื่อยืนยันว่ามี Booking และ remaining เป็น 0 |

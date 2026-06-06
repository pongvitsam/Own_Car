"""Real vehicle maintenance seed data for MyHome CarCare GitHub Pages."""

from __future__ import annotations

import json
from typing import Any


def be_date(day: int, month: int, year_be: int) -> str:
    return f"{year_be - 543:04d}-{month:02d}-{day:02d}"


def year_date(year_be: int, month: int = 6, day: int = 15) -> str:
    return be_date(day, month, year_be)


def log(
    lid: str,
    vid: str,
    date: str,
    shop: str,
    category: str,
    cost: float,
    odo: int = 0,
    alert_km: int = 0,
    alert_month: int = 0,
    ltype: str = "Maintenance",
    shop_note: str = "",
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "id": lid,
        "vehicleId": vid,
        "odo": odo,
        "shop": shop_note if shop == "-" and shop_note else shop,
        "category": category,
        "cost": round(cost, 2),
        "receipt": "",
        "fileLink": "",
        "alertKm": alert_km,
        "alertMonth": alert_month,
        "date": date,
        "type": ltype,
    }
    if shop_note and shop != "-":
        entry["shop"] = f"{shop} — {shop_note[:36]}"
    return entry


def alert_km_offset(odo: int, target: int) -> int:
    return max(0, target - odo) if odo and target else 0


CATEGORIES = [
    {"id": "CAT-001", "name": "เปลี่ยนถ่ายน้ำมันเครื่อง/ของเหลว"},
    {"id": "CAT-002", "name": "ระบบห้ามล้อและเบรก"},
    {"id": "CAT-003", "name": "เปลี่ยนยางและถ่วงล้อ"},
    {"id": "CAT-004", "name": "แบตเตอรี่และระบบขับเคลื่อน"},
    {"id": "CAT-005", "name": "แก๊ส/LPG"},
    {"id": "CAT-006", "name": "ตรอ/ภาษี/พรบ"},
    {"id": "CAT-007", "name": "ประกัน"},
    {"id": "CAT-008", "name": "ของแต่ง/อุปกรณ์"},
    {"id": "CAT-009", "name": "ระบบแอร์"},
    {"id": "CAT-010", "name": "ระบบช่วงล่าง/โช๊ค"},
    {"id": "CAT-011", "name": "บำรุงรักษาใหญ่/ซ่อมเครื่องยนต์"},
    {"id": "CAT-012", "name": "ระบบหม้อน้ำ/ทำความเย็น"},
    {"id": "CAT-013", "name": "ฟิล์ม/ตกแต่งภายนอก"},
]

VEHICLES = [
    {
        "id": "V-001",
        "name": "Mazda",
        "license": "ขต 1062",
        "createdDate": "2024-07-30",
        "insuranceExpiryDate": "2026-08-25",
        "prbExpiryDate": "2026-09-04",
    },
    {
        "id": "V-002",
        "name": "Honda Click 160",
        "license": "รอใส่ทะเบียน",
        "createdDate": "2025-10-04",
        "prbExpiryDate": "2026-10-04",
    },
    {
        "id": "V-003",
        "name": "Toyota Altis",
        "license": "1กพ8782 กทม",
        "createdDate": "2025-11-21",
        "insuranceExpiryDate": "2026-11-22",
    },
]

V1, V2, V3 = "V-001", "V-002", "V-003"


def mazda_logs() -> list[dict[str, Any]]:
    return [
        log(
            "LOG-001",
            V1,
            be_date(30, 7, 2567),
            "อู่ติดแก๊ส",
            "CAT-005",
            27900,
            112059,
            alert_km_offset(112059, 132059),
        ),
        log("LOG-002", V1, be_date(5, 8, 2567), "-", "CAT-005", 3000),
        log(
            "LOG-003",
            V1,
            be_date(8, 8, 2567),
            "อู่ซ่อม",
            "CAT-011",
            5920,
            112350,
            shop_note="สายพาน, น้ำยาหม้อน้ำ, หม้อน้ำ, ค่าแรง",
        ),
        log("LOG-004", V1, be_date(7, 8, 2567), "-", "CAT-005", 6500, shop_note="กล่อง TAP LPG"),
        log(
            "LOG-005",
            V1,
            be_date(4, 10, 2568),
            "ตรอ/ภาษี",
            "CAT-006",
            1432,
            alert_month=11,
            shop_note="ตรอ+ภาษี+ตรวจแก๊ส+ฝากต่อ",
        ),
        log(
            "LOG-006",
            V1,
            year_date(2568, 3, 1),
            "-",
            "CAT-003",
            4800,
            alert_km=0,
            shop_note="ยางใหม่ 4 ล้อ (rotate 135000 km)",
        ),
        log(
            "LOG-007",
            V1,
            be_date(17, 4, 2568),
            "อู่ซ่อม",
            "CAT-001",
            3950,
            117000,
            alert_km_offset(117000, 127000),
            shop_note="ลูกปืนล้อหน้าซ้าย + น้ำมันเครื่อง",
        ),
        log(
            "LOG-008",
            V1,
            be_date(1, 8, 2568),
            "ประกันภัย",
            "CAT-007",
            7514.61,
            alert_month=12,
            shop_note="ต่อประกัน",
        ),
        log(
            "LOG-009",
            V1,
            year_date(2568, 2, 10),
            "อู่ซ่อม",
            "CAT-011",
            11282,
            111000,
            shop_note="Major service: ฝาหม้อน้ำ, ปั๊มน้ำ, thermostat, หัวเทียน, น้ำยาหม้อน้ำ, จอ Android, กรองอากาศ, ล้างหัวฉีด",
        ),
        log(
            "LOG-010",
            V1,
            year_date(2568, 5, 20),
            "อู่แอร์",
            "CAT-009",
            6200,
            shop_note="AC: condenser, O-ring, พัดลมหม้อน้ำ, vacuum+เติมแอร์",
        ),
        log("LOG-011", V1, be_date(8, 11, 2568), "ร้านติดฟิล์ม", "CAT-013", 2300, shop_note="ติดฟิล์ม 60%"),
        log("LOG-012", V1, be_date(15, 11, 2568), "อู่ซ่อม", "CAT-001", 1500, 124686, shop_note="เปลี่ยนน้ำมันเกียร์"),
        log("LOG-013", V1, be_date(15, 11, 2568), "-", "-", 0, 124686, ltype="Odometer_Update"),
    ]


def click_logs() -> list[dict[str, Any]]:
    return [
        log(
            "LOG-101",
            V2,
            be_date(4, 10, 2568),
            "ตรอ/ภาษี",
            "CAT-006",
            690,
            alert_month=12,
            shop_note="พรบ+ภาษี+ฝากต่อ",
        ),
        log(
            "LOG-102",
            V2,
            be_date(9, 11, 2568),
            "อู่ซ่อม",
            "CAT-001",
            450,
            21248,
            alert_km_offset(21248, 24248),
            shop_note="Eneos oil + Motul gear + ค่าแรง",
        ),
        log(
            "LOG-103",
            V2,
            be_date(17, 1, 2569),
            "อู่ซ่อม",
            "CAT-003",
            1250,
            23740,
            shop_note="IRC ยางหน้า + น้ำยาหม้อน้ำ",
        ),
        log(
            "LOG-104",
            V2,
            be_date(25, 1, 2569),
            "อู่ซ่อม",
            "CAT-001",
            979,
            shop_note="น้ำมันเครื่อง x3, injector, gear oil, flushing, bolts",
        ),
        log(
            "LOG-105",
            V2,
            be_date(1, 2, 2569),
            "อู่ซ่อม",
            "CAT-001",
            450,
            24202,
            shop_note="เปลี่ยนน้ำมัน+flushing",
        ),
        log("LOG-106", V2, be_date(31, 5, 2569), "อู่ซ่อม", "CAT-002", 272, 26571, shop_note="ผ้าเบรกหน้า"),
        log(
            "LOG-107",
            V2,
            be_date(6, 6, 2569),
            "Shopee DIY",
            "CAT-001",
            350,
            26679,
            alert_km_offset(26679, 29679),
            shop_note="เปลี่ยนน้ำมัน Shopee DIY",
        ),
        log("LOG-108", V2, be_date(6, 6, 2569), "-", "-", 0, 26679, ltype="Odometer_Update"),
    ]


def altis_logs() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    n = 200

    def add(shop, cat, cost, date, odo=0, alert_km=0, alert_month=0, note=""):
        nonlocal n
        n += 1
        entries.append(
            log(
                f"LOG-{n}",
                V3,
                date,
                shop,
                cat,
                cost,
                odo,
                alert_km,
                alert_month,
                shop_note=note,
            )
        )

    # Image 1 — maintenance
    add("สงขลา", "CAT-001", 1839, be_date(14, 4, 2569), 229726, alert_km_offset(229726, 244726))
    add("ซอยชินเขต", "CAT-001", 2150, be_date(21, 11, 2568), 220669, alert_km_offset(220669, 230669))
    add("ซอยชินเขต", "CAT-001", 171, be_date(21, 11, 2568), 220669, note="กรองแอร์+กรองอากาศ")

    # K.P. Phaisan major overhaul 24/11/2568
    kp_date = be_date(24, 11, 2568)
    kp_odo = 220770
    kp_alert = alert_km_offset(kp_odo, 320770)
    kp_items = [
        ("Shopee", "CAT-012", 268, "thermostat ต่ำ"),
        ("Shopee", "CAT-012", 883, "มอเตอร์พัดลม"),
        ("Shopee", "CAT-012", 1400, "หม้อน้ำ"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-011", 5500, "ยางแท่นเครื่อง"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-004", 4500, "เกียร์ซ่อมรั่ว"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-001", 3000, "น้ำมันเกียร์+กรอง+ปะกัน"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-003", 3000, "ลูกปืนล้อหน้า Koyo x2"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-011", 1100, "ล้างลิ้นปีกผี+กรองปั๊มน้ำมัน"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-004", 4500, "rack พวงมาลัยไฟฟ้า+ยาง stabilizer"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-010", 1400, "ลูกหมากคานหน้า L/R"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-010", 1500, "ลูกหมากล่าง x2"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-010", 1400, "ลิงก์ stabilizer x2"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-010", 1600, "บushing คานใหญ่ x2"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-010", 1000, "ค่าแรง rack+ช่วงล่าง"),
        ("เค.พี. ไพศาลยางยนต์", "CAT-012", 1000, "ค่าแรงปั๊มน้ำ+ท่อ+พัดลม"),
    ]
    for shop, cat, cost, note in kp_items:
        ak = kp_alert if note.startswith("ค่าแรงปั๊ม") else 0
        add(shop, cat, cost, kp_date, kp_odo, ak, note=note)
    add("Shopee", "CAT-011", 90, kp_date, kp_odo, note="ฝาน้ำมันเครื่อง")

    # Accessories 24/11/2568
    acc_date = be_date(24, 11, 2568)
    for cost, note in [
        (453, "พรม dashboard"),
        (2334, "จอ Android"),
        (1200, "กล้องถอยหลัง"),
        (112, "กรอบป้ายทะเบียน"),
        (212, "พวงมาลัย custom"),
        (47, "สติ๊กเกอร์ GR"),
        (148, "หลอด LED"),
        (45, "ปากกาแต้มสี"),
        (871, "พรมรถ"),
        (211, "ปลอกเข็มขัด"),
        (971, "ลายไม้แขนเกียร์"),
        (279, "ฝาเกียร์สแตนเลส"),
        (578, "ไฟหน้า LED"),
    ]:
        add("Shopee/ของแต่ง", "CAT-008", cost, acc_date, note=note)

    add("Shopee/ของแต่ง", "CAT-008", 211, be_date(3, 12, 2568), note="ปลอกเข็มขัด")
    add("Shopee/ของแต่ง", "CAT-008", 871, be_date(3, 12, 2568), note="ถาดพื้นยาง")
    add("Shopee/ของแต่ง", "CAT-008", 1252, be_date(3, 12, 2568), note="OBD2 Reader")
    add("Shopee/ของแต่ง", "CAT-008", 65, be_date(10, 12, 2568), note="กระจกปรับมองข้าง")
    add("Shopee/ของแต่ง", "CAT-008", 69, be_date(10, 12, 2568), note="หลอดไฟแอร์")
    add(
        "ช่างเดียวในกลุ่ม altis",
        "CAT-008",
        3100,
        be_date(14, 12, 2568),
        note="ปุ่มพวงมาลัย+Cruise control",
    )

    # Image 2 — LPG 27/11/2568
    lpg_date = be_date(27, 11, 2568)
    lpg_odo = 220822
    lpg_alert = alert_km_offset(lpg_odo, 260822)
    for cost, note in [
        (60, "ใส่บูทเกียร์ Shopee"),
        (2000, "เปลี่ยนหัวเทียน"),
        (800, "เปลี่ยนปลั๊กหัวฉีด"),
        (22900, "ติดตั้ง LPG KME NEVOJET ECO"),
        (1000, "กรองแก๊ส Ultra 360"),
        (4500, "กล่องปรับ ATD"),
        (800, "ตัดน้ำมัน"),
    ]:
        ak = lpg_alert if "LPG KME" in note else 0
        add("โชคดีแก๊สคาร์เซอร์วิส", "CAT-005", cost, lpg_date, lpg_odo, ak, note=note)

    # Insurance
    add(
        "insurereverse",
        "CAT-007",
        12459.08,
        year_date(2568, 11, 1),
        alert_month=12,
        note="ประกันภัย",
    )

    # Hia Dee VCA 8/12/2568
    hd_date = be_date(8, 12, 2568)
    hd_items = [
        (3800, "เบ้าโช้คแท้ x2"),
        (100, "โฟมรองเบ้าโช้ค"),
        (500, "ยางรองสปริงบนหน้า"),
        (700, "ยางกันกระแทกโช้ค"),
        (200, "ยางรองสปริงล่างหน้า"),
        (1200, "ผ้าเบรคหน้า OEM"),
        (400, "เจียรจานเบรค"),
        (7400, "โช้คอัพหน้า/หลังแท้"),
        (200, "ยางรองสปริงบนหลัง"),
        (500, "สายพานหน้าเครื่อง"),
        (400, "ล้างลิ้นปีกผี+แอร์โฟลว"),
        (1500, "ค่าแรง"),
    ]
    for cost, note in hd_items:
        cat = "CAT-002" if "เบรค" in note or "จาน" in note else "CAT-010"
        if "สายพาน" in note:
            cat = "CAT-011"
        if "ล้าง" in note:
            cat = "CAT-011"
        add("เฮียดี วีซีเอ", cat, cost, hd_date, note=note)

    # Shopee parts 8/12/2568
    sp_date = be_date(8, 12, 2568)
    sp_odo = 222599
    sp_alert = alert_km_offset(sp_odo, 322599)
    sp_items = [
        (1000, "ค่าแรงยก rack+ช่วงล่าง"),
        (400, "ตั้งศูนย์"),
        (2500, "บูทคานหลัง ซ/ข"),
        (1300, "ปั๊มน้ำ Aisin"),
        (550, "ท่อน้ำแท้"),
        (1077, "คอยล์ Denso x1"),
        (3231, "คอยล์ Denso x3"),
        (190, "ฝาหม้อน้ำ"),
    ]
    for cost, note in sp_items:
        ak = sp_alert if "ค่าแรงยก" in note else 0
        cat = "CAT-010" if any(x in note for x in ("rack", "บูท", "ตั้งศูนย์")) else "CAT-012"
        add("Shopee", cat, cost, sp_date, sp_odo, ak, note=note)

    entries.append(log("LOG-299", V3, be_date(14, 4, 2569), "-", "-", 0, 229726, ltype="Odometer_Update"))
    return entries


def build_maintenance_logs() -> list[dict[str, Any]]:
    return mazda_logs() + click_logs() + altis_logs()


ALERTS = [
    {
        "vehicleId": V1,
        "targetKm": 132059,
        "targetDate": "2026-08-25",
        "status": "Active",
        "lastUpdated": be_date(15, 11, 2568),
        "serviceLabel": "แก๊ส/LPG",
        "categoryId": "CAT-005",
    },
    {
        "vehicleId": V2,
        "targetKm": 29679,
        "targetDate": "2026-10-04",
        "status": "Active",
        "lastUpdated": be_date(6, 6, 2569),
        "serviceLabel": "เปลี่ยนถ่ายน้ำมันเครื่อง/ของเหลว",
        "categoryId": "CAT-001",
    },
    {
        "vehicleId": V3,
        "targetKm": 244726,
        "targetDate": "2026-11-22",
        "status": "Active",
        "lastUpdated": be_date(14, 4, 2569),
        "serviceLabel": "เปลี่ยนถ่ายน้ำมันเครื่อง/ของเหลว",
        "categoryId": "CAT-001",
    },
]


def build_seed_state() -> dict[str, Any]:
    return {
        "vehicles": VEHICLES,
        "categories": CATEGORIES,
        "maintenanceLogs": build_maintenance_logs(),
        "fuelLogs": [],
        "alerts": ALERTS,
        "selectedVehicleId": V1,
        "adminAuthenticated": False,
        "lineLogs": [
            "🚀 MyHome CarCare v2.1 — ข้อมูลรถจริง 3 คัน (Mazda, Click 160, Altis)",
            "📡 โฟลเดอร์ใบเสร็จ Google Drive: 1O_L7QryZNzdnzzisWI76bzW269RzhRyd",
        ],
    }


def render_state_js(indent: str = "            ") -> str:
    """Render JavaScript object literal for embedding in index.html."""
    state = build_seed_state()
    lines = ["let state = {"]
    for key, value in state.items():
        if key == "maintenanceLogs":
            lines.append(f'{indent}maintenanceLogs: [')
            for entry in value:
                lines.append(f"{indent}    {json.dumps(entry, ensure_ascii=False)},")
            lines.append(f"{indent}],")
        elif key == "fuelLogs":
            lines.append(f"{indent}fuelLogs: [],")
        elif key == "lineLogs":
            lines.append(f"{indent}lineLogs: [")
            for msg in value:
                lines.append(f'{indent}    "{msg}",')
            lines.append(f"{indent}],")
        else:
            dumped = json.dumps(value, ensure_ascii=False, indent=4)
            inner = "\n".join(indent + line for line in dumped.splitlines())
            lines.append(f"{indent}{key}: {inner.lstrip()},")
    lines.append("        };")
    return "\n".join(lines)


SEED_DATA = build_seed_state()

if __name__ == "__main__":
    print(render_state_js())

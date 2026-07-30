"""Generate gas/SeedData.gs from tools/seed_data.py (family vehicles)."""
from __future__ import annotations

import json
import os

from seed_data import build_seed_state

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "gas", "SeedData.gs")


def main() -> None:
    state = build_seed_state()
    payload = json.dumps(state, ensure_ascii=False, separators=(",", ":"))
    content = f"""/**
 * Family seed data generated from tools/seed_data.py — do not edit by hand.
 * Regenerate: python tools/generate_gas_seed.py
 */
var FAMILY_SEED_JSON_ = {json.dumps(payload)};

function getFamilySeedState_() {{
  return JSON.parse(FAMILY_SEED_JSON_);
}}

/** Wipe data sheets and import Mazda / Click / Altis seed (keeps Settings). */
function importFamilySeedData() {{
  try {{
    var ss = getSpreadsheet_();
    ensureSheets_(ss);
    clearDataSheets_(ss);
    writeFullStateToSheets_(getFamilySeedState_());
    invalidateExecCache_();
    return {{
      success: true,
      spreadsheetId: ss.getId(),
      spreadsheetUrl: ss.getUrl(),
      message: 'นำเข้าข้อมูลรถจริง 3 คัน (Mazda, Click 160, Altis) สำเร็จ',
      state: getFullSyncState_(null)
    }};
  }} catch (e) {{
    return {{ success: false, error: String(e.message || e) }};
  }}
}}

function clearDataSheets_(ss) {{
  [SHEET_NAMES.VEHICLES, SHEET_NAMES.CATEGORIES, SHEET_NAMES.MAINTENANCE,
   SHEET_NAMES.FUEL, SHEET_NAMES.ALERTS].forEach(function (name) {{
    var sheet = ss.getSheetByName(name);
    if (!sheet) return;
    var last = sheet.getLastRow();
    if (last > 1) sheet.getRange(2, 1, last - 1, sheet.getLastColumn()).clearContent();
    // clearContent above uses wrong row count when last>1 — delete rows instead
  }});
  [SHEET_NAMES.VEHICLES, SHEET_NAMES.CATEGORIES, SHEET_NAMES.MAINTENANCE,
   SHEET_NAMES.FUEL, SHEET_NAMES.ALERTS].forEach(function (name) {{
    var sheet = ss.getSheetByName(name);
    if (!sheet) return;
    var last = sheet.getLastRow();
    if (last >= 2) sheet.deleteRows(2, last - 1);
  }});
}}

function writeFullStateToSheets_(state) {{
  state = state || {{}};
  (state.vehicles || []).forEach(function (v) {{
    upsertRow_(SHEET_NAMES.VEHICLES, 'vehicleId', v.id, {{
      vehicleId: v.id,
      'ชื่อ': v.name,
      'ทะเบียน': v.license,
      'สร้างเมื่อ': v.createdDate || getBangkokToday_(),
      prbExpiryDate: v.prbExpiryDate || '',
      insuranceExpiryDate: v.insuranceExpiryDate || ''
    }});
  }});
  (state.categories || []).forEach(function (c) {{
    upsertRow_(SHEET_NAMES.CATEGORIES, 'categoryId', c.id, {{
      categoryId: c.id,
      'ชื่อ': c.name
    }});
  }});
  (state.maintenanceLogs || []).forEach(function (l) {{
    upsertRow_(SHEET_NAMES.MAINTENANCE, 'logId', l.id, {{
      logId: l.id,
      vehicleId: l.vehicleId,
      'วันที่': l.date || getBangkokToday_(),
      categoryId: l.category || '-',
      'ร้าน': l.shop || '-',
      'ราคา': num_(l.cost),
      'ไมล์': num_(l.odo),
      type: l.type || 'Maintenance',
      alertKm: num_(l.alertKm),
      alertMonth: num_(l.alertMonth),
      driveFileId: l.driveFileId || '',
      driveUrl: l.fileLink || '',
      receiptName: l.receipt || ''
    }});
  }});
  (state.fuelLogs || []).forEach(function (l) {{
    upsertRow_(SHEET_NAMES.FUEL, 'logId', l.id, {{
      logId: l.id,
      vehicleId: l.vehicleId,
      'วันที่': l.date || getBangkokToday_(),
      fuelType: l.fuelType || 'oil',
      'ไมล์': num_(l.odo),
      'ลิตร': num_(l.liters),
      'ราคา/ลิตร': num_(l.pricePerLiter),
      'ราคารวม': num_(l.totalCost),
      'เต็มถัง': l.fullTank ? 'TRUE' : 'FALSE',
      'สถานี': l.station || ''
    }});
  }});
  (state.alerts || []).forEach(function (a, idx) {{
    var alertId = a.alertId || ('ALERT-' + (idx + 1));
    upsertRow_(SHEET_NAMES.ALERTS, 'alertId', alertId, {{
      alertId: alertId,
      vehicleId: a.vehicleId,
      targetKm: num_(a.targetKm),
      targetDate: a.targetDate || '',
      status: a.status || 'Active',
      lastUpdated: a.lastUpdated || getBangkokToday_(),
      serviceLabel: a.serviceLabel || '',
      categoryId: a.categoryId || ''
    }});
  }});
  if (Array.isArray(state.lineLogs) && state.lineLogs.length) {{
    setScriptProp_(CONFIG.LINE_LOGS_PROP, JSON.stringify(state.lineLogs));
  }}
}}
"""
    # Fix clearDataSheets_ - the first loop is buggy/redundant. Rewrite cleaner.
    content = f"""/**
 * Family seed data generated from tools/seed_data.py — do not edit by hand.
 * Regenerate: python tools/generate_gas_seed.py
 */
var FAMILY_SEED_JSON_ = {json.dumps(payload)};

function getFamilySeedState_() {{
  return JSON.parse(FAMILY_SEED_JSON_);
}}

/** Wipe data sheets and import Mazda / Click / Altis seed (keeps Settings). */
function importFamilySeedData() {{
  try {{
    var ss = getSpreadsheet_();
    ensureSheets_(ss);
    clearDataSheets_(ss);
    writeFullStateToSheets_(getFamilySeedState_());
    invalidateExecCache_();
    return {{
      success: true,
      spreadsheetId: ss.getId(),
      spreadsheetUrl: ss.getUrl(),
      message: 'นำเข้าข้อมูลรถจริง 3 คัน (Mazda, Click 160, Altis) สำเร็จ',
      counts: {{
        vehicles: (getFamilySeedState_().vehicles || []).length,
        categories: (getFamilySeedState_().categories || []).length,
        maintenanceLogs: (getFamilySeedState_().maintenanceLogs || []).length,
        fuelLogs: (getFamilySeedState_().fuelLogs || []).length,
        alerts: (getFamilySeedState_().alerts || []).length
      }},
      state: getFullSyncState_(null)
    }};
  }} catch (e) {{
    return {{ success: false, error: String(e.message || e) }};
  }}
}}

function clearDataSheets_(ss) {{
  [SHEET_NAMES.VEHICLES, SHEET_NAMES.CATEGORIES, SHEET_NAMES.MAINTENANCE,
   SHEET_NAMES.FUEL, SHEET_NAMES.ALERTS].forEach(function (name) {{
    var sheet = ss.getSheetByName(name);
    if (!sheet) return;
    var last = sheet.getLastRow();
    if (last >= 2) {{
      sheet.deleteRows(2, last - 1);
    }}
  }});
}}

function writeFullStateToSheets_(state) {{
  state = state || {{}};
  (state.vehicles || []).forEach(function (v) {{
    upsertRow_(SHEET_NAMES.VEHICLES, 'vehicleId', v.id, {{
      vehicleId: v.id,
      'ชื่อ': v.name,
      'ทะเบียน': v.license,
      'สร้างเมื่อ': v.createdDate || getBangkokToday_(),
      prbExpiryDate: v.prbExpiryDate || '',
      insuranceExpiryDate: v.insuranceExpiryDate || ''
    }});
  }});
  (state.categories || []).forEach(function (c) {{
    upsertRow_(SHEET_NAMES.CATEGORIES, 'categoryId', c.id, {{
      categoryId: c.id,
      'ชื่อ': c.name
    }});
  }});
  (state.maintenanceLogs || []).forEach(function (l) {{
    upsertRow_(SHEET_NAMES.MAINTENANCE, 'logId', l.id, {{
      logId: l.id,
      vehicleId: l.vehicleId,
      'วันที่': l.date || getBangkokToday_(),
      categoryId: l.category || '-',
      'ร้าน': l.shop || '-',
      'ราคา': num_(l.cost),
      'ไมล์': num_(l.odo),
      type: l.type || 'Maintenance',
      alertKm: num_(l.alertKm),
      alertMonth: num_(l.alertMonth),
      driveFileId: l.driveFileId || '',
      driveUrl: l.fileLink || '',
      receiptName: l.receipt || ''
    }});
  }});
  (state.fuelLogs || []).forEach(function (l) {{
    upsertRow_(SHEET_NAMES.FUEL, 'logId', l.id, {{
      logId: l.id,
      vehicleId: l.vehicleId,
      'วันที่': l.date || getBangkokToday_(),
      fuelType: l.fuelType || 'oil',
      'ไมล์': num_(l.odo),
      'ลิตร': num_(l.liters),
      'ราคา/ลิตร': num_(l.pricePerLiter),
      'ราคารวม': num_(l.totalCost),
      'เต็มถัง': l.fullTank ? 'TRUE' : 'FALSE',
      'สถานี': l.station || ''
    }});
  }});
  (state.alerts || []).forEach(function (a, idx) {{
    var alertId = a.alertId || ('ALERT-' + (idx + 1));
    upsertRow_(SHEET_NAMES.ALERTS, 'alertId', alertId, {{
      alertId: alertId,
      vehicleId: a.vehicleId,
      targetKm: num_(a.targetKm),
      targetDate: a.targetDate || '',
      status: a.status || 'Active',
      lastUpdated: a.lastUpdated || getBangkokToday_(),
      serviceLabel: a.serviceLabel || '',
      categoryId: a.categoryId || ''
    }});
  }});
  if (Array.isArray(state.lineLogs) && state.lineLogs.length) {{
    setScriptProp_(CONFIG.LINE_LOGS_PROP, JSON.stringify(state.lineLogs));
  }}
}}
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()

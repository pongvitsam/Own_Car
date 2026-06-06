/**
 * MyHome CarCare - Configuration & Script Properties
 */
var CONFIG = {
  DRIVE_FOLDER_ID: '1R-dpki8-nS17XAma6tyiQMEH66kEcf7U',
  DEFAULT_ADMIN_PASS: '1234',
  SPREADSHEET_PROP: 'SPREADSHEET_ID',
  LINE_TOKEN_PROP: 'LINE_NOTIFY_TOKEN',
  LINE_LOGS_PROP: 'LINE_LOGS_JSON',
  ADMIN_PASS_PROP: 'ADMIN_PASS',
  TIMEZONE: 'Asia/Bangkok'
};

var SHEET_NAMES = {
  VEHICLES: 'รถ',
  CATEGORIES: 'หมวดซ่อม',
  MAINTENANCE: 'บันทึกซ่อม',
  FUEL: 'เติมเชื้อเพลิง',
  ALERTS: 'แจ้งเตือน',
  SETTINGS: 'ตั้งค่า'
};

function getScriptProp_(key) {
  return getScriptPropCached_(key);
}

function setScriptProp_(key, value) {
  clearScriptPropCache_(key);
  PropertiesService.getScriptProperties().setProperty(key, String(value));
}

function getAdminPass_() {
  return getScriptProp_(CONFIG.ADMIN_PASS_PROP) || CONFIG.DEFAULT_ADMIN_PASS;
}

function getLineNotifyToken_() {
  return getScriptProp_(CONFIG.LINE_TOKEN_PROP) || '';
}

function isLineNotifyConfigured_() {
  return getLineNotifyToken_().trim().length > 0;
}

function getBangkokNow_() {
  return Utilities.formatDate(new Date(), CONFIG.TIMEZONE, 'yyyy-MM-dd HH:mm:ss');
}

function getBangkokToday_() {
  return Utilities.formatDate(new Date(), CONFIG.TIMEZONE, 'yyyy-MM-dd');
}

function generateId_(prefix) {
  return prefix + '-' + new Date().getTime();
}

function appendLineLog_(message) {
  var logs = getLineLogs_();
  logs.push('[' + getBangkokNow_() + '] ' + message);
  if (logs.length > 100) {
    logs = logs.slice(logs.length - 100);
  }
  setScriptProp_(CONFIG.LINE_LOGS_PROP, JSON.stringify(logs));
  return logs;
}

function getLineLogs_() {
  var raw = getScriptProp_(CONFIG.LINE_LOGS_PROP);
  if (!raw) {
    return [
      '🚀 [' + getBangkokNow_() + '] Line API Simulator เริ่มต้นการเชื่อมต่อ...',
      '📡 [' + getBangkokNow_() + '] ค้นพบโฟลเดอร์ Google Drive: ' + CONFIG.DRIVE_FOLDER_ID
    ];
  }
  try {
    return JSON.parse(raw);
  } catch (e) {
    return [];
  }
}

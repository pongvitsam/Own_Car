/** Admin vehicle edit — delegates to Vehicles.gs updateVehicle */
function updateVehicleAdmin(data) {
  return updateVehicle(data);
}

function verifyAdmin(credentials) {
  var user = '';
  var pass = '';
  if (credentials && typeof credentials === 'object') {
    user = String(credentials.username || '').trim();
    pass = String(credentials.password || '');
  } else {
    pass = String(credentials || '');
    user = CONFIG.DEFAULT_ADMIN_USER;
  }
  var expectedPass = String(getAdminPass_());
  if (!expectedPass) {
    return {
      success: true,
      authenticated: false,
      message: 'ยังไม่ได้ตั้งรหัสผ่านแอดมิน (รัน setAdminCredentials ใน Apps Script)'
    };
  }
  var valid = user === String(getAdminUser_()) && pass === expectedPass;
  return {
    success: true,
    authenticated: valid,
    message: valid ? 'ยืนยันแอดมินสำเร็จ' : 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
  };
}

/**
 * Owner-only: run once from the Apps Script editor, e.g.
 *   setAdminCredentials('admin', 'your-strong-password')
 * Stored in Script Properties (never in the Sheet or the repo).
 */
function setAdminCredentials(username, password) {
  if (!password || String(password).length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  setScriptProp_(CONFIG.ADMIN_USER_PROP, String(username || CONFIG.DEFAULT_ADMIN_USER));
  setScriptProp_(CONFIG.ADMIN_PASS_PROP, String(password));
}

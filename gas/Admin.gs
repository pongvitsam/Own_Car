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
  var valid = user === String(getAdminUser_()) && pass === String(getAdminPass_());
  return {
    success: true,
    authenticated: valid,
    message: valid ? 'ยืนยันแอดมินสำเร็จ' : 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง! (admin / 1234)'
  };
}

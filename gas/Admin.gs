function verifyAdmin(passcode) {
  var valid = String(passcode) === String(getAdminPass_());
  return {
    success: true,
    authenticated: valid,
    message: valid ? 'ยืนยันแอดมินสำเร็จ' : 'รหัสผ่านไม่ถูกต้อง! ลองใส่ 1234'
  };
}

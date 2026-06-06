function sendLineNotify_(message) {
  var token = getLineNotifyToken_();
  if (!token) {
    return { success: false, simulated: true, message: message };
  }

  try {
    var response = UrlFetchApp.fetch('https://notify-api.line.me/api/notify', {
      method: 'post',
      headers: {
        Authorization: 'Bearer ' + token
      },
      payload: {
        message: message
      },
      muteHttpExceptions: true
    });

    var code = response.getResponseCode();
    if (code >= 200 && code < 300) {
      return { success: true, status: code };
    }
    return {
      success: false,
      status: code,
      body: response.getContentText()
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

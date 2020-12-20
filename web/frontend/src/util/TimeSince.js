export default function TimeSince(date) {
    var seconds = Math.floor((new Date() - date) / 1000);
    var out = ""
    var interval = Math.floor(seconds / 31536000);
    
    if (interval >= 1) {
      out = interval + " year";
      if(interval > 1) {
        out += "s";
      }
      return out
    }
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) {
      out = interval + " month";
      if(interval > 1) {
        out += "s";
      }
      return out
    }
    interval = Math.floor(seconds / 86400);
    if (interval >= 1) {
      out = interval + " day";
      if(interval > 1) {
        out += "s";
      }
      return out
    }
    interval = Math.floor(seconds / 3600);
    if (interval >= 1) {
      out = interval + " hour";
      if(interval > 1) {
        out += "s";
      }
      return out
    }
    interval = Math.floor(seconds / 60);
    if (interval >= 1) {
      out = interval + " minute";
      if(interval > 1) {
        out += "s";
      }
      return out
    }
    
    if(isNaN(seconds)) {
      return false;
    }
  
    return Math.floor(seconds) + " seconds";
  }
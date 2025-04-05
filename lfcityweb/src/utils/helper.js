const digit2 = (number)=>{
  number = Math.floor(number).toString();
  if(number.length === 1) number = '0' + number;
  return number;
}

const format_date = (seconds)=>{
  let day = seconds / (24 * 60 * 60);
  let hour = (seconds % (24 * 60 * 60)) / (60 * 60);
  let minute = (seconds % (60 * 60)) / 60;
  let second = seconds % 60;

  return `${digit2(day)}天${digit2(hour)}时${digit2(minute)}分${digit2(second)}秒`;
}

const format_duration = (seconds)=>{
    let hours = seconds / (60 * 60);
    let minutes = (seconds % (60 * 60)) / 60;
    let second = seconds % 60;
    return `${parseInt(hours)}小时${digit2(minutes)}分${digit2(second)}秒`;
}

export {format_date, format_duration, digit2};
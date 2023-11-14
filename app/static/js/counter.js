function incrementCounter(id){
    let count = document.getElementById('counter'+String(id)).innerText;
    count++;
    document.getElementById('counter'+String(id)).innerText = count;
  }
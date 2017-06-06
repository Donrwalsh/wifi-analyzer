/**
*Stores the plaintext of all emails within a given label.
*/

function processLabel() {
  //Environmental Variables
  var folder_id = '';
  var label_name = "";
  
  var folder = DriveApp.getFolderById(folder_id);
      label = GmailApp.getUserLabelByName(label_name),
      threads = label.getThreads();
  for (var i = 0; i < threads.length; i++) {
    var date = threads[i].getLastMessageDate(),
        datestring = Utilities.formatDate(date, "GMT", "MM-dd HH:mm"),
        subject = threads[i].getFirstMessageSubject(),
        building = subject.split(' ').slice(0, 1).join(' ')
        name = building + ' ' + datestring
        exists = folder.getFilesByName(name);    
        messages = threads[i].getMessages();
   for (var j = 0; j < messages.length; j++) {
     var rawmsg = messages[j].getPlainBody().slice(0, -91);
     if(!exists.hasNext()){
      folder.createFile(name, rawmsg, MimeType.PLAIN_TEXT);
     }
   }
  }
function decode_rot16(input_string) {
    var decoded = '';
    for (var i = 0; i < input_string.length; i++) {
        var char = input_string.charAt(i);
        if ('a' <= char && char <= 'z') {
            decoded += String.fromCharCode(((char.charCodeAt(0) - 'a'.charCodeAt(0) - 16 + 26) % 26) + 'a'.charCodeAt(0));
        } else if ('A' <= char && char <= 'Z') {
            decoded += String.fromCharCode(((char.charCodeAt(0) - 'A'.charCodeAt(0) - 16 + 26) % 26) + 'A'.charCodeAt(0));
        } else {
            decoded += char;
        }
    }
    return decoded;
}


// This method is called to process the response
function responseReceived(msg, initiator, helper) {
    // Get the response body as a string
    var response_body = msg.getResponseBody().toString();
    if (response_body[0] != '<') return;
    // Decode the body from ROT16
    var decoded_body = decode_rot16(response_body);
    
    // Update the response with the decoded body
    msg.setResponseBody(decoded_body);
}
function sendingRequest(msg, initiator, helper) {
}
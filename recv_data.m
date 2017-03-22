% function recv_data(sock)
while 1
    bytesAvailable = sock.BytesAvailable;
%         fprintf('%d Bytes Available in Buffer\n', bytesAvailable);
    if bytesAvailable > 0
        echo_msg = read(sock, 2);
        fprintf('echo_msg is %x\n', echo_msg);
    end
end
% end
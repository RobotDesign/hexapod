slCharacterEncoding('UTF-8');
SERVER_HOST = '127.0.0.1';
PORT = 9000;
sock = tcpclient(SERVER_HOST, PORT);

fprintf('\n\n<<<<<<<<< --------  Welcome to the LattePanda Client  --------- >>>>>>>>>\n\n');
answer = input('Would you like to start up the Server? (Y/N): ', 's');
if answer == 'Y'
    start_freq = input('Enter a data transmission frequency (Hz) between 1 and 50: ');
    while (start_freq < 1) || (start_freq > 50) || isstring(start_freq)
        start_freq = input('Try Again: Enter a data transmission frequency (Hz) between 1 and 50: ');
    end
    data = pkg_freq(start_freq);
    % send initial frequency setting
    write(sock, data);
    fprintf('Ready to receive messages from LattePanda w/ IP %s on Port %d at %d Hz\n',SERVER_HOST, PORT, start_freq);
else
    return; %% exit the program
end

% j = batch(recv_data, 0, {sock})
disp('Waiting on data from the server...')
recv_data(sock)
% send loop
% while 1
%     disp('start loop')
%     set_freq = input('PRESS Y TO RESET THE DATA TRANSMISSION RATE OR STOP TRANSMISSION:', 's');
%     if set_freq == 'Y'
%         get_send_freq(sock)
%     elseif set_freq == 'N'
%         return; %% exit the program
%     end
      
%     pause(1)
% end
disp('gone past read loop');
clear sock

function pkg = pkg_freq(f)
    cmnd_type = 1;
    if f == 0
        cmnd_type = 255;
    end
    pkg = uint8([cmnd_type, f]);
    fprintf('pkg is %x\n', pkg);
end

function recv_data(sock)
    while 1
        bytesAvailable = sock.BytesAvailable;
    %         fprintf('%d Bytes Available in Buffer\n', bytesAvailable);
        if bytesAvailable > 0
            echo_msg = read(sock, 2);
            fprintf('echo_msg is %x\n', echo_msg);
        end
    end
end


function get_send_freq(sock)
    freq = input('Enter a data transmission frequency (Hz) between 1 and 50: ');
    while (freq < 1) || (freq > 50) || isstring(freq)
        freq = input('Try Again: Enter a data receive frequency between 1 and 50: ');
    end
    data = pkg_freq(freq);
    % send frequency setting
    write(sock, data);
    fprintf('Changed data receive frequency to %d', freq)

end
slCharacterEncoding('UTF-8');
SERVER_HOST = '127.0.0.1';
PORT = 9000;
sock = tcpip(SERVER_HOST, PORT, 'NetworkRole', 'Client');
sock.InputBufferSize = 65536;
fopen(sock);

fprintf('\n\n<<<<<<<<< --------  Welcome to the LattePanda Client  --------- >>>>>>>>>\n\n');
answer = input('Would you like to Start or Stop data transmission from the Server? (Y/N): ', 's');
if answer == 'Y'
    start_freq = input('Enter a data transmission frequency (Hz) between 1 and 50: ');
    while (start_freq < 1) || (start_freq > 50) || isstring(start_freq)
        start_freq = input('Try Again: Enter a data transmission frequency (Hz) between 1 and 50: ');
    end
    data = pkg_freq(start_freq);
    % send initial frequency setting
    fwrite(sock, data);
    fprintf('Ready to receive messages from LattePanda w/ IP %s on Port %d at %d Hz\n',SERVER_HOST, PORT, start_freq);
elseif answer == 'N'
    data = pkg_freq(0); % send 0 as the data transmission frequency
    fwrite(sock, data)
    disp('Stopping data transmission from server')
    return; %% exit the program

else
    disp('Did not enter Y or N: try running program again')
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
    pkg_disp = sprintf('%x ', pkg);
    fprintf('pkg is %s\n', pkg_disp);
end

function recv_data(sock)
    while 1
%         bytesAvailable = sock.BytesAvailable;
        fprintf('%d Bytes Available in Buffer\n', sock.bytesAvailable);
        if sock.bytesAvailable > 0
            data = fread(sock, sock.bytesAvailable);
            arr=sprintf('%u ', data);
            fprintf('Data: %s\n', arr)
        end
        pause(1)
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
clc
clear

% ------ Read the data  -------
data0 = importdata('black2/analog00.csv');
data0 = data0.data;
[rows, columns] = size(data0);
equalize_coeff = sqrt(mean(sum(data0.^2, 2)));   % find Gravity amount

data0 = importdata('blue/analog00.csv');
data0 = data0.data;
[rows, columns] = size(data0);
equalize_coeff1 = sqrt(mean(sum(data0.^2, 2)));   % find Gravity amount

file0 = '04';
data0 = importdata(sprintf('black2/analog%s.csv', file0));
data0 = data0.data;
[rows, columns] = size(data0);

data1 = importdata(sprintf('blue/analog%s.csv', file0));
data1 = data1.data;
[rows1, columns1] = size(data1);

% ------ Equalize  -------
data0_equalized = sqrt(sum(data0.^2, 2)) / equalize_coeff * 10 - 10;
data1_equalized = sqrt(sum(data1.^2, 2)) / equalize_coeff1 * 10 - 10;

% ------ plots --------
% figure(1) 
% subplot(1, 2, 1)
% plot(data0_equalized)
% title(sprintf('data%s acceleration time plot', file0))
% ylabel('m/s^2')
% xlabel('samples')
% 
% subplot(1, 2, 2)
% Nx = length(data0_equalized);       % length of data
% nsc = floor(Nx/100);                % window of fft calculation
% nov = floor(nsc/2);                 % 50% window overlap (smoothing the spectogram)
% nff = max(256, 2^nextpow2(nsc));    % fft number of points
% 
% spectrogram(data0_equalized, hamming(nsc), nov, nff, 'yaxis');
% title(sprintf('data%s Spectogram', file0))

% ------ spectogram example -------
% figure(4) 
% x = 0:10000;
% data0_equalized = sin(1000 * x) + 10 * rand(size(x));
% disp(rand(size([1, 2])))
% plot(data0_equalized)
% figure(5) 
% 
% Nx = length(data0_equalized);       % length of data
% nsc = floor(Nx/100);                % window of fft calculation
% nov = floor(nsc/2);                 % 50% window overlap (smoothing the spectogram)
% nff = max(256, 2^nextpow2(nsc));    % fft number of points
% 
% spectrogram(data0_equalized, hamming(nsc), nov, nff, 'yaxis');
% title('spectogram example')

% ----- cross correlation spectogram plot -------
% figure(2)
% nwin = 100;                           % cross correlation window
% rows = min([rows, rows1]);
% disp(rows)
% xspectrogram(data0_equalized(1:rows), data1_equalized(1:rows), kaiser(nwin, 30), nwin - 1, [], ...
%     'power', 'MinThreshold', -40, 'yaxis')
% title(sprintf('Cross-Correlation Spectogram of data%s ', file0))

% ------- normalized cross correlation plot in time ----------
% rows = min([rows, rows1]);
% r_xy = xcorr(data0_equalized(1:rows), data1_equalized(1:rows));
% % r_xx = xcorr(data0_equalized(1:rows), data0_equalized(1:rows));
% % r_yy = xcorr(data1_equalized(1:rows), data1_equalized(1:rows));
% figure(1)
% % disp()
% plot(r_xy / min(r_xy))
% title(sprintf('normalized cross corrolation in times (data%s equal length)', file0))
% xlabel('t')

% -------- filtering the signals ------
% figure(2)
% fs = 1000;
% rows = min([rows, rows1]);
% out0 = bandpass(data0_equalized(1:rows),[20 150],fs);
% out1 = bandpass(data1_equalized(1:rows),[20 150],fs);
% r_xy = xcorr(out0, out1);
% plot(r_xy / min(r_xy))
% title(sprintf('filtered normalized cross corrolation in times (data%s equal length)', file0))
% xlabel('t')

% -------- phase vs freq --------
rows = min([rows, rows1]);
fft0 = fft(data0_equalized(1:rows), 1024, 1);
figure(3)
plot(linspace(0, 1000, numel(fft0(10:end - 10))), -1 * unwrap(atan2(imag(fft0(10:end - 10)), real(fft0(10:end - 10)))))
xlabel('freq (Hz)')
title(sprintf('phase Vs freq of (data%s)', file0))
ylabel('unwraped angle deg (degrees)')
ylim([0, 1300])
xlim([0, 1000])
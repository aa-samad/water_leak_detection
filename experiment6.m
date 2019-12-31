clc
clear

%% ------ Read the data  -------
data0 = importdata('blue/analog00.csv');
data0 = data0.data;
[rows, columns] = size(data0);
equalize_coeff = sqrt(mean(sum(data0.^2, 2)));   % find Gravity amount

data0 = importdata('purple/analog00.csv');
data0 = data0.data;
[rows, columns] = size(data0);
equalize_coeff1 = sqrt(mean(sum(data0.^2, 2)));   % find Gravity amount

file0 = '06';
data0 = importdata(sprintf('blue/analog%s.csv', file0));
data0 = data0.data;
[rows, columns] = size(data0);

data1 = importdata(sprintf('purple/analog%s.csv', file0));
data1 = data1.data;
[rows1, columns1] = size(data1);

%% ------ Equalize  -------
data0_equalized = sqrt(sum(data0.^2, 2)) / equalize_coeff * 10 - 10;
data0_equalized = data0_equalized - mean(data0_equalized);
data1_equalized = sqrt(sum(data1.^2, 2)) / equalize_coeff1 * 10 - 10;
data1_equalized = data1_equalized - mean(data1_equalized);

% --- upsample
% data0_equalized = resample(data0_equalized, 10, 1);
% rows = numel(data0_equalized) / 5;
% data0_equalized = data0_equalized(1:rows);
% data1_equalized = resample(data1_equalized, 10, 1);
% rows1 = numel(data1_equalized) / 5;
% data1_equalized = data1_equalized(1:rows1);

%% ------ time plot and spectogram --------
% figure(1) 
% subplot(1, 2, 1)
% plot(data0_equalized)
% title(sprintf('data%s-blueSens acceleration time plot', file0))
% ylabel('m/s^2')
% xlabel('samples')
% 
% subplot(1, 2, 2)
% Nx = length(data0_equalized);       % length of data
% nsc = floor(Nx/100);                % window of fft calculation
% nov = floor(nsc/2);                 % 50% window overlap (smoothing the spectogram)
% nff = max(512, 2^nextpow2(nsc));    % fft number of points
% 
% spectrogram(data0_equalized, hamming(nsc), nov, nff, 'MinThreshold',-70, 'yaxis');
% title(sprintf('data%s-blueSens Spectogram', file0))
% 
% figure(2)
% subplot(1, 2, 1)
% plot(data1_equalized)
% title(sprintf('data%s-purpleSens acceleration time plot', file0))
% ylabel('m/s^2')
% xlabel('samples')
% 
% subplot(1, 2, 2)
% Nx = length(data1_equalized);       % length of data
% nsc = floor(Nx/100);                % window of fft calculation
% nov = floor(nsc/2);                 % 50% window overlap (smoothing the spectogram)
% nff = max(512, 2^nextpow2(nsc));    % fft number of points
% 
% spectrogram(data1_equalized, hamming(nsc), nov, nff, 'MinThreshold',-70, 'yaxis');
% title(sprintf('data%s-purpleSens Spectogram', file0))



%% ----- cross correlation spectogram plot -------
% figure(3)
% nwin = 200;                           % cross correlation window
% rows = min([rows, rows1]);
% disp(rows)
% xspectrogram(data0_equalized(1:rows), data1_equalized(1:rows), kaiser(nwin, 10), nwin - 1, [], ...
%     'power', 'MinThreshold', -70, 'yaxis')
% title(sprintf('Cross-Correlation Spectogram of data%s ', file0))

%% -------- filtering the signals (filter bank) ------
fs = 1200;
rows = min([rows, rows1]);
data0_equalized(1:rows) = bandpass(data0_equalized(1:rows),[30 210],fs);
data0_equalized(1:rows) = bandstop(data0_equalized(1:rows),[60 90],fs);
data0_equalized(1:rows) = bandstop(data0_equalized(1:rows),[120 150],fs);
data1_equalized(1:rows) = bandpass(data1_equalized(1:rows),[30 210],fs);
data1_equalized(1:rows) = bandstop(data1_equalized(1:rows),[60 90],fs);
data1_equalized(1:rows) = bandstop(data1_equalized(1:rows),[120 150],fs);

% --- upsample
% data0_equalized = resample(data0_equalized, 4, 1);
% rows = numel(data0_equalized) / 2;
% data0_equalized = data0_equalized(1:rows);
% data1_equalized = resample(data1_equalized, 4, 1);
% rows1 = numel(data1_equalized) / 2;
% data1_equalized = data1_equalized(1:rows1);
%% ----- filtered cross correlation spectogram plot -------
% figure(6)
% nwin = 200;                           % cross correlation window
% rows = min([rows, rows1]);
% disp(rows)
% xspectrogram(data0_equalized(1:rows), data1_equalized(1:rows), kaiser(nwin, 10), nwin - 1, [], ...
%     'power', 'MinThreshold', -55, 'yaxis')
% title(sprintf('Filtered Cross-Correlation Spectogram of data%s ', file0))




%% ------- normalized cross correlation plot in time ----------

% ------ find delay of two signals ----
% figure(4)
rows = min([rows, rows1]);
D = finddelay(data0_equalized(1:rows), data1_equalized(1:rows))

% ------ plot Cross-Corr in time ----
figure(4)
[c, lags] = xcorr(data0_equalized(1:rows), data1_equalized(1:rows));
plot(lags, c)
title(sprintf('cross corrolation in time (data%s equal length)', file0))
xlabel('t (samples)')
xlim([-300, 300])

% r_xy = xcorr(out0, out1);
% plot(r_xy / min(r_xy))
% title(sprintf('filtered normalized cross corrolation in times (data%s equal length)', file0))
% xlabel('t')

%% -------- phase vs freq --------
% rows = min([rows, rows1]);
% fft0 = fft(data0_equalized(1:rows), 1024, 1);
% figure(6)
% plot(linspace(0, 1000, numel(fft0(10:end - 10))), -1 * unwrap(atan2(imag(fft0(10:end - 10)), real(fft0(10:end - 10)))))
% xlabel('freq (Hz)')
% title(sprintf('phase Vs freq of (data%s)', file0))
% ylabel('unwraped angle deg (degrees)')
% % ylim([0, 1300])
% % xlim([0, 1000])
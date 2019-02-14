clc
clear all
%% Se leen ambos canales de ThingSpeak
size=30;
[data_ch1,time_ch1]=thingSpeakRead(699937,'NumPoints',size);%De cada campo 
% (temperatura y humedad) se cogen 30 datos. 
% Se almacenan los valores y los tiempos
[data_ch2,time_ch2]=thingSpeakRead(699938,'NumPoints',size);

%% Unimos ambos arrays de datos
data=zeros(size*2,2);
aux=1; %Para recorrer el vector pequeño
for i=1:2:2*size
    %Datos
    data(i,1)=data_ch1(aux,1);
    data(i,2)=data_ch1(aux,2);
    data(i+1,1)=data_ch2(aux,1);
    data(i+1,2)=data_ch2(aux,2);
    %Tiempo
    time(i,1)=time_ch1(aux,1);
    time(i+1,1)=time_ch2(aux,1);
    
    aux=aux+1;
end

%% Creamos dos gráficos de temperatura y humedad

%Temperatura
figure();
plot(time,data(:,1),'r','LineWidth',1.5);
title('Temperatura');
xlabel('Fecha');
ylabel('Grados(ºC)');
grid on;

%Humedad
figure();
plot(time,data(:,2),'b','LineWidth',1.5);
title('Humedad');
xlabel('Fecha');
ylabel('Porcentaje(%)');
grid on;

%% Fuzzy control

act_temp=zeros(size*2,1);
act_hum=zeros(size*2,1);
act_clim=zeros(size*2,1);

for i=1:2:2*size
    %Comprobacion temperatura
    if(data(i,1)>=20.5)
        act_temp(i,1)=1;
    else
        act_temp(i,1)=0;
    end
    %Comprobacion humedad
    if(data(i,2)>=55)
        act_hum(i,1)=1;
    else
        act_hum(i,1)=0;
    end
    %Combinacion
    if(act_temp(i,1)==1 && act_hum(i,1)==1)
        act_clim(i,1)=1;
    else
        act_clim(i,1)=0;
    end    
end

%Graficar
figure();
subplot(3,1,1);
title('Control de climatizador');
plot(act_temp,'r','LineWidth',1.5);
ylabel('Activación regla temperatura');
subplot(3,1,2);
plot(act_hum,'b','LineWidth',1.5);
ylabel('Activación regla humedad');
subplot(3,1,3);
plot(act_clim,'g','LineWidth',1.5);
ylabel('Activación climatizador');





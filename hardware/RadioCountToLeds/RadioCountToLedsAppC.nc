#include "RadioCountToLeds.h"

configuration RadioCountToLedsAppC {
}

implementation {
  components MainC, RadioCountToLedsC as App, LedsC;
  components new AMSenderC(AM_RADIO_COUNT_MSG);
  components new AMReceiverC(AM_RADIO_COUNT_MSG);
  components new TimerMilliC() as T0;
  components new TimerMilliC() as T1;
  components ActiveMessageC;
  
  App.Boot -> MainC.Boot;
  
  App.Receive -> AMReceiverC;
  App.AMSend -> AMSenderC;
  App.AMControl -> ActiveMessageC;
  App.Leds -> LedsC;
  App.SendTimer -> T0;
  App.BitTimer -> T1;
  App.Packet -> AMSenderC;
}



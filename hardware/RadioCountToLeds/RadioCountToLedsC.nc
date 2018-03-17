#include "Timer.h"
#include "RadioCountToLeds.h"
 
module RadioCountToLedsC @safe() {
  uses {
    interface Leds;
    interface Boot;
    interface Receive;
    interface AMSend;

    interface Timer<TMilli> as SendTimer;
    interface Timer<TMilli> as BitTimer;

    interface SplitControl as AMControl;
    interface Packet;
  }
}

implementation {

	message_t packet;

    bool locked;
    uint16_t counter = 0;
    uint16_t temp = 1;

    event void Boot.booted() {
        call AMControl.start();
    }
  
    event void AMControl.startDone(error_t err) {
        if (err == SUCCESS) {
          call BitTimer.startPeriodic(TIMER_BIT_PERIOD_MILLI);
        }
        else {
           call AMControl.start();
        }
    }
  
    event void AMControl.stopDone(error_t err) {
        // do nothing
    }
    
	uint16_t getBit(){
		temp += 1;
		return temp%2;
	}

	event void BitTimer.fired(){
		uint16_t bit = getBit();

		if(bit){
			if(!(call SendTimer.isRunning()) ){
				call SendTimer.startPeriodic(TIMER_SEND_PERIOD_MILLI);
				call Leds.led2On();
			}	
		}	
		else{
			if(call SendTimer.isRunning()){
				call SendTimer.stop();
				call Leds.led2Off();
			}
		}
	}	


	event void SendTimer.fired() {
    	counter++;
	    dbg("RadioCountToLedsC", "RadioCountToLedsC: timer fired, counter is %hu.\n", counter);
    	if (!locked) {
	      	radio_count_msg_t* rcm = (radio_count_msg_t*)call Packet.getPayload(&packet, sizeof(radio_count_msg_t));
			if (rcm == NULL) return;

			rcm->counter = 0;

			rcm->payload1  = 0; rcm->payload2  = 0; rcm->payload3  = 0; rcm->payload4  = 0; rcm->payload5 = 0; 
			rcm->payload6  = 0; rcm->payload7  = 0; rcm->payload8  = 0; rcm->payload9  = 0; rcm->payload10 = 0;
			rcm->payload11 = 0; rcm->payload12 = 0; rcm->payload13 = 0; rcm->payload14 = 0; rcm->payload15 = 0;
			rcm->payload16 = 0; rcm->payload17 = 0; rcm->payload18 = 0; rcm->payload19 = 0; rcm->payload20 = 0;
			rcm->payload21 = 0; rcm->payload22 = 0; rcm->payload23 = 0; rcm->payload24 = 0; rcm->payload25 = 0;
			rcm->payload26 = 0; rcm->payload27 = 0; rcm->payload28 = 0;


			if (call AMSend.send(AM_BROADCAST_ADDR, &packet, sizeof(radio_count_msg_t)) == SUCCESS) {
				dbg("RadioCountToLedsC", "RadioCountToLedsC: packet sent.\n", counter);	
				call Leds.led0Toggle();
				locked = TRUE;
      		}
    	}
	}

	event message_t* Receive.receive(message_t* bufPtr, void* payload, uint8_t len) {
    	dbg("RadioCountToLedsC", "Received packet of length %hhu.\n", len);
	    if (len == sizeof(radio_count_msg_t)){
			radio_count_msg_t* rcm = (radio_count_msg_t*)payload;
			call Leds.set(rcm->counter);
	    }
		return bufPtr;
	}

	event void AMSend.sendDone(message_t* bufPtr, error_t error) {
    	if (&packet == bufPtr) {
			locked = FALSE;
	    }
	}

}





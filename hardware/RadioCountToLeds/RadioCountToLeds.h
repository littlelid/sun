#ifndef RADIO_COUNT_TO_LEDS_H
#define RADIO_COUNT_TO_LEDS_H

typedef nx_struct radio_count_msg {
  nx_uint16_t counter;
// 125 - 12 = 113
// 113 / 4 = 28
nx_uint32_t payload1;
nx_uint32_t payload2;
nx_uint32_t payload3;
nx_uint32_t payload4;
nx_uint32_t payload5;
nx_uint32_t payload6;

nx_uint32_t payload7;
nx_uint32_t payload8;
nx_uint32_t payload9;

nx_uint32_t payload10;
nx_uint32_t payload11;
nx_uint32_t payload12;

nx_uint32_t payload13;
nx_uint32_t payload14;
nx_uint32_t payload15;
nx_uint32_t payload16;
nx_uint32_t payload17;
nx_uint32_t payload18;

nx_uint32_t payload19;
nx_uint32_t payload20;
nx_uint32_t payload21;
nx_uint32_t payload22;
nx_uint32_t payload23;
nx_uint32_t payload24;

nx_uint32_t payload25;
nx_uint32_t payload26;
nx_uint32_t payload27;
nx_uint32_t payload28;

} radio_count_msg_t;

enum {
  AM_RADIO_COUNT_MSG = 6,
  TIMER_SEND_PERIOD_MILLI = 1,
  TIMER_BIT_PERIOD_MILLI = 1000
};

#endif

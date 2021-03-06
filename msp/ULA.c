#include "msp430F5529.h" //Contains definitions for registers and built-in functions
#include "driverlib.h"

static int counter = 0;

void main(void)
{
WDTCTL = WDTPW + WDTHOLD; // Stop WDT

TA0CCTL0 = CCIE; // CCR0 interrupt enabled
TA0CTL = TASSEL_2 | MC_1 | ID_3; // SMCLK/8, upmode
TA0CCR0 = 270; // I have to calculate it, but I was lazy Hz

P1OUT &= 0x00; // Shut down pins on P1
P1DIR &= 0x00; // Set P1 pins as output
P1DIR |= BIT6; // P1.0 pin set as output the rest are input

/*
P3OUT &= 0x00;
P3DIR &= 0x01;
P3REN = BIT7;
P3OUT = BIT7;
*/

GPIO_setAsInputPinWithPullUpResistor(GPIO_PORT_P3, GPIO_PIN7);

P4OUT &= 0x00; // Shut down pins on P4
P4DIR &= 0x00; // Set P4 pins as output
P4DIR |= BIT7; // P4.7 pin set as output the rest are input

P2REN |= BIT0; // Enable internal pull-up/down resistors for P2
P2OUT |= BIT0; //Select pull-up mode for P2.1

P2IE |= BIT0; // P2.1 interrupt enabled
P2IES |= BIT0; // P2.1 Hi/lo edge
P2IFG &= ~BIT0; // P2.1 IFG cleared

_BIS_SR(CPUOFF + GIE); // Enter LPM0 w/ interrupt

while(1) //Loop forever, we work with interrupts!
{}
}

// Timer A0 interrupt service routine
#pragma vector=TIMER0_A0_VECTOR
__interrupt void Timer_A0 (void)
{
P1OUT ^= BIT6; // Toggle P1.0

}

// Port 2 interrupt service routine
#pragma vector=PORT2_VECTOR
__interrupt void Port_2(void)
{
static int debounce = 0;

while(debounce <= 100)
{
if (~P2IN & BIT0) debounce++;
else debounce = 0;
}
counter++;

//if ((P3IN & BIT7) == 1) {
if (GPIO_getInputPinValue(GPIO_PORT_P3,GPIO_PIN7)) {
    TA0CCR0 -= 2;
}
else {
    TA0CCR0 += 2;
}

P4OUT ^= BIT7; // Toggle P4.7
debounce = 0;

P2IFG &= ~BIT0; // P2.1 IFG cleared
}

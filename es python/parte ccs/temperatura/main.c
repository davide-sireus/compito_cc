#include <msp430.h> 
#include <timer.h>
#include "serial.h"
#include <stdio.h>

#define CALADC12_15V_30C *((unsigned int *)0x1A1A)
#define CALADC12_15V_85C *((unsigned int *)0x1A1C)

char stringa[5];
unsigned long time = 0;
/**
 * main.c
 */
void setup(){
    REFCTL0 &=~ REFMSTR;
    ADC12CTL0 |= ADC12SHT0_8 + ADC12ON;

    ADC12CTL1 = ADC12SHP + ADC12CONSEQ_0;

    ADC12MCTL0 |= ADC12INCH_10;
    ADC12CTL0 |= ADC12REFON;
    ADC12CTL0 &= ~ ADC12REF2_5V;
    ADC12MCTL0 |= ADC12SREF_1;
    ADC12CTL0 |= ADC12ENC + ADC12SC;

    init_timer();
    init_serial();


    while(ADC12CTL1&ADC12BUSY);

}

float conversion(long adc_value){

    return (float)((adc_value - CALADC12_15V_30C) * 55)
                /(CALADC12_15V_85C - CALADC12_15V_30C) + 30.0f;

}
void setup();

void stampa(int intero, int decimale){ //funzione che serve a stampare carattere per carattere i valori dei secondi

    int c = 0;
        sprintf(stringa, "%d.%d\n", intero, decimale);
    do{
        bsend_ch(stringa[c]); //invio un carattere alla volta alla funzione bsend in modo da stampare in seriale
        c++;
    }while(stringa[c] != '\0'); // la stampa si ferma una volta trovato il carattere terminale


}

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD; // stop watchdog timer
    setup();
    int result_int, result_dec;
    while(1){
        ADC12CTL0 |= ADC12ENC + ADC12SC;

        if (millis() - time > 1000){
            float t = conversion(ADC12MEM0);
            result_int = (int)t;
            result_dec = (int)(t*10)%10;

            time = millis();
            stampa(result_int, result_dec);
        }
        while(ADC12CTL1&ADC12BUSY);
    }

}

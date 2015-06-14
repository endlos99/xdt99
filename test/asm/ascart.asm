* EXECUTABLE CART IMAGE

       IDT  'ASCART'
        
VDPWD  EQU  >8C00             * VDP write data
VDPWA  EQU  >8C02             * VDP set read/write address
WRKSP  EQU  >8300             * Workspace memory in fast RAM
R0LB   EQU  WRKSP+1           * Register zero low byte address

MSG1   TEXT 'HELLO CART!'
MSG1E
       EVEN

MAIN   LIMI 0                 * Disable interrupts
       LWPI WRKSP             * Load the workspace pointer to fast RAM

*                               Clear the screen
       CLR  R0                * Start at top left corner of the screen
       LI   R1,>2000          * Write a space (>20 hex is 32 decimal)
       LI   R2,768            * Number of bytes to write

       MOVB @R0LB,@VDPWA      * Send low byte of VDP RAM write address
       ORI  R0,>4000          * Set read/write bits 14 and 15 to write (01)
       MOVB R0,@VDPWA         * Send high byte of VDP RAM write address

CLS    MOVB R1,@VDPWD         * Write byte to VDP RAM
       DEC  R2                * Byte counter
       JNE  CLS               * Check if done

*                               Write the text message to the screen
       LI   R0,395            * Screen location to display message
       LI   R1,MSG1           * Memory location of source data
       LI   R2,MSG1E-MSG1     * Length of data to write

       MOVB @R0LB,@VDPWA      * Send low byte of VDP RAM write address
       ORI  R0,>4000          * Set read/write bits 14 and 15 to write (01)
       MOVB R0,@VDPWA         * Send high byte of VDP RAM write address

DISP   MOVB *R1+,@VDPWD       * Write a byte of the message to the VDP
       DEC  R2                * Byte counter
       JNE  DISP              * Check if done

       LIMI 2                 * Enable interrupts
INFLP  JMP  INFLP             * Infinite loop

SLAST  END  MAIN
